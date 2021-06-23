import random

from flask import Blueprint, request, url_for, redirect, render_template
from flask_login import current_user
from sqlalchemy import text

from modules import db
from modules.model import Folder, Page

folders = Blueprint("folders", __name__)


@folders.route("/")
def index():
    return render_template("folders/index.html",
                           featured_folders=db.session.query(Folder).order_by(text("date_created desc")).all(),
                           featured_pages=db.session.query(Page).order_by(text("last_modified desc")).filter_by(is_draft=False).all())


@folders.route("/my_folders", methods=["POST", "GET"])
def my_folders():
    order_by = request.args.get("order_by", default="date_created desc")
    _ = current_user.folders.order_by(text(order_by)).all()

    return render_template("folders/my_folders.html", my_folders=_, order_by=order_by)


@folders.route("/add_folder", methods=["POST", "GET"])
def add_folder():
    if request.method == "POST":
        name = request.form["name"]
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        db.session.add(Folder(name=name.title(), color=color, users=current_user))
        db.session.commit()
        return redirect(url_for("folders.my_folders"))


@folders.route("/delete_folder")
def delete_folder():
    id_ = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)
    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("folders.my_folders"))


@folders.route("/edit_folder", methods=["POST", "GET"])
def edit_folder():
    id_ = request.args.get("id_")
    folder_: Folder = db.session.query(Folder).get(id_)

    if request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]

        folder_.name = name.title()
        folder_.color = color
        db.session.commit()

        return redirect(url_for("folders.my_folders"))


@folders.route("/folder", methods=["POST", "GET"])
def folder():
    id_ = request.args.get("id_")
    folder_: Folder = db.session.query(Folder).get(id_)
    public_pages = db.session.query(Page).filter_by(folder_id=folder_.id, is_draft=False).all()
    private_pages = db.session.query(Page).filter_by(folder_id=folder_.id, is_draft=True).all()

    return render_template("folders/folder.html",
                           folder=folder_,
                           public_pages=public_pages,
                           private_pages=private_pages)
