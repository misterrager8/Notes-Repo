import os

import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("db_url")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 60}
DEBUG = os.getenv("debug")
ENV = os.getenv("env")
