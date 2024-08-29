from flask import jsonify, request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Venue, User , db, Show
from caching import cache
from auth.role_selection import admin_required


def get_venues():
    return Venue.query.all()

class Venues(Resource):
    @jwt_required()
    @cache.cached(timeout=30, key_prefix='get_all_venue')
    def get(self):
        venues = get_venues()
        if not venues:
            return jsonify({'venues': False})

        venues_data = []
        for venue in venues:
                venue_data = {
                    'id': venue.id,
                    'name': venue.name,
                    'address': venue.address,
                    'city': venue.city,
                    'state': venue.state,
            
                    'shows': [
                        {
                            'id': show.id,
                            'name': show.name,
                            'tag': show.tag,
                            'start_date': show.start_date,  
                            'out_date': show.out_date,      
                            'duration': str(show.duration),
                            'caption': show.caption,
                            'price': show.price,
                            'capacity': show.capacity,
                        }
                        for show in venue.venue_shows 
                    ]
                }
                venues_data.append(venue_data)
        return jsonify({'venues': True, 'venue_data': venues_data})

    @jwt_required()
    @admin_required
    def post(self):
    
        user_email = get_jwt_identity()
        user = User.query.filter_by(email = user_email).first()
        
        try:
            data = request.json
            name = data['name']
            address = data['address']
            city = data['city']
            state = data['state']
            venue = Venue(name=name, address=address, city=city, state=state,owner_id = user.id)
            db.session.add(venue)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Venue created successfully'})
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        finally:
            cache.delete('get_all_venue')
            db.session.close()

    @jwt_required()
    @admin_required
    def put(self, id):
        venue = Venue.query.filter_by(id = id).first()
        if venue:
            try:
                data = request.json
                name = data['name']
                address = data['address']
                city = data['city']
                state = data['state']
                if name:
                    venue.name = name
                if address:
                    venue.address = address
                if city:
                    venue.city = city
                if state:
                    venue.state= state
                db.session.commit()
                return jsonify({'success': True, 'message': 'Venue edited successfully'})
            except Exception as e:
                db.session.rollback()
                error_msg = {'error': str(e)}
                return make_response(jsonify(error_msg), 400)
            finally:
                cache.delete('get_all_venue')
                db.session.close()
        else:
            error_msg = {'error': 'Venue does not exist.'}
            return make_response(jsonify(error_msg), 404)    
        
    @jwt_required()
    @admin_required
    def delete(self, id):
        venue = Venue.query.get(id)
        if venue is None:
            error_msg = {'error': 'Venue does not exist.'}
            return make_response(jsonify(error_msg), 404)
        Show.query.filter_by(venue_id=id).delete()
        db.session.delete(venue)
        db.session.commit()
        cache.delete('get_all_venue')
        
        return jsonify({'message': 'Venue deleted successfully'})