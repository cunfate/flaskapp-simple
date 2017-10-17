from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, abort

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    # username = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if(user is None):
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['Known'] = False
        else:
            session['Known'] = True
            # username = user
        # name = form.name.data
        oldName = session.get('name')
        if oldName is not None and oldName != form.name.data:
            flash('looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index-test.html')


@main.route('/admin')
@admin_required
def for_admins_only():
    return 'For admins only!'


@main.route('/user/<username>')
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
