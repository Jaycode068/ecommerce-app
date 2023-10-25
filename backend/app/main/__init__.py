from flask import Blueprint

bp = Blueprint('main', __name__ , static_folder='product/images')

from app.main import routes