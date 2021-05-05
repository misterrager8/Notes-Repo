import random

from flask import render_template, request, redirect, url_for
from sqlalchemy import text

from modules import app
from modules.ctrla import DB
from modules.model import Page, Folder

my_db = DB()


# --FOLDER FNS--

@app.context_processor
def inject_folders():
    folders = my_db.read_all(Folder)
    pages = my_db.read_all(Page)
    return dict(folders=folders, pages=pages)


@app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")
    _ = my_db.read_all(Folder).order_by(text(order_by))

    return render_template("index.html", all_folders=_, order_by=order_by)


@app.route("/add_folder", methods=["POST", "GET"])
def add_folder():
    if request.method == "POST":
        name = request.form["name"]
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        my_db.create(Folder(name, color))
        return redirect(url_for("index"))


@app.route("/delete_folder")
def delete_folder():
    id_ = request.args.get("id_")
    _: Folder = my_db.find_by_id(Folder, id_)
    my_db.delete(_)

    return redirect(url_for("index"))


@app.route("/edit_folder", methods=["POST", "GET"])
def edit_folder():
    id_ = request.args.get("id_")
    folder_: Folder = my_db.find_by_id(Folder, id_)

    if request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        folder_.edit_folder(name, color)

        return redirect(url_for("index"))


@app.route("/folder", methods=["POST", "GET"])
def folder():
    id_ = request.args.get("id_")
    folder_: Folder = my_db.find_by_id(Folder, id_)

    return render_template("folder.html", folder=folder_)


# --PAGE FNS--


@app.route("/all_pages", methods=["POST", "GET"])
def all_pages():
    order_by = request.args.get("order_by", default="last_modified desc")
    _ = my_db.read_all(Page).order_by(text(order_by)).join(Folder)

    return render_template("all_pages.html", all_pages=_, order_by=order_by)


@app.route("/page", methods=["POST", "GET"])
def page():
    id_ = request.args.get("id_")
    page_: Page = my_db.find_by_id(Page, id_)

    return render_template("page.html", page=page_)


@app.route("/page_plain")
def page_plain():
    id_ = request.args.get("id_")
    page_: Page = my_db.find_by_id(Page, id_)

    return render_template("page_plain.html", page=page_)


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


@app.route("/delete_page")
def delete_page():
    id_ = request.args.get("id_")
    _: Page = my_db.find_by_id(Page, id_)
    folder_ = _.folders
    my_db.delete(_)

    return redirect(url_for("folder", id_=folder_.id))


@app.route("/edit_page", methods=["POST", "GET"])
def edit_page():
    id_ = request.args.get("id_")
    page_: Page = my_db.find_by_id(Page, id_)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        page_.edit_page(title, content)

        return redirect(url_for("folder", id_=page_.folder_id))

    return render_template("edit_page.html", page=page_)
