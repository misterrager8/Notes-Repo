from datetime import datetime
from bs4 import BeautifulSoup
import html2text


from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    send_from_directory,
    current_app,
)
from flask_login import login_required, current_user

from NotesRepo import db
from NotesRepo.ctrla import Database
from NotesRepo.models import Note
import requests

notes = Blueprint("notes", __name__)
database = Database()


@notes.route("/note")
@login_required
def note():
    note_: Note = database.get(Note, int(request.args.get("id_")))

    return render_template("note.html", note=note_)


@notes.route("/note_create", methods=["POST"])
@login_required
def note_create():

    if request.form["folder_id"]:
        id_ = int(request.form["folder_id"])
    else:
        id_ = None

    _ = Note(
        title=request.form["title"] or "%s" % datetime.now().strftime("%F %T"),
        folder_id=id_,
        content="",
        date_created=datetime.now(),
        last_modified=datetime.now(),
        user_id=current_user.id,
    )
    database.create(_)
    return redirect(url_for("notes.editor", id_=_.id))


@notes.route("/note_create_from_url", methods=["POST"])
@login_required
def note_create_from_url():
    soup = BeautifulSoup(requests.get(request.form["url"]).text, "html.parser")

    if request.form["folder_id"]:
        id_ = int(request.form["folder_id"])
    else:
        id_ = None

    note_ = Note(
        title=soup.find("title").get_text(),
        folder_id=id_,
        content=html2text.html2text(str(soup)),
        date_created=datetime.now(),
        last_modified=datetime.now(),
        user_id=current_user.id,
    )
    database.create(note_)

    return redirect(url_for("notes.editor", id_=note_.id))


@notes.route("/note_delete")
@login_required
def note_delete():
    _: Note = database.get(Note, int(request.args.get("id_")))
    id_ = _.folder_id
    database.delete(_)

    return redirect(url_for("folders.folder", id_=id_))


@notes.route("/note_download", methods=["GET", "POST"])
@login_required
def note_download():
    _: Note = database.get(Note, int(request.args.get("id_")))
    full_path = "%s/%s.md" % (current_app.root_path, _.title)

    with open(full_path, "w") as f:
        f.write(_.content)

    return send_from_directory(directory=current_app.root_path, path="%s.md" % _.title)


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
        note_: Note = database.get(Note, int(request.args.get("id_")))
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

        return render_template(
            "search.html", results=results, header='"%s"' % search_term
        )
