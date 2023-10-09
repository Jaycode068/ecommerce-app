# app/auth/user_auth.py

from flask import Blueprint, request, jsonify, session, g
from app.extension import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_session import Session


auth_bp = Blueprint('user_auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    
    if not user or not verify_password(user.password, password):
        return jsonify({'message': 'Login failed'}), 401
    
    # Store user information in the session
    session['user_id'] = user.id

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    # Clear the session to log the user out
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/current_user', methods=['GET'])
@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

def verify_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password)

@auth_bp.route('/protected/resource', methods=['GET'])
@jwt_required()
def protected_resource():
    # This endpoint is protected, and only accessible with a valid access token

    # Return a JSON response
    return jsonify({'message': 'This is a protected resource.'})