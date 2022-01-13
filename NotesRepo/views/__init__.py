from flask import request, url_for, render_template, current_app
from flask_login import login_user, logout_user
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from NotesRepo import db, login_manager
from NotesRepo.models import Folder, Page, Admin


@current_app.context_processor
def inject_recent():
    folders_ = db.session.query(Folder).order_by(text("date_created desc"))
    pages_ = db.session.query(Page).order_by(text("last_modified desc"))
    folders_count = db.session.query(Folder).order_by(text("date_created desc")).count()
    pages_count = db.session.query(Page).order_by(text("last_modified desc")).count()
    return dict(folders_=folders_, pages_=pages_, folders_count=folders_count, pages_count=pages_count)


@current_app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")

    return render_template("index.html",
                           folders_=db.session.query(Folder).order_by(text(order_by)).all(),
                           order_by=order_by)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Admin).get(int(user_id))


@current_app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_: Admin = db.session.query(Admin).filter_by(username=username).first()
        if user_ and check_password_hash(generate_password_hash(user_.password), password):
            login_user(user_)
            return redirect(url_for("index"))
        else:
            return "Login failed."


@current_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
