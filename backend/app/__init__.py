from flask import Flask
from config import Config
from app.extension import db
from app.main import bp as main_bp
from app.api.category import category_bp
from app.api.product import product_bp
from app.api.order import order_bp
from app.api import bp as user_bp
from app.auth.user_auth import auth_bp
from flask_jwt_extended import JWTManager
from flask_session import Session


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'your_secret_key_here'  

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://johnson:"Ibelieve1!"@localhost:3306/appdb'

    # Initialize Flask extensions here
    db.init_app(app)

    # Initialize Flask-Session
    Session(app)

    # Initialize the JWTManager
    jwt = JWTManager(app)

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp, url_prefix='/api')
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')


    

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
 
