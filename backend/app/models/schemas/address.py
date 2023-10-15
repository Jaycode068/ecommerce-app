from marshmallow import Schema, fields, validate

class AddressSchema(Schema):
    id = fields.Int(dump_only=True)
    street = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    postal_code = fields.String(required=True)
    user_id = fields.Int(required=False)
