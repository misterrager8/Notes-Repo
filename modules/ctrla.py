import textwrap

from modules import db
from modules.model import Note


class NoteDB:
    def __init__(self): pass

    @staticmethod
    def get_all(): return db.session.query(Note).all()

    @staticmethod
    def insert_many(stuff: list):
        for i in stuff: i.insert()

    @staticmethod
    def insert_from_file(title: str, file_path: str):
        with open(file_path, "r") as f:
            output = textwrap.fill(f.read(), replace_whitespace=False, width=120)

        Note(title, output).insert()

    @staticmethod
    def find_by_id(note_id: int): return db.session.query(Note).get(note_id)

    @staticmethod
    def delete_all():
        db.session.execute("TRUNCATE TABLE notes")
        db.session.commit()
