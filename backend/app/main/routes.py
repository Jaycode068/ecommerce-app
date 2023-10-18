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

@bp.route('/shop')
def shop_list():
    
    return render_template('shop-list.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')


@bp.route('/cart')
def cart():
    return render_template('cart.html')


@bp.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@bp.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')


@bp.route('/error')
def error():
    return render_template('404.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    
    return render_template('login.html')

@bp.route('/test-login', methods=['GET', 'POST'])
def test_login():
    
    return render_template('test.html')

