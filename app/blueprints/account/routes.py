from app import db
from flask import render_template, redirect, url_for, flash, request
from app.models import User, Post
from app.blueprints.account.forms import LoginForm, RegistrationForm, ProfileForm, BlogForm
from flask_login import login_user, logout_user, login_required, current_user, login_required

from app.blueprints.account import account

@account.route('/about',methods=['GET','POST'])
@login_required
def about():
    form = ProfileForm()
    context ={
        'form':form
    }
    if request.method == 'GET':
        form.name.data = current_user.name 
        form.email.data = current_user.email
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.password = form.password.data
        current_user.generate_password(current_user.password)
        db.session.commit()
        flash("Profile information updated successfully","success")
        return redirect(url_for('account.about'))


    return render_template('about.html',**context)

@account.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    p = Post.query.get(id)
    db.session.delete(p)
    db.session.commit()
    flash("Post deleted successfully","info")
    return redirect(url_for('account.profile',id=current_user.id))

@account.route('/profile/<int:id>',methods=['GET','POST'])
@login_required
def profile(id):
    form = BlogForm()
    if form.validate_on_submit():
        p = Post(body=form.body.data, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash("Post added succesfully!", 'success')
        return redirect(url_for('account.profile',id=id))
    context = {
        'form':form,
        'posts': Post.query.filter_by(user_id=id).order_by(Post.timestamp.desc()).all()
    }
    return render_template('profile.html', **context)



@account.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    context = {
        'form':form
    }
    if form.validate_on_submit():
        #returns a generator
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid Credentials. Please try again","danger")
            return redirect(url_for('account.login'))
        
        flash("You have logged in successfully","success")
        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('login.html', **context)

@account.route('/register', methods=['GET','POST'])
def register():
    #form class from forms.py 
    form = RegistrationForm()
    if form.validate_on_submit():
        #u is the object 
        u = User(name=form.name.data, email=form.email.data)

        #calling gen_pass function in models.py in user Class
        u.generate_password(form.password.data)

        #sqlalchemy commands
        db.session.add(u)
        db.session.commit()
        flash("You have registered successfully","success")
        return redirect(url_for('account.login'))
    else:
        flash("Email already in use ","danger")
        return redirect(url_for('account.login'))
    context = {
        'form':form
    }
    return render_template('register.html', **context)

@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully loggedd out","Primary")
    return redirect(url_for('account.login'))