from flask import Blueprint, url_for, redirect, request, render_template
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from modules import db
from modules.model import User

users = Blueprint("users", __name__)


@users.route("/authors")
def authors():
    return render_template("users/authors.html", authors=db.session.query(User))


@users.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_: User = User.query.filter_by(username=username).first()
        if user_ and check_password_hash(generate_password_hash(user_.password), password):
            login_user(user_)
            return redirect(url_for("folders.index"))
        else:
            return "Login failed."


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("folders.index"))


@users.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db.session.add(User(username=username, password=password))
        db.session.commit()

        return redirect(url_for("folders.index"))
