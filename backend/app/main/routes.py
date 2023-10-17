from app.main import bp
from flask import render_template


@bp.route('/')
def index():
    #return render_template('shopzo.html')
    return 'This is The Main Blueprint'

