from flask import Flask, render_template

from modules.ctrla import JsonCtrla

app = Flask(__name__)
notes = JsonCtrla().get_all()


@app.route("/")
def index():
    return render_template("index.html", notes=notes)
