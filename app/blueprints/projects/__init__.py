from flask import Blueprint

projects = Blueprint('projects', __name__, template_folder='templates/projects',static_folder='static')

from app.blueprints.projects import routes