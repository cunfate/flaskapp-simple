from flask_wtf import Form
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, Email

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                            Email()])
    password = PasswordField('Password', validators=[Required()])
    remeber_me = BooleanField('remeber me')
    submit = SubmitField('Log in')
