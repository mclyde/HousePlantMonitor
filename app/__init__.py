from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
CsrfProtect(app)
Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)

from app import views, models
