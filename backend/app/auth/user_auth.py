# app/auth/user_auth.py

from flask import Blueprint, request, jsonify, session, g, redirect, url_for
from app.extension import db, bcrypt
from app.models.user import User
import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity




auth_bp = Blueprint('user_auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    
    if not user or not verify_password(user.password, password):
        return jsonify({'messavge':'Invalid username and password'}), 401
    
    # Store user information in the session
    session['user_id'] = user.id
    session['logged_in'] = True
    session['username'] = user.username

    access_token = create_access_token(identity=user.id)
    
    # Redirect the user to the '/main' route
    return 'success', 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Clear the session to log the user out
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.before_request
def before_request():
    last_activity_time = session.get('last_activity')
    if last_activity_time and (datetime.datetime.now() - last_activity_time > datetime.timedelta(minutes=2)):
        # Clear session and log out user
        session.clear()

    # Update the last activity time in the session
    session['last_activity'] = datetime.datetime.now()


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