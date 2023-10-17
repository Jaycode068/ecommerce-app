from app.main import bp
from flask import render_template


@bp.route('/')
def index():
    return render_template('shopzo.html')

@bp.route('/users')
def user():
    return  render_template('user.html')

@bp.route('/address')
def add_address():
    return  render_template('address.html')