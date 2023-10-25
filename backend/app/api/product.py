from flask import Blueprint, request, jsonify, Response, json, send_from_directory
from flask_restful import Api, Resource
from app.extension import db
from app.models.product import Product
from app.models.category import Category
from app.models.schemas.product import ProductSchema
from app.models.schemas.category import CategorySchema
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
import os

product_bp = Blueprint('product', __name__)
api = Api(product_bp)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@product_bp.route('/product', methods=['POST', 'GET'])
def create_product():

    # Check for multipart/form-data 
    if request.files:
        # Get data from form 
        name = request.form.get('name')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        price = request.form.get('price')
      
        # Get file object
        file = request.files.get('image')
      
        if file:
            # Save file
            filename = save_file(file)

        else:
            # Get JSON data
            data = request.get_json()
    
        # Get category
        category = Category.query.get(category_id)

        if not category:
            return {"error": "Invalid category"}, 400

        # Create product object
        product = Product(name=name, description=description, price=price, category=category, image_filename=filename)

        db.session.add(product)
        db.session.commit()
        response = {
            "product": product_schema.dump(product),
            "image_path": send_from_directory('product/images/', filename)
        }
        return jsonify(response)

    return {"error": "Invalid request"}, 400

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
    
    def post():
        
        '''
        # Validate form data
        product_data, errors = product_schema().load(request.form)
  
        # Validate file 
        file_data, file_errors = request.files
  
        if errors or file_errors:
            return jsonify({
            "errors": errors + file_errors
        }), 400
  
        # Save file
        filename = save_file(file_data['image'])
        
        product_data['image_filename'] = filename
  
        # Create product 
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()

        # Return product object
        return jsonify({
            "product": product_schema().dump(product) 
        })
        '''
        return 'Here', 200
    
def save_file(file):
    filename = secure_filename(file.filename)
  
    # Generate unique filename if file already exists
    if os.path.exists(os.path.join('product/images/', filename)):
        filename = generate_unique_filename(filename)

    file.save(os.path.join('product/images', filename))
  
    return filename

def generate_unique_filename(filename):
    basename = os.path.basename(filename) 
    ext = os.path.extsep + filename.split(os.path.extsep)[-1]
  
    counter = 1
    while os.path.exists(os.path.join('product/images/', 
                       basename + '_' + str(counter) + ext)):
        counter += 1

    new_filename = basename + '_' + str(counter) + ext
    return new_filename

    # def post(self):
    #     try:
    #         # Get JSON data from the request
    #         data = request.get_json()
    #         print(data)
    #         category = data.get('category_id')
    
    #         if 'image' not in request.files:
    #             return "File name not found"
    #         file = request.files['image']
    #         print("*******")
    #         print(file.filename)
    #         print("*******")
    #         try:
    #             if file:
    #                 filename = os.path.join(product_bp.config['UPLOAD_FOLDER'], file.filename)
    #                 file.save(filename)
    #                 print('not found')
    #         except Exception as e:
    #             print(e)
    #             return "Error while trying to save file", 500
    #         try:
    #             #Retrieve the existing category from the database based on category_id
    #             existing_category = Category.query.get_or_404(category)
        
    #         # Handle validation errors, IntegrityErrors, and other exceptions as needed
    #         except ValidationError as err:
    #             response_data = {'errors': err.messages}
    #             return json_response(response_data, status_code=400)
            
            
            
            
            
    #         # Validate and deserialize product data using product_schema
    #         product_data_validated = product_schema.load(data)
    #         product_data_validated['image_filename'] = filename
            
    #         # Create a new Product instance associated with the existing category
    #         new_product = Product(**product_data_validated)

    #         # Add the new product to the database session
    #         db.session.add(new_product)

    #         # Commit the transaction to the database
    #         db.session.commit()

    #         # Return the newly created product as JSON response
    #         response_data = {
    #             'product': ProductSchema().dump(new_product),
    #             'category': CategorySchema().dump(existing_category)
    #         }
    #         return json_response(response_data, status_code=201)

    #     # Handle validation errors, IntegrityErrors, and other exceptions as needed
    #     except ValidationError as err:
    #         response_data = {'errors': err.messages}
    #         return json_response(response_data, status_code=400)

    #     except IntegrityError as e:
    #         db.session.rollback()
    #         response_data = {'error': 'Database integrity error occurred.'}
    #         return json_response(response_data, status_code=500)

    #     except Exception as e:
    #         db.session.rollback()
    #         print(e)
    #         response_data = {'error': 'Internal server error occurred.'}
    #         return json_response(response_data, status_code=500)
        
        
def json_response(data, status_code=200):
    """Helper function to create a JSON response."""
    return Response(json.dumps(data), status=status_code, mimetype='application/json')
        
api.add_resource(ProductListResource, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')