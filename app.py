from database import TinyURLDatabase
from flask import Flask, redirect, render_template, request, flash, send_from_directory, url_for, jsonify
from forms import PetiteURLForms
import logging
from personal_information import *
import os
from utilities import is_url_alive
import validators

# Environment variables (Secret keys)
URI = os.environ['URI']
SECRET_KEY = os.environ['secret_key']
SIZE_HASH = int(os.environ['size_hash'])


logging.basicConfig(filename='record.log',
                    level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
app.secret_key = SECRET_KEY

my_info = PersonalInformation().dict()

db = TinyURLDatabase(URI)


@app.route('/', methods=["GET", "POST"])
def index():
    index_form = PetiteURLForms()
    return render_template("index.html", form=index_form, info=my_info)


@app.route('/<shorten_url_hash>')
def redirect_from_token(shorten_url_hash: str):
    query_answer = db.query_url(shorten_url_hash)

    if query_answer == "Not found":
        return render_template("404.html", message= "The URL was not found in the server.")
    elif query_answer == "Expired":
        return render_template("404.html", message="The URL has expired.")

    # If the hash+value is present and not expired, then it redirect to the URL from the database
    app.logger.info(f'Redirecting to ->  {request.base_url}{shorten_url_hash}')
    return redirect(query_answer, code=302)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# AJAX methods
@app.route("/_submit")
def _submit():
    original_url = request.args.get("url", type=str)
    exp_date = request.args.get("expiration_date", type=str)
    is_legal_url = validators.url(original_url)

    if not is_legal_url:
        app.logger.info(f'{original_url} is not a valid URL')
        result = 'Please, check that the URL is legal and try again.'
        is_href = False

    elif not is_url_alive(original_url):
        app.logger.info(f'{original_url} is not a live URL')
        result = "The website is either offline, forbidden or cannot be found."
        is_href = False
    else:
        shorten_url = db.insert(original_url, exp_date, SIZE_HASH)
        app.logger.info(f'{original_url} inserted')
        result = f'{request.url_root}{shorten_url}'
        is_href = True

    return jsonify(result={"response": result, "href": is_href})

@app.route("/_check_hash")
def _check_name():
    original_url = request.args.get("url", type=str)
    exp_date = request.args.get("expiration_date", type=str)
    is_legal_url = validators.url(original_url)

    if not is_legal_url:
        app.logger.info(f'{original_url} is not a valid URL')
        result = 'Please, check that the URL is legal and try again.'
        is_href = False

    elif not is_url_alive(original_url):
        app.logger.info(f'{original_url} is not a live URL')
        result = "The website is either offline, forbidden or cannot be found."
        is_href = False
    else:
        shorten_url = db.insert(original_url, exp_date, SIZE_HASH)
        app.logger.info(f'{original_url} inserted')
        result = f'{request.url_root}{shorten_url}'
        is_href = True

    return jsonify(result={"response": result, "href": is_href})



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)


