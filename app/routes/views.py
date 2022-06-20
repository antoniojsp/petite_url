from app.forms import PetiteURLForms
from app import db
from app import my_info
from flask import redirect, render_template, request, Blueprint

ruta = Blueprint('routes', __name__)


@ruta.route('/', methods=["GET", "POST"])
def index():
    index_form = PetiteURLForms()
    return render_template("index.html", form=index_form, info=my_info), 200


@ruta.route('/<shorten_url_hash>')
def redirect_from_token(shorten_url_hash: str):
    query_answer = db.query_url(shorten_url_hash)
    result = f'{request.url_root}{shorten_url_hash}'

    if query_answer == "Not found":
        return render_template("404.html", message=f"The URL {result} was not found in the server."), 404

    # If the hash_value is present and not expired, then it redirect to the URL from the database
    # PetiteURL.logger.info(f'Redirecting to ->  result')
    return redirect(query_answer, code=302)

#
# ruta.add_url_rule('/', view_func=index, methods=["GET", "POST"])
# ruta.add_url_rule('/<shorten_url_hash>', view_func=redirect_from_token)
