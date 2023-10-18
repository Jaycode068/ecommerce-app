from app.main import bp
from flask import render_template


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/users')
def user():
    return  render_template('user.html')

@bp.route('/about')
def about_us():
    
    return render_template('about.html')

@bp.route('/my-account')
def my_account():
    
    return render_template('my-account.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    
    return render_template('login.html')

@bp.route('/test-login', methods=['GET', 'POST'])
def test_login():
    
    return render_template('test.html')

