from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been log out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Now you can login')
        return redirect(url_for(auth.login))
    return render_template('auth/register.html', form=form)
