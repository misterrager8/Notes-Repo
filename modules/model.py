from datetime import date, datetime

from sqlalchemy import Column, Text, Date, Integer

from modules import db


class Note(db.Model):
    __tablename__ = "notes"

    title = Column(Text)
    content = Column(Text)
    date_added = Column(Date)
    last_modified = Column(Date)
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 title: str,
                 content: str,
                 date_added: date = datetime.now().date(),
                 last_modified: date = datetime.now().date()):
        self.title = title
        self.content = content
        self.date_added = date_added
        self.last_modified = last_modified

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def update(self):
        pass

    def get_date(self):
        return self.date_added.strftime("%B %d, %Y")

    def save(self):
        file1 = open(self.title + ".txt", "w")
        file1.write(self.content)

    def __repr__(self):
        return "%s\t%s\t%s" % (self.title,
                               self.date_added,
                               self.last_modified)


db.create_all()
