from app.forms import PetiteURLForms
from app import db
from app import my_info
from flask import redirect, render_template, request

from flask import Blueprint

ruta = Blueprint('login', __name__)


@ruta.route('/login/user', methods=["GET", "POST"])
def login():

    user = request.args['user']
    password = request.args['password']

    return render_template("login.html")




