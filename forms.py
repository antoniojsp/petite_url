from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class PetiteURLForm(FlaskForm):
    name = StringField(label='URL', validators=[DataRequired()])
    submit = SubmitField(label="Submit")