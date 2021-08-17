from datetime import datetime

import markdown
from flask_login import UserMixin
from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from modules import app, db


class Page(db.Model):
    __tablename__ = "pages"

    title = Column(Text)
    content = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    last_modified = Column(DateTime, default=datetime.now())
    bookmarked = Column(Boolean, default=False)
    folder_id = Column(Integer, ForeignKey("folders.id"))
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Page, self).__init__(**kwargs)

    def content_to_html(self) -> str:
        html = markdown.markdown(self.content)
        return html

    def __str__(self):
        return "%s,%s,%s,%s" % (self.title,
                                self.date_created,
                                self.last_modified,
                                self.folders.name)


class Folder(db.Model):
    __tablename__ = "folders"

    name = Column(Text)
    color = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    pages = relationship("Page", backref="folders")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Folder, self).__init__(**kwargs)

    def __str__(self):
        return "%s,%s,%s" % (self.name,
                             self.color,
                             self.date_created)


class Admin(UserMixin, db.Model):
    __tablename__ = "admin"

    username = Column(Text)
    password = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)

    def __str__(self):
        return "%s" % self.username


with app.app_context():
    db.create_all()
