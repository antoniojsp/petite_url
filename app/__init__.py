from database import TinyURLDatabase
from config import Config
from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ['secret_key']
    my_info = Config().dict()
    db = TinyURLDatabase(os.environ['URI'])

    return app, my_info, db

