from forms import PetiteURLForms
from flask import redirect, render_template, request, send_from_directory
import os
from PetiteURL.routes import ruta
from PetiteURL import db as data
from PetiteURL import Config

my_info = Config().dict()


@ruta.route('/', methods=["GET", "POST"])
def index():
    index_form = PetiteURLForms()
    return render_template("index.html", form=index_form, info=my_info), 200


@ruta.route('/<shorten_url_hash>')
def redirect_from_token(shorten_url_hash: str):
    query_answer = data.query_url(shorten_url_hash)
    result = f'{request.url_root}{shorten_url_hash}'

    if query_answer == "Not found":
        return render_template("404.html", message=f"The URL {result} was not found in the server."), 404

    # If the hash_value is present and not expired, then it redirect to the URL from the database
    # PetiteURL.logger.info(f'Redirecting to ->  result')
    return redirect(query_answer, code=302)


# @ruta.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'PetiteURL/static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')