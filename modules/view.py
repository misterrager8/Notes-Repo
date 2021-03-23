from flask import render_template, redirect, url_for

from modules import app
from modules.ctrla import NoteDB

note_db = NoteDB()
notes = note_db.get_all()


@app.route("/")
def index():
    return render_template("index.html", notes=notes)


@app.route("/notes/<note_id>")
def note_pg(note_id: int):
    note = note_db.find_by_id(note_id)
    return render_template("note_page.html", note=note)


@app.route("/save/<note_id>")
def save(note_id: int):
    note = note_db.find_by_id(note_id)
    note.save()
    return redirect(url_for("note_pg", note_id=note_id))
