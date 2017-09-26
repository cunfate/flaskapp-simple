#!/usr/bin/env python

from flask import Flask, render_template, session, redirect, url_for
from flask import request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_FLASK')


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        # name = form.name.data
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index-test.html', name=session['name'], form=form)


@app.route('/hello')
def helloPage():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent


@app.route('/base')
def basePage():
    return render_template('base.html', title='Hello',
                           body='<p>I love you1</p>')


@app.route('/hello/<name>')
def helloname(name):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    manager.run()
