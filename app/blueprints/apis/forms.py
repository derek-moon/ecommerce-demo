from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, EqualTo, DataRequired


class PokedexForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    submit = SubmitField('Submit')


