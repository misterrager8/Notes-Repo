import json
from datetime import datetime


class Note:
    def __init__(self,
                 title: str,
                 content: str,
                 date_added: str = datetime.now().strftime("%Y-%m-%d")):
        self.title = title
        self.content = content
        self.date_added = date_added

    def insert(self):
        f_n = "../notes/" + self.title + ".json"
        with open(f_n, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)

    def __repr__(self):
        return "%s\t%s" % (self.title,
                           self.date_added)
