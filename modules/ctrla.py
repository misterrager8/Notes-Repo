from modules import db


class DB:
    def __init__(self):
        pass

    @staticmethod
    def find_by_id(type_, id_: int):
        return db.session.query(type_).get(id_)

    @staticmethod
    def create(object_):
        db.session.add(object_)
        db.session.commit()

    @staticmethod
    def read_all(type_):
        return db.session.query(type_).all()

    @staticmethod
    def delete(object_):
        db.session.delete(object_)
        db.session.commit()
