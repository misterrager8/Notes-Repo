import random

from flask import Blueprint, request, url_for, redirect, render_template
from flask_login import login_required
from sqlalchemy import text

from modules import db
from modules.model import Folder

folders = Blueprint("folders", __name__)


@folders.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")

    return render_template("folders/index.html",
                           folders_=db.session.query(Folder).order_by(text(order_by)).all(),
                           order_by=order_by)


@folders.route("/add_folder", methods=["POST", "GET"])
@login_required
def add_folder():
    if request.method == "POST":
        name = request.form.getlist("name")

        for i in name:
            db.session.add(Folder(name=i.title(), color="#{:06x}".format(random.randint(0, 0xFFFFFF))))

        db.session.commit()

        return redirect(url_for("folders.index"))


@folders.route("/delete_folder")
@login_required
def delete_folder():
    id_ = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)
    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("folders.index"))


@folders.route("/edit_folder", methods=["POST", "GET"])
@login_required
def edit_folder():
    id_ = request.args.get("id_")
    folder_: Folder = db.session.query(Folder).get(id_)

    if request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        description = request.form["description"]

        folder_.name = name.title()
        folder_.color = color
        folder_.description = description
        db.session.commit()

        return redirect(url_for("folders.index"))


@folders.route("/folder", methods=["POST", "GET"])
def folder():
    id_ = request.args.get("id_")
    folder_: Folder = db.session.query(Folder).get(id_)

    return render_template("folders/folder.html",
                           folder=folder_)
