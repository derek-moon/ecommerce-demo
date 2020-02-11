from app import create_app, db
from app.models import User, Post

app = create_app()

@app.shell_context_processor
def get_context():
    return dict(User = User, app=app, db=db, Post=Post)