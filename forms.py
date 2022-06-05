from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL


class PetiteURLForms(FlaskForm):
    url = StringField(label='URL', validators=[DataRequired()])
    expiration = BooleanField(label='Expires')
    submit = SubmitField(label="Shorten")
