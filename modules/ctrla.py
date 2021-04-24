from modules import db
from modules.model import Page


class DB:
    def __init__(self):
        pass

    @staticmethod
    def find_by_id(id_):
        return db.session.query(Page).get(id_)

    @staticmethod
    def create(object_):
        db.session.add(object_)
        db.session.commit()

    @staticmethod
    def read_all():
        return db.session.query(Page).all()

    @staticmethod
    def delete(object_):
        db.session.delete(object_)
        db.session.commit()
