from flask import Blueprint, request
from flask_restful import Api, Resource
from app.extension import db
from app.models.category import Category
from app.models.schemas.category import CategorySchema
from sqlalchemy.exc import IntegrityError
from flask import make_response

category_bp = Blueprint('category', __name__)
api = Api(category_bp)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

class CategoryResource(Resource):
    def get(self, category_id):
        category = Category.query.get_or_404(category_id)
        category_schema = CategorySchema()
        return category_schema.dump(category)

    def put(self, category_id):
        category = Category.query.get_or_404(category_id)
        data = request.get_json() or {}
        category_schema = CategorySchema()

        # Validate the incoming data
        errors = category_schema.validate(data)
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, 400

        try:
            # Update category fields from the request data
            category.name = data.get('name', category.name)
            # Update other fields here as needed

            db.session.commit()
            return category_schema.dump(category), 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error updating category', 'error': str(e)}, 500

    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return 'Category deleted', 204


class CategoryListResource(Resource):
    def get(self):
        categories = Category.query.all()
        category_schema = CategorySchema(many=True)
        return category_schema.dump(categories)

    def post(self):
        data = request.get_json()
        category_schema = CategorySchema()

        try:
            category = Category(name = data['name'])
            db.session.add(category)
            db.session.commit()
            return category_schema.dump(category), 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Category name must be unique'}, 400


api.add_resource(CategoryListResource, '/categories')
api.add_resource(CategoryResource, '/categories/<int:category_id>')
