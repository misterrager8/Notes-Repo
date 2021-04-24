from flask import render_template

from modules import app
from modules.ctrla import DB

page_db = DB()


@app.route("/")
def index():
    return render_template("index.html", pages=page_db.read_all())
