from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required
from sqlalchemy import text

from NotesRepo import db
from NotesRepo.models import Page, Folder

pages = Blueprint("pages", __name__)


@pages.route("/my_pages")
def my_pages():
    order_by = request.args.get("order_by", default="last_modified desc")
    _ = db.session.query(Page).join(Folder).order_by(text(order_by))

    return render_template("pages/my_pages.html", all_pages=_, order_by=order_by)


@pages.route("/page")
def page():
    page_: Page = db.session.query(Page).get(request.args.get("id_"))

    return render_template("pages/page.html", page=page_)


@pages.route("/page_plain")
def page_plain():
    page_: Page = db.session.query(Page).get(request.args.get("id_"))

    return "<title>%s [PLAIN]</title><div style=\"white-space: pre-wrap;\">%s</div>" % (page_.title, page_.content)


@pages.route("/page_create", methods=["POST"])
@login_required
def page_create():
    folder_: Folder = db.session.query(Folder).get(request.args.get("id_"))

    _ = Page(title=request.form["title"].title(),
             content="",
             folders=folder_,
             date_created=datetime.now(),
             last_modified=datetime.now())
    db.session.commit()
    return redirect(url_for("pages.editor", id_=_.id))


@pages.route("/page_delete")
@login_required
def page_delete():
    _: Page = db.session.query(Page).get(request.args.get("id_"))
    db.session.delete(_)
    db.session.commit()

    return redirect(request.referrer)


@pages.route("/editor", methods=["POST", "GET"])
@login_required
def editor():
    if request.method == "POST":
        id_ = int(request.form["id_"])
        page_: Page = db.session.query(Page).get(id_)

        page_.title = request.form["title"]
        page_.folder_id = int(request.form["folder_id"])
        page_.content = request.form["content"]
        page_.last_modified = datetime.now()
        db.session.commit()

        return redirect(request.referrer)
    else:
        id_ = request.args.get("id_")
        page_: Page = db.session.query(Page).get(id_)

        return render_template("pages/editor.html", page=page_)


@pages.route("/mark_page")
@login_required
def mark_page():
    page_: Page = db.session.query(Page).get(request.args.get("id_"))

    page_.bookmarked = not page_.bookmarked
    db.session.commit()

    return redirect(request.referrer)


@pages.route("/page_visibility")
@login_required
def page_visibility():
    page_: Page = db.session.query(Page).get(request.args.get("id_"))

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
    return render_template("pages/bookmarks.html",
                           bookmarks_=db.session.query(Page).filter(Page.bookmarked).order_by(
                               text("last_modified desc")))
