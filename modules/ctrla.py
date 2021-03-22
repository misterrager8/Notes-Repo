from modules import db
from modules.model import Note


class NoteDB:
    def __init__(self): pass

    @staticmethod
    def get_all(): return db.session.query(Note).all()

    @staticmethod
    def insert_many(stuff):
        for i in stuff: i.insert()

    @staticmethod
    def delete_all():
        db.session.execute("TRUNCATE TABLE notes")
        db.session.commit()
