#!/usr/bin/env python

from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm as Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import os
basedir = os.path.abspath(os.path.dirname(__file__))
mysql_username = os.getenv('MYSQL_USERNAME')
mysql_pwd = os.getenv('MYSQL_PWD_FLASK')

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_FLASK')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://%s:%s@127.0.0.1/flaskapp?charset=utf8'\
    % (mysql_username, mysql_pwd)
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if(user is None):
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['Known'] = False
        else:
            session['Known'] = True
        # name = form.name.data
        oldName = session.get('name')
        if oldName is not None and oldName != form.name.data:
            flash('looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index-test.html',
                           name=session.get('name'), form=form,
                           known=session.get('Known'))


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


def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
