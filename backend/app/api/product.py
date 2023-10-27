from flask import Blueprint, request, jsonify, Response, json, send_from_directory
from flask_restful import Api, Resource
from app.extension import db
from app.models.product import Product
from app.models.category import Category
from app.models.schemas.product import ProductSchema
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
import os

product_bp = Blueprint('product', __name__, static_folder='img_upload')
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
    
def save_file(file):
    filename = secure_filename(file.filename)
  
    # Generate unique filename if file already exists
    if os.path.exists(os.path.join('main/upload', filename)):
        filename = generate_unique_filename(filename)

    file.save(os.path.join('main/upload', filename))
  
    return filename

def generate_unique_filename(filename):
    basename = os.path.basename(filename) 
    ext = os.path.extsep + filename.split(os.path.extsep)[-1]
  
    counter = 1
    while os.path.exists(os.path.join('main/upload', 
                       basename + '_' + str(counter) + ext)):
        counter += 1

    new_filename = basename + '_' + str(counter) + ext
    return new_filename

    
def query_image(product_id):
    result = Product.query.filter_by(id=product_id)
    for image in result:
        return image.image

class FetchPost(Resource):
    def get(self, image):
        
        return send_from_directory('img', image, mimetype='image/png')
    
def json_response(data, status_code=200):
    """Helper function to create a JSON response."""
    return Response(json.dumps(data), status=status_code, mimetype='application/json')

api.add_resource(FetchPost, '/file')    
api.add_resource(ProductListResource, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')