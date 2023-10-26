from flask import Blueprint

bp = Blueprint('api', __name__, static_folder='img_upload')

from app.api import user