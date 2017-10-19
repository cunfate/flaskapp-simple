from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, abort
from flask import request
from flask_login import current_user, login_required

from . import main
from .forms import EditProfileForm, PostForm
from .. import db
from ..models import User, Permission, Post
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # # username = None
    # if form.validate_on_submit():
        # user = User.query.filter_by(username=form.name.data).first()
        # if(user is None):
            # user = User(username=form.name.data)
            # db.session.add(user)
            # db.session.commit()
            # session['Known'] = False
        # else:
            # session['Known'] = True
            # # username = user
        # # name = form.name.data
        # oldName = session.get('name')
        # if oldName is not None and oldName != form.name.data:
            # flash('looks like you have changed your name!')
        # session['name'] = form.name.data
        # return redirect(url_for('.index'))
    # return render_template('index-test.html')
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=10, error_out=False
    )
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination)


@main.route('/admin')
@admin_required
def for_admins_only():
    return 'For admins only!'


@main.route('/user/<username>')
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been upadated.')
        return redirect(url_for('.user_page', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
