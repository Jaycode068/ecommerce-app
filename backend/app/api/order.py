from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, abort
from app.extension import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User
from app.models.product import Product
from marshmallow import Schema, fields, validate, ValidationError

order_bp = Blueprint('orders', __name__)
api = Api(order_bp)

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    total_price = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)
    items = fields.Nested(OrderItemSchema, many=True, required=True)

order_item_schema = OrderItemSchema()
order_schema = OrderSchema()

class OrderResource(Resource):
    def get(self, order_id):
        order = Order.query.get_or_404(order_id)
        order_data = order_schema.dump(order)
        return order_data, 200

    def post(self):
        try:
            data = request.get_json()
            # Deserialize and validate the incoming JSON data
            order_data = order_schema.load(data)
        except ValidationError as e:
            return {"message": "Validation error", "errors": e.messages}, 400
        
        # Create a new order instance and save it to the database
        order = Order(user_id=order_data['user_id'],
                      total_price=order_data['total_price'],
                      items=[OrderItem(**item) for item in order_data['items']])
        db.session.add(order)
        db.session.commit()

        return order_schema.dump(order), 201
    
class OrderListResource(Resource):
   
    def get(self, order_id=None):
        order_schema = OrderSchema()
        orders_schema = OrderSchema(many=True)
        # If order_id is provided, return a specific order
        if order_id:
            order = Order.query.get_or_404(order_id)
            return order_schema.dump(order), 200
        # If no order_id is provided, return all orders
        else:
            orders = Order.query.all()
        return orders_schema.dump(orders), 200


api.add_resource(OrderResource, '/orders', '/orders/<int:order_id>')
api.add_resource(OrderListResource, '/orders/all')