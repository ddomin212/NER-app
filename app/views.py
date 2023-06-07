"""
This module contains the Flask routes for the AI chatbot application.
It includes a route for rendering the index.html template and a
route for accepting a JSON request and returning a response using a GPT model.
"""
import os
from flask import render_template, request, flash, jsonify, send_file, g
from app.functions import *
from app import app


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Renders the index.html template if the request method is GET.

    If the request method is POST, it checks if a file was
    uploaded and returns an error message if not.

    If a file was uploaded, it initializes a Kaggle dataset
    and returns the result of a named entity recognition algorithm.
    """
    if request.method != "POST":
        return render_template("index.html")
    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return "No file selected", 400
    first_time = (
        "no"
        if os.path.isdir(os.path.join("app", "static", "generated", "dataset"))
        else "yes"
    )
    if first_time == "yes":
        init_kaggle()
    data = get_ner_kaggle(uploaded_file, first_time)
    g.loading_complete = True
    return render_template("result.html", data=data)


@app.route("/api/gpt-modal", methods=["POST"])
def gpt_modal():
    """
    Accepts a JSON request with a name and tags field.
    Uses the name and tags to generate a response using a GPT model.
    Returns the response and an image URL.
    """
    if not request.json:
        return "Did not recieve data", 400
    if name := request.json["name"]:
        tags = request.json["tags"]
        data, img_url = get_response(name, tags)
        g.loading_complete = True
        return jsonify({"response": data, "img_url": img_url})
    return "Did not recieve data", 400


@app.route("/api/export", methods=["GET"])
def export():
    """
    If a file exists at the specified path, sends the file as an attachment.
    Otherwise, returns an error message.
    """
    print(os.path.join("app", "static", "generated", "output", "data.xlsx"))
    if os.path.exists(
        os.path.join("app", "static", "generated", "output", "data.xlsx")
    ):
        return send_file(
            os.path.join("static", "generated", "output", "data.xlsx"),
            as_attachment=True,
        )
    return "Did not recieve data", 400
