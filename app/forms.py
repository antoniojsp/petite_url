from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField


class PetiteURLForms(FlaskForm):
    url = StringField(label='URL', validators=[DataRequired()],
                      render_kw={"class": "form-control p-2s",
                                 "placeholder": "Paste here the complete URL you want to shorten", 'autocomplete': "off"})
    expires_option = BooleanField(label='Do you want the link to expire?  ',
                                  render_kw={"onclick": "hide_show_expiration('date_local', '#expires_option')"})
    expire_time = DateTimeLocalField()
    custom_hash_option = BooleanField(label="Do you want to personalized the hash value?",
                                      render_kw={"onclick": "hide_show_expiration('personalized', '#custom_hash_option')"})
    custom_hash = StringField(validators=[Length(max=7)],
                              render_kw={"placeholder": "Custom name"})
    submit = SubmitField(label="Shorten",
                         render_kw={"class": "btn btn-success"})
