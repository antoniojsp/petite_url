from flask import request, jsonify, Blueprint
from app.utilities import is_url_alive
import validators
from app import db

ruta = Blueprint('ajax', __name__)


@ruta.route("/_submit")
def _submit():
    original_url = request.args.get("url", type=str)
    exp_date = request.args.get("expiration_date", type=str)
    custom_hash = request.args.get("custom_hash", type=str)

    is_legal_url = validators.url(original_url)

    # Validations. URL is legal and alive. Client use JS to do validations too but for extra protection
    if not is_legal_url:
        result = 'Please, check that the URL is legal and try again.'
    elif not is_url_alive(original_url):
        result = "The website is either offline, forbidden or cannot be found."
    else:
        try:
            shorten_url = db.insert(original_url, exp_date, custom_hash)
        except LookupError as e:  # In case a duplicate custom_hash is sent to the server. JS also check for duplicates
            shorten_url = "Duplicate"
            print("Error occurred", e)

        result = f'{request.url_root}{shorten_url}'

        if shorten_url == "Duplicate":
            result = f"The hash name {custom_hash} exists"

    return jsonify(result={"response": result})


@ruta.route("/_check_hash")
def _check_name():
    partial_name = request.args.get("name", type=str)
    result = db.is_hash_duplicated(partial_name)

    return jsonify(result={"response": result})
