from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.debug = True
app.secret_key = os.getenv('PAGE_SECRET')

from app import views