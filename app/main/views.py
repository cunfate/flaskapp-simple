from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, abort
from flask import request, make_response, current_app, jsonify, Response
from flask_login import current_user, login_required
from werkzeug import secure_filename
from PIL import Image
import os
import json

from . import main
from .forms import EditProfileForm, PostForm, CommentForm, AvatarForm
from .. import db
from ..models import User, Permission, Post, Comment
from ..decorators import permission_required
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
            page,
            per_page=20,
            error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           show_followed=show_followed,
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


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('You comment has been published')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / 20 + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=20, error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return url_for('.index')
    if current_user.is_following(user):
        flash('You are already followed this user')
        return redirect(url_for('.user_page', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user_page', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user!')
        return url_for('.index')
    if user.is_followed_by(current_user):
        flash('You do not following this user!')
        return redirect(url_for('.user_page', username=username))
    current_user.unfollow(user)
    flash('You unfollowed %s' % username)
    return redirect(url_for('.user_page', username=username))


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('Your post has been updated!')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=20, error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('follows.html', user=user, title='Follows of',
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=20, error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('follows.html', user=user, title='Followed by',
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    form = AvatarForm()
    if form.validate_on_submit():
        f = form.avatar.data
        filename = secure_filename(f.filename)
        f.save(
            os.path.join(
                './app/static/' + current_app.config['AVATAR_PATH'],
                str(current_user.id) +
                os.path.splitext(filename)[-1]
            )
        )
        current_user.set_avatar_url(
            os.path.join(
                current_app.config['AVATAR_PATH'], str(current_user.id) +
                os.path.splitext(filename)[-1]
            )
        )
        return redirect(url_for('.user_page', username=current_user.username))
    return render_template('upavatar.html', form=form)


@main.route('/avatarcrop', methods=['GET', 'POST'])
@login_required
def crop_avtar():
    if request.accept_mimetypes.accept_json:
        path = os.path.join('./app/static/', current_user.get_avatar_url())
        img = Image.open(path)
        local = (request.json)
        crop_box = (local['x'], local['y'],
                        local['x2'], local['y2'])
        region = img.crop(crop_box)
        region.save(path)
        return '{"a":true}'


@main.route('/avatarnew', methods=['POST'])
@login_required
def crop_avtar_new():
    if request.accept_mimetypes.accept_json:
        print(request.data)
        print('files:')
        print(request.files)
        print('values:')
        a = request.form['area']
        print(a)
        r = Response(response='{"success": true}', status=200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json; charset=utf-8"
        return r


@main.route('/avatarnew', methods=['GET'])
@login_required
def change_avatar_new():
    return render_template("upavatarnew.html");
