from app.database import TinyURLDatabase
from config import Config
from flask import Flask
import os

def create_app():
    URI = os.environ['URI']
    SECRET_KEY = os.environ['secret_key']
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    my_info = Config().dict()
    db = TinyURLDatabase(URI)
    return app, my_info, db

