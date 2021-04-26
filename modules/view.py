from flask import render_template, request, redirect, url_for

from modules import app
from modules.ctrla import DB
from modules.model import Page, Folder

my_db = DB()


@app.context_processor
def inject_folders():
    _ = my_db.read_all(Folder)
    return dict(folders=_)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_page", methods=["POST", "GET"])
def add_page():
    id_: int = request.args.get("id_")
    folder_: Folder = my_db.find_by_id(Folder, id_)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        folder_.add_page(Page(title, content))
        return redirect(url_for("folder", id_=folder_.id))

    return render_template("add_page.html", folder=folder_)


@app.route("/add_folder", methods=["POST", "GET"])
def add_folder():
    if request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]

        my_db.create(Folder(name, color))
        return redirect(url_for("index"))


@app.route("/edit_page", methods=["POST", "GET"])
def edit_page():
    id_ = request.args.get("id_")
    page: Page = my_db.find_by_id(Page, id_)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        page.edit_page(title, content)

        return redirect(url_for("folder", id_=page.folder_id))

    return render_template("edit_page.html", page=page)


@app.route("/delete_page")
def delete_page():
    id_ = request.args.get("id_")
    _: Page = my_db.find_by_id(Page, id_)
    folder_ = _.folders
    my_db.delete(_)

    return redirect(url_for("folder", id_=folder_.id))


@app.route("/folder", methods=["POST", "GET"])
def folder():
    id_ = request.args.get("id_")
    folder_: Folder = my_db.find_by_id(Folder, id_)

    return render_template("folder.html", folder=folder_)


@app.route("/doc", methods=["POST", "GET"])
def doc():
    id_ = request.args.get("id_")
    page: Page = my_db.find_by_id(Page, id_)

    return render_template("doc.html", page=page)


@app.route("/doc_plain")
def doc_plain():
    id_ = request.args.get("id_")
    page: Page = my_db.find_by_id(Page, id_)

    return render_template("doc_plain.html", page=page)
