from database import Database
from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ['secret_key']
    return app


def create_database():
    return Database(os.environ['URI'])


db = create_database()

