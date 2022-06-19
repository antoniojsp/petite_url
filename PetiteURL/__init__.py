from database import PetiteUrlDatabase
from config import Config
from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ['secret_key']
    return app


def create_database():
    return PetiteUrlDatabase(os.environ['URI'])


def get_personal_info():
    return Config().dict()


db = create_database()

