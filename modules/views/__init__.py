from flask import request, url_for
from flask_login import login_user, logout_user
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from modules import app, db, login_manager
from modules.model import Folder, Page, Admin


@app.context_processor
def inject_recent():
    folders_ = db.session.query(Folder).order_by(text("date_created desc"))
    pages_ = db.session.query(Page).order_by(text("last_modified desc"))
    return dict(folders_=folders_, pages_=pages_)


@current_app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")

    return render_template("index.html",
                           folders_=db.session.query(Folder).order_by(text(order_by)).all(),
                           order_by=order_by)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Admin).get(int(user_id))


@app.route("/login", methods=["POST"])
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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
