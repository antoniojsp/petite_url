# from PetiteURL import create_app
from flask import Flask
from database import PetiteUrlDatabase
import os
from config import Config
# from routes.views import ruta as routes
from routes.views import ruta as routes


app = Flask(__name__)
app.secret_key = os.environ['secret_key']
# db = PetiteUrlDatabase(os.environ['URI'])
my_info = Config().dict()

app.register_blueprint(routes)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)


