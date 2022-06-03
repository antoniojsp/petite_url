from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from wtforms.validators import DataRequired


class PetiteURLForms(FlaskForm):
    name = StringField(label='URL', validators=[DataRequired()])
    submit = SubmitField(label="Shorten")
