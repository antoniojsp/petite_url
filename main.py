import configparser
from database import *
from flask import Flask, redirect, render_template, request, flash, send_from_directory, url_for
import logging
import os
import validators
from forms import PetiteURLForm
configurations = configparser.ConfigParser()
configurations.read("credentials.ini")

app = Flask(__name__)
app.secret_key = configurations['API']['flash']

logging.basicConfig(filename='record.log',
                    level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

db = TinyURLDatabase()


@app.route('/', methods=["GET", "POST"])
def index():
    personal_github_url = f'{request.base_url}66284f2b21'
    cform = PetiteURLForm()

    if cform.validate_on_submit():
        original_url = cform.name.data
        is_valid_url = validators.url(original_url)
        url_link = ""

        cform = PetiteURLForm()

        if is_valid_url:
            shorten_url = db.insert(original_url)
            app.logger.info(f'{original_url} inserted')
            url_link = f'{request.base_url}{shorten_url}'
            flash(url_link)
        elif original_url == "":
            app.logger.info(f'Empty')
            flash('Invalid website')
        else:
            app.logger.info(f'{original_url} is an empty url')
            flash('You need to enter a URL')

        return render_template("index.html", link=url_link, github= personal_github_url, form=PetiteURLForm())

    return render_template("index.html", github= personal_github_url, form=cform)


@app.route('/<shorten_url_token>')
def redirect_from_token(shorten_url_token: str):
    full_url = db.query_url(shorten_url_token)
    if full_url == "":
        return render_template("404.html")
    print(f'Redirecting to ->  {request.base_url}{shorten_url_token}')
    return redirect(full_url, code=302)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',mimetype='image/vnd.microsoft.icon')



if __name__ == '__main__':
    app.run()

