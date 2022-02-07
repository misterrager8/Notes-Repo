from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user

from NotesRepo import db
from NotesRepo.ctrla import Database
from NotesRepo.models import Note, Folder

notes = Blueprint("notes", __name__)
database = Database()


@notes.route("/notes_")
def notes_():
    order_by = request.args.get("order_by", default="last_modified desc")
    return render_template("notes.html", order_by=order_by)


@notes.route("/favorites")
def favorites():
    return render_template("favorites.html")


@notes.route("/note")
def note():
    note_: Note = database.get(Note, request.args.get("id_"))

    return render_template("note.html", note=note_)


@notes.route("/note_plain")
def note_plain():
    note_: Note = database.get(Note, request.args.get("id_"))

    return "<title>%s [PLAIN]</title><div style=\"white-space: pre-wrap;\">%s</div>" % (note_.title, note_.content)


@notes.route("/note_create", methods=["POST"])
@login_required
def note_create():
    folder_: Folder = database.get(Folder, request.args.get("id_"))

    _ = Note(title=request.form["title"],
             content="",
             folder_id=folder_.id,
             date_created=datetime.now(),
             last_modified=datetime.now(),
             user_id=current_user.id)
    database.create(_)
    return redirect(url_for("notes.editor", id_=_.id))


@notes.route("/note_delete")
@login_required
def note_delete():
    _: Note = database.get(Note, request.args.get("id_"))
    database.delete(_)

    return redirect(request.referrer)


@notes.route("/note_favorite")
@login_required
def note_favorite():
    _: Note = database.get(Note, request.args.get("id_"))
    _.favorited = not _.favorited
    database.update()

    return redirect(request.referrer)


@notes.route("/editor", methods=["POST", "GET"])
@login_required
def editor():
    if request.method == "POST":
        note_: Note = database.get(Note, int(request.form["id_"]))

        note_.title = request.form["title"]
        note_.folder_id = int(request.form["folder_id"])
        note_.content = request.form["content"]
        note_.last_modified = datetime.now()
        database.update()

        return redirect(request.referrer)
    else:
        id_ = request.args.get("id_")
        note_: Note = database.get(Note, id_)

        return render_template("editor.html", note=note_)


@notes.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_term = request.form["search_term"]
        results = db.session.query(Note).filter(Note.title.ilike(f"%{search_term}%"))

        return render_template("search.html", results=results, header="\"%s\"" % search_term)
