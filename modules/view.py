from flask import Flask, render_template

from modules.ctrla import NoteDB

app = Flask(__name__)
notes = NoteDB().get_all()


@app.route("/")
def index():
    return render_template("index.html", notes=notes)


@app.route("/notes/<title>")
def note_pg(note):
    return render_template("note_page.html", note=note)
