from flask import request, url_for, render_template, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from NotesRepo import login_manager
from NotesRepo.ctrla import Database
from NotesRepo.models import User

database = Database()


@current_app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("index.html", order_by=order_by)


@login_manager.user_loader
def load_user(id_: int):
    return database.get(User, id_)


@current_app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user_: User = User.query.filter_by(username=username).first()
    if user_ and check_password_hash(user_.password, password):
        login_user(user_)
        return redirect(url_for("index"))
    else:
        return "Login failed."


@current_app.route("/signup", methods=["POST"])
def signup():
    _ = User(
        username=request.form["username"],
        password=generate_password_hash(request.form["password"]),
    )

    database.create(_)
    login_user(_)
    return redirect(url_for("index"))


@current_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@current_app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "GET":
        return render_template("account.html")
    else:
        current_user.username = request.form["username"]
        database.update()
        return redirect(request.referrer)


@current_app.route("/change_password", methods=["POST"])
def change_password():
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]
    new_password_confirm = request.form["new_password_confirm"]

    if (
        check_password_hash(current_user.password, old_password)
        and new_password == new_password_confirm
    ):
        current_user.password = generate_password_hash(new_password)
        database.update()
    else:
        return "Try again."

    return redirect(request.referrer)
