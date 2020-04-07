# Python standard libraries
import json
import sqlite3
import os

# Third party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
#from db import init_db_command
#from user import User
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    login_manager.init_app(app)

    GOOGLE_CLIENT_ID ='856122308427-29ccsisqdr637u58u4k2dmoo5aom68df.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'YjwznTE9_1qaccXUFxiUO4L2'
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    # OAuth2 client setup
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    db.init_app(app)
    migrate.init_app(app, db)

    app.jinja_env.filters['date_filter'] = date_filter
    
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.app)
        return app

  

def date_filter(date):
    return date.strftime('%m-%d-%Y')
    







