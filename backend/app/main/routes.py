from app.main import bp
from flask import render_template


@bp.route('/')
def index():
    return 'This is The Main Blueprint'