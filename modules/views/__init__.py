from sqlalchemy import text

from modules import app
from modules.ctrla import DB
from modules.model import Folder, Page


@app.context_processor
def inject_recent():
    recent_folders = DB().read_all(Folder).order_by(text("date_created desc"))[:5]
    recent_pages = DB().read_all(Page).order_by(text("last_modified desc"))[:5]
    return dict(recent_folders=recent_folders, recent_pages=recent_pages)
