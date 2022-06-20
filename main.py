# from PetiteURL import create_app
from flask import Flask
import os
from config import Config
from ajax.views import ruta as ajax
from routes.views import ruta as routes


app = Flask(__name__)
app.secret_key = os.environ['secret_key']
my_info = Config().dict()

app.register_blueprint(routes)
app.register_blueprint(ajax)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)


