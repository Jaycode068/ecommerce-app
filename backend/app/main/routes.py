from app.main import bp
from flask import render_template


@bp.route('/')
def index():
    return render_template('shopzo.html')
    
@bp.route('/register')
def register():
    return render_template('register.html')
