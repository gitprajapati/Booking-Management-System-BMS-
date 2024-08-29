from flask import jsonify, request, make_response, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import  db, Show, Booking
import json
from datetime import datetime,timedelta
from werkzeug.utils import secure_filename
import os
from auth.role_selection import admin_required
from caching import cache


class shows(Resource):
    @jwt_required()
    @admin_required
    def post(self, id):
        try:
            data = json.loads(request.form['data'])
            print(data)
            image = request.files.get('image', None)
            name = data['name']
            form_start_date = data['start_date']
            start_date = datetime.strptime(form_start_date, '%Y-%m-%d').date()
            form_out_date = data['out_date']
            out_date = datetime.strptime(form_out_date, '%Y-%m-%d').date()
            duration = data['duration']
            capacity = data['capacity']
            tags = data['tags']
            price = data['price']
            caption = data['caption']

            if image:
                os.makedirs(os.path.dirname(current_app.config['UPLOAD_FOLDER']), exist_ok=True)
                image_name = secure_filename(image.filename)
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)
                save_image = image.save(path)
            else:
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'default_show_image.JPG')
            venue_id = id
            show = Show(name=name, capacity=capacity,start_date=start_date,out_date = out_date,duration=duration,image_path = image_path,tag=tags,price=price,caption=caption,venue_id=venue_id)
            
            db.session.add(show)
            db.session.commit()
            
            start_date_obj = start_date
            out_date_obj = out_date
            
            current_date = start_date_obj
            while current_date <= out_date_obj:
                date_str = current_date.strftime("%Y-%m-%d")
                booking = Booking(date=date_str, capacity=capacity, price=price, show_id=show.id)
                db.session.add(booking)
                current_date += timedelta(days=1)
            db.session.commit()
            cache.clear()
            return jsonify({'success': True, 'message': 'Show created successfully'})
        except Exception as e:
            db.session.rollback()
            error_msg = {'error': str(e)}
            return make_response(jsonify(error_msg), 400)
        finally:
            db.session.close()



    @jwt_required()
    def get(self, id):
        shows = Show.query.filter_by(venue_id = id).all()
        
        if shows:
            shows_data=[]
            for show in shows:
                if show.image_path:
                    image_url = request.host_url+show.image_path
                    
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
                    'venue_id': show.venue_id,
                    'show_image_url': image_url
                })
            return jsonify({'shows': True,'shows_data':shows_data})
        else:
            return {'error': 'Show not found.','shows': False,}, 404
        
    @jwt_required()
    @admin_required
    def delete(self, id):
        show = Show.query.get(id)
        if show:
            db.session.delete(show)
            db.session.commit()
            cache.clear()
            response = jsonify({'message': 'Show deleted successfully'})
            return make_response(response, 200)
        else:
            response = jsonify({'message': 'Show not found'})
            return make_response(response, 404)
        
    @jwt_required()
    @admin_required
    def put(self, id):
        show = Show.query.get(id)
        if show:
            data = json.loads(request.form['data'])
            name = data['name']
            duration = data['duration']
            capacity = data['capacity']
            tag = data['tag']
            price = data['price']
            caption = data['caption']
            if name:
                show.name = name
            if caption:
                show.caption = caption
            if tag:
                show.tag = tag
            if duration:
                show.duration = duration
            if price:
                show.price = price
            if capacity:
                    show.capacity = capacity       
            db.session.commit()
            
            response = jsonify({'success': True,'message': 'Show edited successfully'})
            return make_response(response, 200)
       
        else:   
            response = jsonify({'message': 'Show not found'})
            return make_response(response, 404)
