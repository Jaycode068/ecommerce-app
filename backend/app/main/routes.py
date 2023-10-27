
from flask import render_template, session, jsonify, redirect, send_from_directory,url_for, Blueprint
import os
bp = Blueprint('routes', __name__, static_folder='static/img')

@bp.route('/img')
def get_product_image():
    return send_from_directory(bp.static_folder, 'blog1.png', origin='http://localhost:5000')

@bp.route('/')
def landing_page():
    return render_template('landing-page.html')

@bp.route('/main')
#@login_required
def main():
    if session.get('logged_in'):
        
        return render_template('index.html')
    else:
        return redirect('/login')
        
@bp.route('/users')
def user():
    return  render_template('user.html')

@bp.route('/about')
def about_us():
    
    return render_template('about.html')

@bp.route('/my-account')
def my_account():
    if session.get('logged_in'):
        login_user = session.get('username')
        return render_template('my-account.html', login_user=login_user)
    else:
        return redirect('/login')
        
@bp.route('/app')
def application_manager():
    
    return render_template('application-management.html')

@bp.route('/shop-grid')
def shop_grid():
    if session.get('logged_in'):
        user_id = session.get('user_id')
        return render_template('shop-grid.html', user_id=user_id)
    else:
        return redirect('/login')
    

@bp.route('/contact')
def contact():
    return render_template('contact.html')


@bp.route('/cart')
def cart():
    if session.get('logged_in'):
        print(session.get('user_id'))
        return render_template('cart.html')
    else:
        return redirect('/login')


@bp.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@bp.route('/compare')
def compare():
    return render_template('compare.html')

@bp.route('/faq')
def faq():
    return render_template('faq.html')


@bp.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@bp.route('/blog')
def blog():
    return render_template('blog.html')

@bp.route('/blog-details')
def blog_details():
    return render_template('blog-details.html')

@bp.route('/product-details')
def product_details():
    return render_template('product-details.html')

@bp.route('/checkout')
def checkout():
    return render_template('checkout.html')

@bp.route('/error')
def error():
    return render_template('404.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    
    return render_template('login.html')

@bp.route('/test-login', methods=['GET', 'POST'])
def test_login():
    
    return render_template('test.html')