from flask import render_template
from app.forms import LoginForm
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'ModoUnreal'}

    posts = [
            
            {
                'author': {'username': 'Captain Swiggles'},
                'body': 'Hey this is me, just checkin out..'
            }
            
            ]

    return render_template('index.html', title='Dopenet: You can do anything', user=user, posts=posts)

@app.route('/login')
def login():
    loginform = LoginForm()
    return render_template('login.html', title='Login to Dopenet', form=loginform)
