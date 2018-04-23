from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'

from app import routes, models, errors

# Deal with any blueprints here.
from .auth import api as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
