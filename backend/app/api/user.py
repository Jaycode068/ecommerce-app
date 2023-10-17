from flask import request, jsonify
from app.api import bp
from app.exceptions.user_exception import UserNotFound
from app.extension import db
from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.models.address import Address
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
# GET endpoint to retrieve all users
@bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        user_list = [{"Id":user.id, "username": user.username, "email": user.email} for user in users]
        return jsonify({"users": user_list}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'Database error occurred'}), 500

# Error handler for UserNotFoundError
@bp.errorhandler(UserNotFound)
def handle_user_not_found_error(error):
    return jsonify({'error': 'User not found'}), 404

# Error handler for general exceptions
@bp.errorhandler(Exception)
def handle_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate the request data
    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing username, email, or password'}), 400

    username = data['username']
    email = data['email']
    password = data['password']
    
    # Check if the username or email already exists in the database
    try:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({'error': 'Email already exists'}), 400
        
    except SQLAlchemyError as e:
        print(e)
        return jsonify({'error': 'Database error occurred'}), 500
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user
    new_user = User(username=username, email=email, password=hashed_password)

    try:
        # Add the new user to the database and commit the transaction
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        # Handle database errors
        db.session.rollback()
        return jsonify({'error': 'Error occurred while registering the user'}), 500

    # Add a return statement in case none of the conditions are met
    return jsonify({'error': 'Invalid request'}), 400

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Validate the request data
    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing username or email'}), 400

    username = data['username']
    email = data['email']
    password = data['password']

    # Check if the user with the specified user_id exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    # Update user information
    user.username = username
    user.email = email
    user.password = hashed_password

    try:
        db.session.commit()
        return jsonify({'message': 'User information updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error occurred while updating user information'}), 500

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Check if the user with the specified user_id exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error occurred while deleting the user'}), 500


