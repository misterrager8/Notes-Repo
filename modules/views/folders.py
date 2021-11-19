import random
from datetime import datetime

from flask import Blueprint, request, redirect, render_template
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


@folders.route("/folder_create", methods=["POST"])
@login_required
def folder_create():
    db.session.add(Folder(name=request.form["name"].title(),
                          color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                          date_created=datetime.now()))
    db.session.commit()

    return redirect(request.referrer)


@folders.route("/folder_delete")
@login_required
def folder_delete():
    _: Folder = db.session.query(Folder).get(request.args.get("id_"))
    db.session.delete(_)
    db.session.commit()

    return redirect(request.referrer)


@folders.route("/folder_update", methods=["POST"])
@login_required
def folder_update():
    folder_: Folder = db.session.query(Folder).get(int(request.form["id_"]))

    folder_.name = request.form["name"]
    folder_.color = request.form["color"]
    folder_.description = request.form["description"]
    db.session.commit()

    return redirect(request.referrer)


@folders.route("/folder")
def folder():
    folder_: Folder = db.session.query(Folder).get(request.args.get("id_"))

    return render_template("folders/folder.html", folder=folder_)
