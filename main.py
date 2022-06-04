import configparser
from collections import namedtuple
from database import *
from flask import Flask, redirect, render_template, request, flash, send_from_directory, url_for, jsonify
from forms import PetiteURLForms
import logging
import os
from utilities import check_url_alive, enviroment_settings
import validators

# separation of concerns (dictionary with setting variables and keys)
my_info = enviroment_settings("credentials.ini")

app = Flask(__name__)
app.secret_key = my_info['secret_word']

logging.basicConfig(filename='record.log',
                    level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

db = TinyURLDatabase()


@app.route('/', methods=["GET", "POST"])
def index():
    form = PetiteURLForms()
    return render_template("index.html", form=form, info=my_info)


@app.route('/<shorten_url_token>')
def redirect_from_token(shorten_url_token: str):
    full_url = db.query_url(shorten_url_token)
    if full_url == "":
        return render_template("404.html")
    app.logger.info(f'Redirecting to ->  {request.base_url}{shorten_url_token}')
    return redirect(full_url, code=302)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# AJAX methods
@app.route("/_submit")
def _submit():
    original_url = request.args.get("url", type=str)
    is_legal_url = validators.url(original_url)
    is_alive_url = check_url_alive(original_url)
    if not is_legal_url:
        app.logger.info(f'{original_url} is not a valid URL')
        result = 'Please, check that the URL is legal and try again.'
        is_href = False

    elif not is_alive_url:
        app.logger.info(f'{original_url} is not a live URL')
        result = "The website is either offline, forbidden or cannot be found."
        is_href = False
    else:
        shorten_url = db.insert(original_url)
        app.logger.info(f'{original_url} inserted')
        result = f'{request.url_root}{shorten_url}'
        is_href = True

    return jsonify(result={"response": result, "href": is_href})


if __name__ == '__main__':
    app.run()

