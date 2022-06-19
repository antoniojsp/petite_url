from flask import Blueprint

ruta = Blueprint('ajax', __name__)
from PetiteURL.ajax import views

