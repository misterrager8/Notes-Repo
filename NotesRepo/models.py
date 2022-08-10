from flask_login import UserMixin
from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship
import markdown
from NotesRepo import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    username = Column(Text)
    password = Column(Text)
    folders = relationship("Folder", backref="users", lazy="dynamic")
    notes = relationship("Note", backref="users", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_folders(self, filter_: str = "", order_by: str = "date_created desc"):
        return self.folders.filter(text(filter_)).order_by(text(order_by))

    def get_notes(self, filter_: str = "", order_by: str = "last_modified desc"):
        return self.notes.filter(text(filter_)).order_by(text(order_by))


class Folder(db.Model):
    __tablename__ = "folders"

    name = Column(Text)
    color = Column(Text)
    date_created = Column(DateTime)
    notes = relationship("Note", backref="folders", lazy="dynamic")
    user_id = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Folder, self).__init__(**kwargs)

    def get_notes(self, filter_: str = "", order_by: str = "last_modified desc"):
        return self.notes.filter(text(filter_)).order_by(text(order_by))


class Note(db.Model):
    __tablename__ = "notes"

    title = Column(Text)
    content = Column(Text)
    date_created = Column(DateTime)
    last_modified = Column(DateTime)
    favorited = Column(Boolean, default=False)
    folder_id = Column(Integer, ForeignKey("folders.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Note, self).__init__(**kwargs)

    def get_markdown(self):
        return markdown.markdown(self.content)
