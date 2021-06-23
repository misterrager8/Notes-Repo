from flask_login import current_user
from sqlalchemy import text

from modules import app, db, login_manager
from modules.model import User


@app.context_processor
def inject_recent():
    folders_ = current_user.folders.order_by(text("date_created desc")) if not current_user.is_anonymous else []
    pages_ = current_user.pages.filter_by(is_draft=False).order_by(
        text("last_modified desc")) if not current_user.is_anonymous else []
    return dict(folders_=folders_, pages_=pages_)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))
