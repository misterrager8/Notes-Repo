from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user

from NotesRepo.ctrla import Database
from NotesRepo.models import Link

links = Blueprint("links", __name__)
database = Database()


@links.route("/link_create", methods=["POST"])
@login_required
def link_create():
    database.create(
        Link(
            url=request.form["url"],
            title=request.form["linktitle"],
            user_id=current_user.id,
            date_added=datetime.now(),
        )
    )

    return redirect(request.referrer)


@links.route("/links_")
@login_required
def links_():
    return render_template("links.html")


@links.route("/link_edit", methods=["POST"])
@login_required
def link_edit():
    link_: Link = database.get(Link, int(request.form["id_"]))

    link_.url = request.form["url"]
    link_.title = request.form["title"]
    database.update()

    return redirect(request.referrer)


@links.route("/toggle_read")
@login_required
def toggle_read():
    link_: Link = database.get(Link, int(request.args.get("id_")))

    link_.been_read = not link_.been_read
    database.update()

    return redirect(request.referrer)


@links.route("/link_delete")
@login_required
def link_delete():
    link_: Link = database.get(Link, int(request.args.get("id_")))
    database.delete(link_)

    return redirect(url_for("index"))


@links.route("/export_all")
@login_required
def export_all():
    return "\n".join(["%s %s" % (i.url, i.title) for i in current_user.get_links()])


@links.route("/get_title", methods=["POST"])
def get_title():
    url = request.form["url"]
    title = (
        BeautifulSoup(requests.get(url).content, "html.parser").find("title").get_text()
    )

    return title
