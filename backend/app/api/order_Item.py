from flask import Flask, Blueprint, request
from flask_restful import Api, Resource, reqparse
from app.extension import db  
from app.models.order_item import OrderItem
from app.models.product import Product
from marshmallow import Schema, fields, ValidationError  

order_item_bp = Blueprint('order_items', __name__)
api = Api(order_item_bp)

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    order_id = fields.Int(required=False)
    

# Resource Definition
class OrderItemResource(Resource):
    order_item_schema = OrderItemSchema()

    def get(self, order_item_id):
        order_item = OrderItem.query.get_or_404(order_item_id)
        return self.order_item_schema.dump(order_item)

    def delete(self, order_item_id):
        order_item = OrderItem.query.get_or_404(order_item_id)
        db.session.delete(order_item)
        db.session.commit()
        return {'message': 'Order item deleted successfully'}, 204

class OrderItemListResource(Resource):
    order_item_schema = OrderItemSchema()
    order_items_schema = OrderItemSchema(many=True)
    def get(self):
        order_items = OrderItem.query.all()
        serialized_order_items = self.order_items_schema.dump(order_items)
        return serialized_order_items

    def post(self):
        try:
            data = request.get_json()
            # Deserialize and validate the incoming JSON data
            order_item_data = self.order_item_schema.load(data)
        except ValidationError as e:
            return {"message": "Validation error", "errors": e.messages}, 400
        
        # Create a new OrderItem instance and save it to the database
        order_item = OrderItem(product_id=order_item_data['product_id'],
                               quantity=order_item_data['quantity'])
        
        db.session.add(order_item)
        db.session.commit()

        return self.order_item_schema.dump(order_item), 201
    
    def put(self, order_item_id):
        order_item = OrderItem.query.get_or_404(order_item_id)
        data = request.get_json()
        errors = self.order_item_schema.validate(data)
        if errors:
            return errors, 400

        product_id = data['product_id']
        quantity = data['quantity']

        product = Product.query.get_or_404(product_id)
        order_item.product = product
        order_item.quantity = quantity

        db.session.commit()

        return self.order_item_schema.dump(order_item), 200

api.add_resource(OrderItemResource, '/order_items/<int:order_item_id>')
api.add_resource(OrderItemListResource, '/order_items')