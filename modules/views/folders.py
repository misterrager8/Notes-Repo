import random

from flask import Blueprint, request, url_for, redirect, render_template
from sqlalchemy import text

from modules.ctrla import DB
from modules.model import Folder

folders = Blueprint("folders", __name__)
my_db = DB()


@folders.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")
    _ = my_db.read_all(Folder).order_by(text(order_by)).all()

    return render_template("folders/index.html", all_folders=_, order_by=order_by)


@folders.route("/add_folder", methods=["POST", "GET"])
def add_folder():
    if request.method == "POST":
        name = request.form["name"]
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        my_db.create(Folder(name, color))
        return redirect(url_for("folders.index"))


@folders.route("/delete_folder")
def delete_folder():
    id_ = request.args.get("id_")
    _: Folder = my_db.find_by_id(Folder, id_)
    my_db.delete(_)

    return redirect(url_for("folders.index"))


@folders.route("/edit_folder", methods=["POST", "GET"])
def edit_folder():
    id_ = request.args.get("id_")
    folder_: Folder = my_db.find_by_id(Folder, id_)

    if request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        folder_.edit_folder(name, color)

        return redirect(url_for("folders.index"))


@folders.route("/folder", methods=["POST", "GET"])
def folder():
    id_ = request.args.get("id_")
    folder_: Folder = my_db.find_by_id(Folder, id_)

    return render_template("folders/folder.html", folder=folder_)
