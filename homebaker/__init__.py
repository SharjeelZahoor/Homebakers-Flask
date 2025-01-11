# homebaker/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize the Flask app
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# Configurations
app.debug = True
UPLOAD_FOLDER = os.path.join(basedir, 'static', 'img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "abc1234"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "database/homebaker.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration objects
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes and models to avoid circular imports
from homebaker import routes
from homebaker import models
