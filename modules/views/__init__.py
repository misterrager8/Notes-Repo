from sqlalchemy import text

from modules import app, db
from modules.model import Folder, Page


@app.context_processor
def inject_recent():
    folders_ = db.session.query(Folder).order_by(text("date_created desc"))
    pages_ = db.session.query(Page).filter_by(is_draft=False).order_by(text("last_modified desc"))
    return dict(folders_=folders_, pages_=pages_)
