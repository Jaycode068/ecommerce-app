from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.extension import db
from app.models.user import User
from app.models.schemas.user import UserSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt as bcrypt


user_bp = Blueprint('user', __name__)
api = Api(user_bp)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json() or {}

        try:
            user = user_schema.load(data, instance=user, partial=True)
            db.session.commit()
            return user_schema.dump(user), 200
        except IntegrityError as e:
            db.session.rollback()

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        data = request.get_json()
        errors = user_schema.validate(data)  # Validate the schema
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, 400

        # Check for unique username and email
        existing_user_with_username = User.query.filter_by(username=data['username']).first()
        existing_user_with_email = User.query.filter_by(email=data['email']).first()

        if existing_user_with_username:
            return {'message': 'Username already exists'}, 400

        if existing_user_with_email:
            return {'message': 'Email already exists'}, 400

        try:
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            return user_schema.dump(new_user), 201
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            return {'message': 'Error creating user'}, 500
        
api.add_resource(UserListResource, '/user')
api.add_resource(UserResource, '/user/<int:user_id>')