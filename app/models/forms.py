# forms.py

from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired


class LoginForm(Form):
	email = StringField('email', validators=[DataRequired()])
	senha = PasswordField('senha',  validators=[DataRequired()])
	remember_me = BooleanField('remember_me')