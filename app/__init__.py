from app.database import PetiteUrlDatabase
from app.config import Config
import os
from flask import Flask


db = PetiteUrlDatabase(os.environ['URI'])
my_info = Config().dict()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ['secret_key']

    return app