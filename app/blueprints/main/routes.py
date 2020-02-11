from app import  db
from flask import current_app, render_template, redirect, url_for, flash
from app.models import User
from flask_login import login_user, logout_user

from app.blueprints.main import main
import requests 

@main.route('/')
def index():
    
    return render_template('index.html')


@main.route('/students')
def students():
    context = {
        'students': ["abiola", "michael", "Derek"]
    }
    return render_template('students.html', **context)
