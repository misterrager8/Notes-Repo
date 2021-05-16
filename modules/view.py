import random

import requests
from bs4 import BeautifulSoup
from flask import render_template, request, redirect, url_for
from sqlalchemy import text

from modules import app
from modules.ctrla import DB
from modules.model import Page, Folder, Link, Draft

my_db = DB()


# --FOLDER FNS--

@app.context_processor
def inject_folders():
    recent_folders = my_db.read_all(Folder).order_by(text("date_created desc"))[:5]
    recent_pages = my_db.read_all(Page).order_by(text("last_modified desc"))[:5]
    return dict(recent_folders=recent_folders, recent_pages=recent_pages)


@app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")
    _ = my_db.read_all(Folder).order_by(text(order_by)).all()

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
    _ = my_db.read_all(Page).order_by(text(order_by)).join(Folder).all()

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

        return redirect(url_for("page", id_=page_.id))

    return render_template("edit_page.html", page=page_)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_term = request.form["search_term"]
        results = my_db.read_all(Page).filter(Page.title.ilike(f"%{search_term}%"))

        return render_template("search.html", results=results, header="\"%s\"" % search_term)


@app.route("/drafts")
def drafts():
    _ = my_db.read_all(Draft).all()
    return render_template("drafts.html", drafts=_)


@app.route("/bookmarks")
def bookmarks():
    _ = my_db.read_all(Page).filter(Page.bookmarked.is_(True))
    return render_template("bookmarks.html", bookmarks_=_)


@app.route("/links", methods=["POST", "GET"])
def links():
    if request.method == "POST":
        url = request.form["url"]
        title = BeautifulSoup(requests.get(url).content, "html.parser").find("title").string

        my_db.create(Link(url, title))
        return redirect(url_for("links"))

    return render_template("links.html", links=my_db.read_all(Link).order_by(text("date_added desc")).all())


@app.route("/delete_link")
def delete_link():
    id_ = request.args.get("id_")
    link = my_db.find_by_id(Link, id_)

    my_db.delete(link)
    return redirect(url_for("links"))


@app.route("/edit", methods=["POST"])
def edit_link():
    if request.method == "POST":
        id_ = request.args.get("id_")
        link = my_db.find_by_id(Link, id_)
        title = request.form["title_"]

        link.set_title(title)

        return redirect(url_for("links"))


@app.route("/mark")
def mark_page():
    id_ = request.args.get("id_")
    page_: Page = my_db.find_by_id(Page, id_)

    page_.toggle_marked()

    return redirect(request.referrer)
