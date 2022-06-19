from flask import Blueprint
ruta = Blueprint('routes', __name__)
from PetiteURL.routes import views
