from sqlalchemy import text

from modules import app
from modules.ctrla import DB
from modules.model import Folder, Page


@app.context_processor
def inject_recent():
    folders_ = DB().read_all(Folder).order_by(text("date_created desc"))
    pages_ = DB().read_all(Page).order_by(text("last_modified desc"))
    return dict(folders_=folders_, pages_=pages_)
