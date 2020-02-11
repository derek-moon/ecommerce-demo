from app import  db
from flask import current_app, render_template, redirect, url_for, flash
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.account.forms import BlogForm

from app.blueprints.main import main
import requests 

@main.route('/', methods=['GET','POST'])
def index():
    form = BlogForm()
    context = {
        'form':form,
        'posts':Post.query.order_by(Post.timestamp.desc()).all()
    }
    if form.validate_on_submit():
        p = Post(body=form.body.data, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash("Post added succesfully!", 'success')
        return redirect(url_for('main.index'))
    return render_template('index.html', **context)

@main.route('/users')
def users():
    context = {
        'users':User.query.all()
    }
    return render_template('users.html', **context)
