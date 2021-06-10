from datetime import datetime

import markdown
from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from modules import app, db


class Page(db.Model):
    __tablename__ = "pages"

    title = Column(Text)
    content = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    last_modified = Column(DateTime, default=datetime.now())
    folder_id = Column(Integer, ForeignKey("folders.id"))
    bookmarked = Column(Boolean, default=False)
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 title: str,
                 content: str,
                 date_created: datetime = datetime.now(),
                 last_modified: datetime = datetime.now(),
                 tag: str = ""):
        self.title = title.title()
        self.content = content
        self.date_created = date_created
        self.last_modified = last_modified
        self.bookmarked = bookmarked

    def edit_page(self, title: str, content: str):
        self.title = title.title()
        self.content = content
        self.last_modified = datetime.now()
        db.session.commit()

    def content_to_html(self):
        html = markdown.markdown(self.content)
        return html

    def get_last_modified(self):
        return self.last_modified.strftime("%B %d, %Y %I:%M %p")

    def get_date_created(self):
        return self.date_created.strftime("%B %d, %Y %I:%M %p")

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.title,
                                      self.content,
                                      self.date_created,
                                      self.last_modified,
                                      self.folder_id,
                                      self.bookmarked)


class Folder(db.Model):
    __tablename__ = "folders"

    name = Column(Text)
    color = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    pages = relationship("Page", backref="folders")
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 name: str,
                 color: str,
                 date_created: datetime = datetime.now()):
        self.name = name.title()
        self.color = color
        self.date_created = date_created

    def edit_folder(self, name: str, color: str):
        self.name = name.title()
        self.color = color
        db.session.commit()

    def add_page(self, page: Page):
        self.pages.append(page)
        db.session.commit()

    def get_date_created(self):
        return self.date_created.strftime("%B %d, %Y %I:%M %p")

    def __str__(self):
        return "%s,%s,%s" % (self.name,
                             self.color,
                             self.date_created)


class Link(db.Model):
    __tablename__ = "links"

    url = Column(Text)
    title = Column(Text)
    date_added = Column(DateTime, default=datetime.now())
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Link, self).__init__(**kwargs)

    def get_date_added(self) -> str:
        return self.date_added.strftime("%B %d, %Y %I:%M %p")

    def __str__(self):
        return "%s,%s,%s" % (self.url,
                             self.title,
                             self.date_added)


class Idea(db.Model):
    __tablename__ = "ideas"

    title = Column(Text)
    date_added = Column(DateTime, default=datetime.now())
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Idea, self).__init__(**kwargs)

    def __str__(self):
        return "%s,%s" % (self.title, self.date_added)


with app.app_context():
    db.create_all()
