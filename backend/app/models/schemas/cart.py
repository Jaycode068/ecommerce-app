# from marshmallow import Schema, fields
# from app.models.schemas.user import UserSchema
# from app.models.schemas.product import ProductSchema

# class CartSchema(Schema):
#     id = fields.Int(dump_only=True)
#     user = fields.Nested(UserSchema, only=('id', 'username'))
#     product = fields.Nested(ProductSchema, only=('id', 'name'))
#     quantity = fields.Int(required=True)