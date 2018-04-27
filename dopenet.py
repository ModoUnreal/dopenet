from app import app, db
from app.models import User, Post, Comment, Topic
from waitress import serve

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment, 'Topic': Topic}

if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)
