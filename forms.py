from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from wtforms.validators import DataRequired, URL


class PetiteURLForms(FlaskForm):
    url = StringField(label='URL', validators=[DataRequired()])
    submit = SubmitField(label="Shorten")
