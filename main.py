# from PetiteURL import create_app
from flask import Flask
import os
from PetiteURL.ajax.views import ruta as ajax
from PetiteURL.routes.views import ruta as routes

app = Flask(__name__)
app.secret_key = os.environ['secret_key']
app.register_blueprint(ajax)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)


