from app.database import TinyURLDatabase
from config import Config
from flask import Flask
import os


def create_app():
    uri = os.environ['URI']
    secret_key = os.environ['secret_key']
    app = Flask(__name__)
    app.secret_key = secret_key
    my_info = Config().dict()
    db = TinyURLDatabase(uri)
    return app, my_info, db

