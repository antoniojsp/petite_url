from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL


class PetiteURLForms(FlaskForm):
    url = StringField(label='URL', validators=[DataRequired()])
    expires = BooleanField(label='Do you want the link to expire?:  ')
    submit = SubmitField(label="Shorten")
    personalized_name = BooleanField(label="Do you want to personalized the hash number?")
