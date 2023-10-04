from flask import Flask
from config import Config
from app.extension import db
from app.main import bp as main_bp
from app.api.category import category_bp
from app.api.product import product_bp
from app.api import bp as user_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://johnson:"Ibelieve1!"@localhost:3306/appdb'

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp, url_prefix='/api')
    app.register_blueprint(product_bp, url_prefix='/api')

    

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
 
