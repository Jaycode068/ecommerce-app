from flask import Blueprint, request, jsonify, Response, json
from flask_restful import Api, Resource
from app.extension import db
from app.models.product import Product
from app.models.category import Category
from app.models.schemas.product import ProductSchema
from app.models.schemas.category import CategorySchema
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
import re

product_bp = Blueprint('product', __name__)
api = Api(product_bp)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return product_schema.dump(product)
    def put(self, product_id):
        product = Product.query.get_or_404(product_id)
        data = request.get_json() or {}

        try:
            # Validate and load the JSON data into a new product object
            updated_product = product_schema.load(data, partial=True)
            # Update the specific fields of the existing product
            for field in updated_product:
                setattr(product, field, updated_product[field])

            db.session.commit()
            return product_schema.dump(product), 200
        except ValidationError as e:
            # Handle validation errors
            db.session.rollback()
            return {"message": str(e)}, 400
        except IntegrityError:
            # Handle integrity errors (e.g., unique constraint violations)
            db.session.rollback()
            return {'message': 'Error updating product. Integrity error occurred.'}, 400
        except Exception as e:
            # Handle other unexpected errors
            db.session.rollback()
            return {'message': str(e)}, 500
        

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return products_schema.dump(products)
   
    def post(self):
        try:
            # Get JSON data from the request
            data = request.get_json()
            
            category = data.get('category_id')
            print(category)
            try:
                #Retrieve the existing category from the database based on category_id
                existing_category = Category.query.get_or_404(category)
                print(existing_category)
        
            # Handle validation errors, IntegrityErrors, and other exceptions as needed
            except ValidationError as err:
                response_data = {'errors': err.messages}
                return json_response(response_data, status_code=400)
            
            # Validate and deserialize product data using product_schema
            product_data_validated = product_schema.load(data)
            
            # Create a new Product instance associated with the existing category
            new_product = Product(**product_data_validated)

            # Add the new product to the database session
            db.session.add(new_product)

            # Commit the transaction to the database
            db.session.commit()

            # Return the newly created product as JSON response
            response_data = {
                'product': ProductSchema().dump(new_product),
                'category': CategorySchema().dump(existing_category)
            }
            return json_response(response_data, status_code=201)

        # Handle validation errors, IntegrityErrors, and other exceptions as needed
        except ValidationError as err:
            response_data = {'errors': err.messages}
            return json_response(response_data, status_code=400)

        except IntegrityError as e:
            db.session.rollback()
            response_data = {'error': 'Database integrity error occurred.'}
            return json_response(response_data, status_code=500)

        except Exception as e:
            db.session.rollback()
            print(e)
            response_data = {'error': 'Internal server error occurred.'}
            return json_response(response_data, status_code=500)
        
        
def json_response(data, status_code=200):
    """Helper function to create a JSON response."""
    return Response(json.dumps(data), status=status_code, mimetype='application/json')
        
api.add_resource(ProductListResource, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')