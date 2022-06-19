from app.forms import PetiteURLForms
import os
import logging
from app import create_app
from flask import redirect, render_template, request, send_from_directory, jsonify
from app.utilities import is_url_alive
import validators


logging.basicConfig(filename='record.log',
                    level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app, my_info, db = create_app()


@app.route('/', methods=["GET", "POST"])
def index():
    index_form = PetiteURLForms()
    return render_template("index.html", form=index_form, info=my_info), 200


@app.route('/<shorten_url_hash>')
def redirect_from_token(shorten_url_hash: str):
    query_answer = db.query_url(shorten_url_hash)
    result = f'{request.url_root}{shorten_url_hash}'

    if query_answer == "Not found":
        return render_template("404.html", message=f"The URL {result} was not found in the server."), 404

    # If the hash_value is present and not expired, then it redirect to the URL from the database
    app.logger.info(f'Redirecting to ->  result')
    return redirect(query_answer, code=302)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'app/static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# AJAX methods
@app.route("/_submit")
def _submit():
    original_url = request.args.get("url", type=str)
    exp_date = request.args.get("expiration_date", type=str)
    custom_hash = request.args.get("custom_hash", type=str)

    is_legal_url = validators.url(original_url)

    # Validations. URL is legal and alive. Client use JS to do validations too but for extra protection
    if not is_legal_url:
        app.logger.info(f'{original_url} is not a valid URL')
        result = 'Please, check that the URL is legal and try again.'
    elif not is_url_alive(original_url):
        app.logger.info(f'{original_url} is not a live URL')
        result = "The website is either offline, forbidden or cannot be found."
    else:
        try:
            shorten_url = db.insert(original_url, exp_date, custom_hash)
        except LookupError as e:  # In case a duplicate custom_hash is sent to the server. JS also check for duplicates
            shorten_url = "Duplicate"
            print("Error occurred", e)

        app.logger.info(f'{original_url} inserted')
        result = f'{request.url_root}{shorten_url}'

        if shorten_url == "Duplicate":
            result = f"The hash name {custom_hash} exists"

    return jsonify(result={"response": result})


@app.route("/_check_hash")
def _check_name():
    partial_name = request.args.get("name", type=str)
    result = db.is_hash_duplicated(partial_name)

    return jsonify(result={"response": result})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)


