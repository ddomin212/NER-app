"""
This module initializes the Flask application and sets up the app's secret key.
It also imports the app's views module.
"""
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.debug = True
app.secret_key = os.getenv("PAGE_SECRET")

from app import views
