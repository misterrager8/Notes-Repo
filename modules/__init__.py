import os

import dotenv
import pymysql
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()
app = Flask(__name__)

dotenv.load_dotenv()

db_host = os.getenv("host")
db_user = os.getenv("user")
db_pass = os.getenv("passwd")
db_name = os.getenv("db")

secret_key = os.getenv("secret_key")

app.config['SECRET_KEY'] = secret_key

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_pass}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100, 'pool_recycle': 280}

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

from modules.views.folders import folders
from modules.views.pages import pages

app.register_blueprint(folders)
app.register_blueprint(pages)
