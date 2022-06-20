# from PetiteURL import create_app
from flask import Flask
import os
from app.ajax.views import ruta as ajax
from app.routes.views import ruta as routes


app = Flask(__name__, template_folder="./app/templates", static_folder="./app/static")
app.secret_key = os.environ['secret_key']

app.register_blueprint(routes)
app.register_blueprint(ajax)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)


