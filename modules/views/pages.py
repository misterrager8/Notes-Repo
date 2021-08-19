import os.path
from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for, send_from_directory
from flask_login import login_required
from sqlalchemy import text

from modules import db, app
from modules.model import Page, Folder

pages = Blueprint("pages", __name__)


@pages.route("/my_pages", methods=["POST", "GET"])
def my_pages():
    order_by = request.args.get("order_by", default="last_modified desc")
    _ = db.session.query(Page).join(Folder).order_by(text(order_by))

    return render_template("pages/my_pages.html", all_pages=_, order_by=order_by)


@pages.route("/page", methods=["POST", "GET"])
def page():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)

    return render_template("pages/page.html", page=page_)


@pages.route("/page_plain")
def page_plain():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)

    return "<title>%s [PLAIN]</title><div style=\"white-space: pre-wrap;\">%s</div>" % (page_.title, page_.content)


@pages.route("/download")
def download():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)
    full_path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])

    with open(f"{full_path}/{page_.title}.md", "w") as f:
        f.write(page_.content)

    f.close()

    return send_from_directory(full_path, f"{page_.title}.md")


@pages.route("/add_page", methods=["POST", "GET"])
@login_required
def add_page():
    id_: int = request.args.get("id_")
    folder_: Folder = db.session.query(Folder).get(id_)

    if request.method == "POST":
        title = request.form["title"].title()

        _ = Page(title=title.title(), content="", folders=folder_)
        db.session.commit()
        return redirect(url_for("pages.editor", id_=_.id))


@pages.route("/delete_page")
@login_required
def delete_page():
    id_ = request.args.get("id_")
    _: Page = db.session.query(Page).get(id_)
    db.session.delete(_)
    db.session.commit()

    return redirect(request.referrer)


@pages.route("/editor", methods=["POST", "GET"])
@login_required
def editor():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)

    if request.method == "POST":
        title = request.form["title"]
        folder_id: int = request.form.get("folder_id")
        content = request.form["content"]

        page_.title = title
        page_.folder_id = folder_id
        page_.content = content
        page_.last_modified = datetime.now()

        db.session.commit()

        return redirect(url_for("pages.editor", id_=page_.id))

    return render_template("pages/editor.html", page=page_)


@pages.route("/mark")
@login_required
def mark_page():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)

    page_.bookmarked = not page_.bookmarked
    db.session.commit()

    return redirect(request.referrer)


@pages.route("/page_visibility")
@login_required
def page_visibility():
    id_ = request.args.get("id_")
    page_: Page = db.session.query(Page).get(id_)

    page_.visible = not page_.visible
    db.session.commit()

    return redirect(request.referrer)


@pages.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_term = request.form["search_term"]
        results = db.session.query(Page).filter(Page.title.ilike(f"%{search_term}%"))

        return render_template("pages/search.html", results=results, header="\"%s\"" % search_term)


@pages.route("/bookmarks")
@login_required
def bookmarks():
    return render_template("pages/bookmarks.html", bookmarks_=db.session.query(Page).filter(Page.bookmarked))
