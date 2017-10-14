from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remeber_me = BooleanField('remeber me')
    submit = SubmitField('Log in')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                           'username cannot have charater excpet letters'
                           )
    ])

    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='password verfiy failed!')
    ])

    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        print('validating email %s\n' %field.data)
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        print('validating username: %s\n' % field.data)
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')
