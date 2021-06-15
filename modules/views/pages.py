import re
from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy import text

from modules import db
from modules.model import Page, Folder, Source

pages = Blueprint("pages", __name__)


@pages.route("/all_pages", methods=["POST", "GET"])
def all_pages():
    order_by = request.args.get("order_by", default="last_modified desc")
    _ = db.session.query(Page).filter_by(is_draft=False).order_by(text(order_by)).join(Folder).all()

    return render_template("pages/all_pages.html", all_pages=_, order_by=order_by)


@pages.route("/page", methods=["POST", "GET"])
def page():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)

    return render_template("pages/page.html", page=page_)


@pages.route("/page_plain")
def page_plain():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)

    return render_template("pages/page_plain.html", page=page_)


@pages.route("/add_page", methods=["POST", "GET"])
def add_page():
    id_: int = request.args.get("id_")
    folder_: Folder = db.session.query(Folder).get(id_)

    if request.method == "POST":
        title = request.form["title"]
        is_draft = bool(request.form.get("is_draft"))

        _ = Page(title=title.title(), content="", is_draft=is_draft)
        folder_.pages.append(_)
        db.session.commit()
        return redirect(url_for("folders.folder", id_=folder_.id))

    return render_template("pages/add_page.html", folder=folder_)


@pages.route("/delete_page")
def delete_page():
    id_ = request.args.get("id_")
    _: Page = db.session.query(Page).get(id_)
    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("folders.folder", id_=folder_.id))


@pages.route("/edit_page", methods=["POST", "GET"])
def edit_page():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        page_.edit_page(title, content)

        return redirect(url_for("pages.page", id_=page_.id))

    return render_template("pages/edit_page.html", page=page_)


@pages.route("/mark")
def mark_page():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)

    page_.bookmarked = not page_.bookmarked
    db.session.commit()

    return redirect(request.referrer)


@pages.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_term = request.form["search_term"]
        results = db.session.query(Page).filter(Page.title.ilike(f"%{search_term}%"))

        return render_template("pages/search.html", results=results, header="\"%s\"" % search_term)


@pages.route("/drafts")
def drafts():
    return render_template("pages/drafts.html", drafts=db.session.query(Page).filter(Page.is_draft).all())


@pages.route("/bookmarks")
def bookmarks():
    return render_template("pages/bookmarks.html", bookmarks_=db.session.query(Page).filter(Page.bookmarked.is_(True)))


@pages.route("/sources")
def sources():
    name_regex = "[^]]+"
    url_regex = "http[s]?://[^)]+"
    markup_regex = "\[({0})]\(\s*({1})\s*\)".format(name_regex, url_regex)
    _ = []
    for i in db.session.query(Page).order_by(Page.title).all():
        for match in re.findall(markup_regex, i.content):
            _.append(Source(url=match[1], title=match[0], folders=i.folders, pages=i))

    return render_template("pages/sources.html", sources_=_)
