from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    description = fields.Str(validate=validate.Length(max=500)) 
    category_id = fields.Int(required=False)
