from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user

from NotesRepo import db
from NotesRepo.ctrla import Database
from NotesRepo.models import Note

notes = Blueprint("notes", __name__)
database = Database()


@notes.route("/notes_")
@login_required
def notes_():
    order_by = request.args.get("order_by", default="last_modified desc")
    return render_template("notes.html", order_by=order_by)


@notes.route("/favorites")
@login_required
def favorites():
    return render_template("favorites.html")


@notes.route("/note")
@login_required
def note():
    note_: Note = database.get(Note, int(request.args.get("id_")))

    return render_template("note.html", note=note_)


@notes.route("/note_create", methods=["POST"])
@login_required
def note_create():
    if request.args.get("id_"):
        id_ = int(request.args.get("id_"))
    else:
        id_ = None
    _ = Note(title=request.form["title"] or datetime.now().strftime("%F"),
             content="",
             folder_id=id_,
             date_created=datetime.now(),
             last_modified=datetime.now(),
             user_id=current_user.id)
    database.create(_)
    return redirect(url_for("notes.editor", id_=_.id))


@notes.route("/note_delete")
@login_required
def note_delete():
    _: Note = database.get(Note, int(request.args.get("id_")))
    database.delete(_)

    return redirect(request.referrer)


@notes.route("/note_favorite")
@login_required
def note_favorite():
    _: Note = database.get(Note, int(request.args.get("id_")))
    _.favorited = not _.favorited
    database.update()

    return redirect(request.referrer)


@notes.route("/editor", methods=["POST", "GET"])
@login_required
def editor():
    if request.method == "POST":
        note_: Note = database.get(Note, int(request.form["id_"]))
        if request.form["folder_id"]:
            folder_id = int(request.form["folder_id"])
        else:
            folder_id = None

        note_.title = request.form["title"]
        note_.folder_id = folder_id
        note_.content = request.form["content"]
        note_.last_modified = datetime.now()
        database.update()

        return redirect(request.referrer)
    else:
        id_ = int(request.args.get("id_"))
        note_: Note = database.get(Note, id_)

        return render_template("editor.html", note=note_)


@notes.route("/search", methods=["POST", "GET"])
@login_required
def search():
    if request.method == "POST":
        search_term = request.form["search_term"]
        results = db.session.query(Note).filter(Note.title.ilike(f"%{search_term}%"))

        return render_template("search.html", results=results, header="\"%s\"" % search_term)
