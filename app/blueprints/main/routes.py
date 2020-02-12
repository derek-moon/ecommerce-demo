from app import  db
from flask import current_app, render_template, redirect, url_for, flash
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.account.forms import BlogForm

from app.blueprints.main import main
import requests 

@main.route('/', methods=['GET','POST'])
@login_required

def index():
    form = BlogForm()
    context = {
        'form':form,
        #current_user.followed_posts()
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
@login_required
def users():
    context = {
        'users':[i for i in User.query.all() if i.id != current_user.id]
    }
    return render_template('users.html', **context)

#<user> passed in HTML href=""
@main.route('/users/add/<user>')
@login_required
def users_add(user):
    user = User.query.filter_by(name=user).first()
    if user not in current_user.followed:
        flash("User followed successfully", "success")
        current_user.follow(user)
        return redirect(url_for('main.users'))
    flash(f"You are already following {user.name}", "warning")
    return redirect(url_for('main.users'))
    
@main.route('/users/remove/<user>')
@login_required
def users_remove(user):
    user = User.query.filter_by(name=user).first()
    if user in current_user.followed:
        current_user.unfollow(user)
        flash("User unfollowed successfully", "warning")
        return redirect(url_for('main.users'))
    flash(f"You are not following {user.name}", "danger")
    return redirect(url_for('main.users'))

@main.route('/users/delete/<user>')
@login_required
def users_delete(user):
    user = current_user
    db.session.delete(user)
    db.session.commit()
    flash("Your was deleted", "success")
    return redirect(url_for('main.index'))
