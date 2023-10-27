from flask import Flask, Blueprint, request
from flask_restful import Api, Resource, reqparse
from app.extension import db
from app.models.cart import Cart
from app.models.schemas.cart import CartSchema

from app.models.user import User
from app.models.product import Product

cart_bp = Blueprint('cart', __name__)
api = Api(cart_bp)

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

class CartResource(Resource):
    def get(self, cart_id):
        cart = Cart.query.get_or_404(cart_id)
        return cart_schema.dump(cart)
    
    def delete(self, cart_id):
          cart = Cart.query.get_or_404(cart_id)
          db.session.delete(cart)
          db.session.commit()
          return {'message': 'Cart item deleted successfully'}, 204

class CartListResource(Resource):
    def get(self):
        carts = Cart.query.all()
        return carts_schema.dump(carts), 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
        parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
        args = parser.parse_args()
        #Deserialize and validate the incoming JSON data using the schema
        try:
            cart_data = cart_schema.load(args)
        except Exception as e:
            return {"message": "Validation error", "errors": e.messages}, 400
        
        user = User.query.get_or_404(cart_data['user_id'])
        product = Product.query.get_or_404(cart_data['product_id'])

        cart_item = Cart(user=user, product=product, quantity=cart_data['quantity'])
        db.session.add(cart_item)
        db.session.commit()

        #Serialize the response data using the schema
        result = cart_schema.dump(cart_item)
        return result, 201

api.add_resource(CartResource, '/cart_items/<int:cart_id>')
api.add_resource(CartListResource, '/cart_items')