import random
from datetime import datetime

from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user

from NotesRepo.ctrla import Database
from NotesRepo.models import Folder

folders = Blueprint("folders", __name__)
database = Database()


@folders.route("/folder_create", methods=["POST"])
@login_required
def folder_create():
    database.create(Folder(name=request.form["name"],
                           color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                           date_created=datetime.now(),
                           user_id=current_user.id))

    return redirect(request.referrer)


@folders.route("/folder")
def folder():
    folder_: Folder = database.get(Folder, int(request.args.get("id_")))

    return render_template("folder.html", folder=folder_)


@folders.route("/folder_edit", methods=["POST"])
@login_required
def folder_edit():
    folder_: Folder = database.get(Folder, int(request.form["id_"]))

    folder_.name = request.form["name"]
    folder_.color = request.form["color"]
    database.update()

    return redirect(request.referrer)


@folders.route("/folder_delete")
@login_required
def folder_delete():
    _: Folder = database.get(Folder, int(request.args.get("id_")))
    database.delete_multiple([i for i in _.get_notes()])
    database.delete(_)

    return redirect(request.referrer)
