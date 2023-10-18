from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=False)
    confirmpasswd = fields.String(required=True)
    addresses = fields.String(required=False)
