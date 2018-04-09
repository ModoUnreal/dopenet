from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    username = "ModoUnreal"
    return render_template('base.html', title='Dopenet: You can do anything', username=username)
