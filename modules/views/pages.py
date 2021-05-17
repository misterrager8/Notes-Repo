from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy import text

from modules.ctrla import DB
from modules.model import Page, Folder, Draft

pages = Blueprint("pages", __name__)
my_db = DB()


@pages.route("/all_pages", methods=["POST", "GET"])
def all_pages():
    order_by = request.args.get("order_by", default="last_modified desc")
    _ = my_db.read_all(Page).order_by(text(order_by)).join(Folder).all()

    return render_template("pages/all_pages.html", all_pages=_, order_by=order_by)


@pages.route("/page", methods=["POST", "GET"])
def page():
    id_ = request.args.get("id_")
    page_: Page = my_db.find_by_id(Page, id_)

    return render_template("pages/page.html", page=page_)


@pages.route("/page_plain")
def page_plain():
    id_ = request.args.get("id_")
    page_: Page = my_db.find_by_id(Page, id_)

    return render_template("pages/page_plain.html", page=page_)


@pages.route("/add_page", methods=["POST", "GET"])
def add_page():
    id_: int = request.args.get("id_")
    folder_: Folder = my_db.find_by_id(Folder, id_)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        folder_.add_page(Page(title, content))
        return redirect(url_for("folders.folder", id_=folder_.id))

    return render_template("pages/add_page.html", folder=folder_)


@pages.route("/delete_page")
def delete_page():
    id_ = request.args.get("id_")
    _: Page = my_db.find_by_id(Page, id_)
    folder_ = _.folders
    my_db.delete(_)

    return redirect(url_for("folders.folder", id_=folder_.id))


@pages.route("/edit_page", methods=["POST", "GET"])
def edit_page():
    id_ = request.args.get("id_")
    page_: Page = my_db.find_by_id(Page, id_)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        page_.edit_page(title, content)

        return redirect(url_for("pages.page", id_=page_.id))

    return render_template("pages/edit_page.html", page=page_)


@pages.route("/mark")
def mark_page():
    id_ = request.args.get("id_")
    page_: Page = my_db.find_by_id(Page, id_)

    page_.toggle_marked()

    return redirect(request.referrer)


@pages.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_term = request.form["search_term"]
        results = my_db.read_all(Page).filter(Page.title.ilike(f"%{search_term}%"))

        return render_template("pages/search.html", results=results, header="\"%s\"" % search_term)


@pages.route("/drafts")
def drafts():
    _ = my_db.read_all(Draft).all()
    return render_template("pages/drafts.html", drafts=_)


@pages.route("/bookmarks")
def bookmarks():
    _ = my_db.read_all(Page).filter(Page.bookmarked.is_(True))
    return render_template("pages/bookmarks.html", bookmarks_=_)
