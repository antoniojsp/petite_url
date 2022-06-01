import configparser
from database import *
from collections import namedtuple
from flask import Flask, redirect, render_template, request, flash, send_from_directory, url_for
from forms import PetiteURLForm
import logging
import os
import validators

# separation of concerns
configurations = configparser.ConfigParser()
configurations.read("credentials.ini")

app = Flask(__name__)
app.secret_key = configurations['API']['flash']

logging.basicConfig(filename='record.log',
                    level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


db = TinyURLDatabase()

# my info
informacion = namedtuple('MyInfo', ['email', 'github'])
my_info = informacion("antonios@uoregon.edu", "72b594348a")


@app.route('/', methods=["GET", "POST"])
def index():
    personal_github_url = f'{request.base_url}{my_info.github}'
    forma = PetiteURLForm()

    if forma.validate_on_submit():
        original_url = forma.name.data
        is_valid_url = validators.url(original_url)

        if is_valid_url:
            shorten_url = db.insert(original_url)

            if shorten_url == "404":
                flash('Website Down')
                return redirect(url_for('index'))

            app.logger.info(f'{original_url} inserted')
            url_link = f'{request.base_url}{shorten_url}'
            flash(url_link)
        elif original_url == "":
            app.logger.info(f'Empty')
            flash('No input')
        else:
            app.logger.info(f'{original_url} is an empty url')
            flash('You need to enter a URL')

        return redirect(url_for('index'))

    return render_template("index.html", github=personal_github_url, form=forma, email=my_info.email)


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

