from datetime import datetime

import markdown
from flask_login import UserMixin
from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship

from modules import app, db


class Page(db.Model):
    __tablename__ = "pages"

    title = Column(Text)
    content = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    last_modified = Column(DateTime, default=datetime.now())
    author_id = Column(Integer, ForeignKey("users.id"))
    folder_id = Column(Integer, ForeignKey("folders.id"))
    bookmarked = Column(Boolean, default=False)
    is_draft = Column(Boolean, default=False)
    sources = relationship("Source", backref="pages")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Page, self).__init__(**kwargs)

    def content_to_html(self) -> str:
        html = markdown.markdown(self.content)
        return html

    def get_last_modified(self) -> str:
        return self.last_modified.strftime("%B %d, %Y %I:%M %p")

    def get_date_created(self) -> str:
        return self.date_created.strftime("%B %d, %Y %I:%M %p")

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s,%s,%s" % (self.id,
                                            self.title,
                                            self.date_created,
                                            self.last_modified,
                                            self.users.username,
                                            self.folder_id,
                                            self.bookmarked,
                                            self.is_draft)


class Folder(db.Model):
    __tablename__ = "folders"

    name = Column(Text)
    color = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    author_id = Column(Integer, ForeignKey("users.id"))
    pages = relationship("Page", backref="folders")
    sources = relationship("Source", backref="folders")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Folder, self).__init__(**kwargs)

    def get_date_created(self) -> str:
        return self.date_created.strftime("%B %d, %Y %I:%M %p")

    def __str__(self):
        return "%s,%s,%s,%s,%s" % (self.id,
                                   self.name,
                                   self.color,
                                   self.date_created,
                                   self.users.username)


class Source(db.Model):
    __tablename__ = "sources"

    url = Column(Text)
    title = Column(Text)
    folder_id = Column(Integer, ForeignKey("folders.id"))
    page_id = Column(Integer, ForeignKey("pages.id"))
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Source, self).__init__(**kwargs)

    def __str__(self):
        return "%s,%s" % (self.url,
                          self.title)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    username = Column(Text)
    password = Column(Text)
    pages = relationship("Page", backref="users", lazy="dynamic")
    folders = relationship("Folder", backref="users", lazy="dynamic")
    date_added = Column(Date, default=datetime.today())
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return "%s,%s,%s" % (self.id,
                             self.username,
                             self.date_added)


with app.app_context():
    db.create_all()
