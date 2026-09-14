from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

BASE_DIR = Path(__file__).resolve().parent.parent
HTML_DIR = BASE_DIR / 'html'

app = Flask(
    __name__,
    template_folder=str(HTML_DIR),
    static_folder=str(HTML_DIR),
    static_url_path=''
)
app.config.from_object(Config)

db = SQLAlchemy(app)

from yacut import views
from yacut.error_handlers import register_error_handlers

register_error_handlers(app)

from yacut import api_views, views
