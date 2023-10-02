from flask import request, jsonify
from app.api import bp
from app.exceptions.user_exception import UserNotFound
from app.extension import db
from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.models.address import Address


# GET endpoint to retrieve all users
@bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        ##addresses = Address.query.all()
        
        print(users)
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


@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate the request data
    if not all(key in data for key in ['username', 'email','password']):
        return jsonify({'error': 'Missing username or email'}), 400

    username = data['username']
    email = data['email']
    password = data['password']
    
    print(data)

    print("Check user firs")
    # Check if the username or email already exists in the database
    try:
        existing_user = User.query.filter_by(username=username).first()
        print("Checking existing user from db "+ existing_user)
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({'error': 'Email already exists'}), 400
        
    except SQLAlchemyError as e:
        print(e)

    # Create a new user
    new_user = User(username=username, email=email, password=password)

    try:
        # Add the new user to the database and commit the transaction
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        print(e)
        # Handle database errors
        db.session.rollback()
        return jsonify({'error': 'Error occurred while registering the user'}), 500
