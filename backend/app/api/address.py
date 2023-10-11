from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.extension import db
from app.models.address import Address
from app.models.schemas.address import AddressSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError


address_bp = Blueprint('address', __name__)
api = Api(address_bp)

address_schema = AddressSchema()

class AddressResource(Resource):
    def get(self, address_id):
        address = Address.query.get_or_404(address_id)
        return address_schema.dump(address)

    def put(self, address_id):
        address = Address.query.get_or_404(address_id)
        data = request.get_json() or {}

        try:
            address = address_schema.load(data, instance=address, partial=True)
            db.session.commit()
            return address_schema.dump(address), 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Error updating address'}, 400

    def delete(self, address_id):
        address = Address.query.get_or_404(address_id)
        db.session.delete(address)
        db.session.commit()
        return '', 204

class AddressListResource(Resource):
    def get(self):
        addresses = Address.query.all()
        return address_schema.dump(addresses)

    def post(self):
        data = request.get_json()

        try:
            address = address_schema.load(data)
            db.session.add(address)
            db.session.commit()
            return address_schema.dump(address), 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Error creating address'}, 400
        
class AddressTestResource(Resource):
    def get(self):
        addresses = Address.query.all()
        return address_schema.dump(addresses)
    
@address_bp.route('/all', methods=['GET'])
def get_users():
    try:
        addresses = Address.query.all()
        address_list = [address.to_dict() for address in addresses]  # Assuming to_dict() method is defined in your Address model
        return jsonify(addresses=address_list), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)  # You can log the error for debugging purposes
        return jsonify({'error': 'Database error occurred'}), 500

api.add_resource(AddressListResource, '/addresses')
api.add_resource(AddressResource, '/addresses/<int:address_id>')
api.add_resource(AddressTestResource, '/address')