from datetime import datetime

from sqlalchemy import Column, Text, Integer, DateTime

from modules import db


class Page(db.Model):
    __tablename__ = "pages"

    title = Column(Text)
    content = Column(Text)
    date_created = Column(DateTime)
    last_modified = Column(DateTime)
    tag = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 title: str,
                 content: str,
                 date_created: datetime = datetime.now(),
                 last_modified: datetime = datetime.now(),
                 tag: str = ""):
        self.title = title.capitalize()
        self.content = content
        self.date_created = date_created
        self.last_modified = last_modified
        self.tag = tag

    def __str__(self):
        return "%d\t%s" % (self.id, self.title)


db.create_all()
