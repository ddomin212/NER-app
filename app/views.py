from flask import render_template, request, flash, jsonify, send_file, g
import os
from app.functions import *
from app import app


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method != "POST":
        return render_template("index.html")
    if "file" not in request.files:
        flash("No file part")
    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return "No file selected", 400
    first_time = "no" if os.path.isdir(os.path.join("app", "static","generated","dataset")) else "yes"
    if first_time == "yes":
        init_kaggle()
    data = get_ner_kaggle(uploaded_file, first_time)
    g.loading_complete = True
    return render_template("result.html", data=data)


@app.route("/api/gpt-modal", methods=["POST"])
def gpt_modal():
    if name := request.json["name"]:
        tags = request.json["tags"]
        data, img_url = get_response(name, tags)
        g.loading_complete = True
        return jsonify({"response": data, "img_url": img_url})
    else:
        return "Did not recieve data", 400


@app.route("/api/export", methods=["GET"])
def export():
    print(os.path.join("app","static","generated","output", "data.xlsx"))
    if os.path.exists(os.path.join("app","static","generated","output", "data.xlsx")):
        return send_file(os.path.join("static","generated","output", "data.xlsx"), as_attachment=True)
    else:
        return "Did not recieve data", 400
