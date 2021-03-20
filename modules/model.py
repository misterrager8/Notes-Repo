from datetime import date, datetime


class Note:
    def __init__(self,
                 title: str,
                 content: str,
                 date_added: date = datetime.now().date(),
                 last_modified: date = datetime.now().date(),
                 tags: list = None):
        self.title = title
        self.content = content
        self.date_added = date_added
        self.last_modified = last_modified
        self.tags = tags

    def __repr__(self):
        return "%s\t%s\t%s" % (self.title,
                               self.date_added,
                               self.last_modified)
