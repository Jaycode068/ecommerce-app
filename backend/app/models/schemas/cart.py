from marshmallow import Schema, fields
from app.models.schemas.user import UserSchema
from app.models.schemas.product import ProductSchema

class CartSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)