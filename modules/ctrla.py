import os


class JsonCtrla:
    def __init__(self): pass

    @staticmethod
    def get_all():
        _ = []
        for i in os.listdir("./notes/"):
            _.append(i.split(".json")[0])

        return _

    @staticmethod
    def delete_all(): pass

    @staticmethod
    def import_notes(): pass
