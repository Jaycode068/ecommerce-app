from flask import Blueprint, request, jsonify, session, redirect, url_for
from app.models.user import User  # Import your User model
from app.extension import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    # User is authenticated, store user_id in the session
    session["user_id"] = user.id
    return jsonify({"message": "Login successful"}), 200

# Logout route
@auth_bp.route("/logout", methods=["POST"])
def logout():
    # Clear the user's session
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"}), 200

# Check the current user route
@auth_bp.route("/current_user", methods=["GET"])
def current_user():
    user_id = session.get("user_id")
    
    if user_id:
        user = User.query.get(user_id)
        return jsonify({"user": {"username": user.username, "email": user.email}}), 200
    else:
        return jsonify({"message": "No user is currently logged in"}), 200

# Protect routes with authentication
@auth_bp.before_request
def require_login():
    if "user_id" not in session:
        return jsonify({"error": "Authentication required"}), 401

# Add a logout route here

# Add a route to check the current user's information here

# Add any other authentication-related routes here

# Define a function to retrieve the current user object based on session
def get_current_user():
    user_id = session.get("user_id")
    if user_id:
        return User.query.get(user_id)
    return None

# Define a function to check if a user is currently authenticated
def is_authenticated():
    return "user_id" in session
