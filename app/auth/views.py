from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db
from ..email import send_email, send_mail_smtp
from flask import current_app


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
@login_required
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
        token = user.generate_confirm_token()
        print(user.email + ' is sending target')
        try:
            send_mail_smtp(user.email, 'Confirm your account - flaskapp',
                            'auth/email/confirm', user=user, token=token)
        except Exception as e:
            print(e)
            # db.session.delete(user)
            flash('send email fail!')
            flash(url_for('auth.confirm', token=token, _external=True))
            return redirect(url_for('auth.login'))
        flash('a confirmation email has been sent to your email address')
        flash('Now you can login')
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account! thanks!')
    else:
        flash('The confirmation url is invalid.')
    return redirect(url_for('main.index'))
