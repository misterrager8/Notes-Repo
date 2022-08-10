import pymysql
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from NotesRepo.views.folders import folders
        from NotesRepo.views.notes import notes

        app.register_blueprint(folders)
        app.register_blueprint(notes)

        # db.drop_all()
        db.create_all()

        return app
