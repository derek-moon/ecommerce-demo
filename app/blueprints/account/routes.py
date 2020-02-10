from app import db
from flask import render_template, redirect, url_for, flash
from app.models import User
from app.blueprints.account.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required

from app.blueprints.account import account

@account.route('/profile')
def profile():
    context = dict(
        username='Derek_codingtemple',
        email="Derek_h@codingtemple.com"
    )
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