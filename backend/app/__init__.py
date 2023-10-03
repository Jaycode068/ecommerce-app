from flask import Flask

from config import Config
from app.extension import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://johnson:"Ibelieve1!"@localhost:3306/appdb'

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    #User endpoint blueprint
    from app.api import bp as user_bp
    app.register_blueprint(user_bp)

    # from app.posts import bp as posts_bp
    # app.register_blueprint(posts_bp, url_prefix='/posts')

    # from app.questions import bp as questions_bp
    # app.register_blueprint(questions_bp, url_prefix='/questions')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
