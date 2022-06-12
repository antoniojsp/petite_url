from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField


class PetiteURLForms(FlaskForm):
    url = StringField(label='URL', validators=[DataRequired()])
    expires = BooleanField(label='Do you want the link to expire?  ', render_kw={"onclick": "hide_show_expiration('date_local', '#expires')"})
    submit = SubmitField(label="Shorten", render_kw={"class":"btn btn-success"})
    personalized_name = BooleanField(label="Do you want to personalized the hash value?", render_kw={"onclick": "hide_show_expiration('personalized', '#personalized_name')"})
    custom_hash = StringField(validators=[Length(max=7)])
    exp_date = DateTimeLocalField()
