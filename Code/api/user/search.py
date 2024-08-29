from flask import request, jsonify, Response, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import  Show,Venue
from tasks import *


# class dotask(Resource):
#     # @jwt_required()
#     def get(self):
#         c = add_together.delay(4,10)
#         c = str(c)
#         return c
    

class ExportCSV(Resource):
    def get(self,id):
        with app.app_context():
            task_result = exportCSV.delay(id)
            result = task_result.get()  

            if isinstance(result, dict) and 'message' in result:
                # The task returned an error message (e.g., 'Venue not found')
                return jsonify(result), 404

            headers = {
                'Content-Type': 'application/csv',
                'Content-Disposition': f"attachment;filename=csvfile.csv"
            }

            response = Response(result, headers=headers)
            return response
        

class searchShow(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        
        tag = data['tag']
        show_name = data['show_name']
        if not tag and not show_name:
            return {"message": "Please provide tag or show_name parameter."}

        
        if tag:
            shows = Show.query.filter(Show.tag == tag).all()
        elif show_name:
            shows = Show.query.filter(Show.name.ilike(f'%{show_name}%')).all()
        if shows:
            shows_data = []
            for show in shows:
                shows_data.append({
                    'id': show.id,
                    'name': show.name,
                    'tag': show.tag,
                    'start_date': show.start_date,
                    'out_date': show.out_date,
                    'duration': show.duration,
                    'caption': show.caption,
                    'price': show.price,
                    'capacity': show.capacity,
                    'avg_showrate':show.avg_showrate

                    
                })
            return jsonify({'success': True,'shows_data':shows_data})
        if len(shows) == 0:
            response = jsonify({'message': 'No matching show found.', 'success':False})
            return make_response(response, 404)


class searchVenue(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        venue_name = data['venue_name']        
        venues = Venue.query.filter(Venue.name.ilike(f'%{venue_name}%')).all()
        if venues:
            venues_data = []
            for venue in venues:
                venues_data.append({'id': venue.id,
                    'name': venue.name,
                    'address': venue.address,
                    'city': venue.city,
                    'state': venue.state,
                    'avg_venuerate':venue.avg_venuerate})
            return jsonify({'success': True,'venues_data':venues_data})
        if len(venues) == 0:
            response = jsonify({'message': 'No matching venues found.', 'success':False})
            return make_response(response, 404)
