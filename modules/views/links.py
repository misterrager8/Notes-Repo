import requests
from bs4 import BeautifulSoup
from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy import text

from modules.ctrla import DB
from modules.model import Link

saved_links = Blueprint("saved_links", __name__)
my_db = DB()


@saved_links.route("/links", methods=["POST", "GET"])
def all_links():
    if request.method == "POST":
        url = request.form["url"]
        title = BeautifulSoup(requests.get(url).content, "html.parser").find("title").string

        my_db.create(Link(url, title))
        return redirect(url_for("all_links"))

    return render_template("links/all_links.html", links=my_db.read_all(Link).order_by(text("date_added desc")).all())


@saved_links.route("/delete_link")
def delete_link():
    id_ = request.args.get("id_")
    link = my_db.find_by_id(Link, id_)

    my_db.delete(link)
    return redirect(url_for("all_links"))


@saved_links.route("/edit", methods=["POST"])
def edit_link():
    if request.method == "POST":
        id_ = request.args.get("id_")
        link = my_db.find_by_id(Link, id_)
        title = request.form["title_"]

        link.set_title(title)

        return redirect(url_for("all_links"))
