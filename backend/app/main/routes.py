from app.main import bp
from flask import render_template


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/users')
def user():
    return  render_template('user.html')
