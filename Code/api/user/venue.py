from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import Venue
from werkzeug.exceptions import HTTPException
import json


class NotFoundError(HTTPException):
    def __init__(self, status_code,  error_message):
        data = {"error_message": error_message}
        self.response = make_response(json.dumps(data), status_code)

        
class getVenue(Resource):
    @jwt_required()
    def get(self, id):
        venue = Venue.query.get(id)

        
        venue_data = []
        if venue:
            venue_data.append({
                    'id': venue.id,
                    'name': venue.name,
                    'address': venue.address,
                    'city': venue.city,
                    'state': venue.state,
                    'avg_venuerate':venue.avg_venuerate
                })
                
            return jsonify({'success': True,'venue_data':venue_data[0]})
        # return jsonify({'success': False,'venue_data':None})
        response = jsonify({'message': 'Venue not found','success': False,'venue_data':None})
        return make_response(response, 404)
        