from flask import Flask, render_template, jsonify, send_from_directory, send_file, abort
from config import Config
from app.extension import db
from app.main.routes import bp as main_bp
from app.api.category import category_bp
from app.api.product import product_bp
from app.api.order import order_bp
from app.api import bp as user_bp
from app.auth.user_auth import auth_bp
from app.api.address import address_bp
from app.api.order_Item import order_item_bp
from app.api.cart import cart_bp
import os
from flask_cors import CORS
 

from flask_jwt_extended import JWTManager
from flask_session import Session

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='main/templates', static_folder='main/static/assets')
    app.config.from_object(config_class)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    CORS(app)
    
    
    # Ensure the upload folder exists, create it if necessary
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  

    

    # Initialize Flask extensions here
    db.init_app(app)
    

    # Initialize Flask-Session
    Session(app)

    # Initialize the JWTManager
    jwt = JWTManager(app)

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/api/v1')
    app.register_blueprint(category_bp, url_prefix='/api/v1')
    app.register_blueprint(product_bp, url_prefix='/api/v1')
    app.register_blueprint(order_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/auth/v1')
    app.register_blueprint(address_bp, url_prefix='/api/v1')
    app.register_blueprint(order_item_bp, url_prefix='/api/v1')
    app.register_blueprint(cart_bp, url_prefix='/api/v1')
    
    @app.route('/static/images/<path:filename>')
    def serve_static_image_file(filename):
        return send_from_directory('tests', filename, mimetype='image/png')

    
    @app.route('/test/')
    def test_page():
        
        from app.models.address import Address
        from app.models.cart import Cart
        from app.models.category import Category
        from app.models.order_item import OrderItem
        from app.models.order import Order
        from app.models.payment import Payment
        from app.models.product import Product
        from app.models.user import User
        db.create_all()
        
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    

    return app
 
