from flask import jsonify, request, make_response, current_app, render_template, Response
import requests
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import  Show, Venue, Booking, db, bookedTicket, User
from datetime import datetime
import pdfkit
from caching import cache

def get_all_user_shows():
    return Show.query.join(Venue).add_columns(
        Show.id,
        Show.name,
        Show.tag,
        Show.start_date,
        Show.out_date,
        Show.duration,
        Show.caption,
        Show.price,
        Show.capacity,
        Show.venue_id,
        Show.image_path,
        Venue.name.label('venue_name')
    ).all()
class allShows(Resource):
    @jwt_required()
    @cache.cached(timeout=60, key_prefix='get_all_user_shows')
    def get(self):
        shows = get_all_user_shows()

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
                    'show_image_url': image_url,
                    'venue_name': show.venue_name
                })
            
            return jsonify({'shows': True,'shows_data':shows_data})
        else:
            return jsonify({'shows': False})
        
class bookingShow(Resource):
    @jwt_required()
    def get(self, id):
        show = Show.query.get(id)
        
        if show:
            shows_data=[]
            if show.image_path:
                    image_url = request.host_url+show.image_path
           
                
            shows_data.append({
                'id': show.id,
                'name': show.name,
                'tag': show.tag,
                'start_date': show.start_date,
                'out_date': show.out_date,
                'avg_showrate':show.avg_showrate,
                'duration': show.duration,
                'caption': show.caption,
                'capacity': show.capacity,
                'price': show.price,
                'venue_id': show.venue_id,
                'image_url': image_url,
                
            })
           
            return jsonify({'shows': True,'shows_data':shows_data[0]})
        else:
            return jsonify({'shows': False})


    @jwt_required()
    def post(self, id):
        data = request.json
        date = data['date']
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        
        booking = Booking.query.filter_by(show_id=id, date=date_obj).first()
        if booking:
            booking_data=[]
            
            
                
            booking_data.append({
                'id': booking.id,
                
                'date': booking.date,
                
                'capacity': booking.capacity,
                'price': booking.price,
                
            })
            
            return jsonify({'success': True,'booking_data':booking_data[0]})
        else:
            return jsonify({'success': False})


class purchase(Resource):
    @jwt_required()
    def post(self, id):

        data = request.json
        seat = data['seat']

        booking = Booking.query.get(id)
        if booking:
            capacity = booking.capacity
            remaining_seat = int(capacity)-int(seat)
            
            booking.capacity = remaining_seat
            db.session.commit()

            show = Show.query.get(booking.show_id)
            show_name = show.name
            booked_date = datetime.now()
            show_date = booking.date
            price = int(seat)*int(booking.price)
            
            
            tag = show.tag
            duration = show.duration
            image_path = show.image_path

            venue = Venue.query.get(show.venue_id)
            venue_name = venue.name
            venue_address = venue.address
            venue_city = venue.city
            
            email = get_jwt_identity()
            user = User.query.filter_by(email = email).first()
            first_name = user.first_name
            last_name = user.last_name
            user_email = user.email
            show_id = show.id
            venue_id = venue.id
            tktbooking = bookedTicket(venue_id=venue_id,show_id=show_id,user_email=user_email,first_name=first_name,last_name=last_name,venue_city=venue_city,venue_address=venue_address,venue_name=venue_name,image_path=image_path,duration=duration,tag=tag,price=price,show_date=show_date,booked_date=booked_date,show_name=show_name,seats=seat)
            db.session.add(tktbooking)
            db.session.commit()
            booked_table_id = tktbooking.id
            
            return jsonify({'success': True,'id':booked_table_id})
        response = jsonify({'message': 'Booking data not found.'})
        return make_response(response, 404)

class myBooking(Resource):
    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        mybooking = bookedTicket.query.filter_by(user_email = str(id)).all()
        

        booked_details = []
        for booking in mybooking:
            booked_details.append({
                'id':booking.id,
                'first_name': booking.first_name,
                'last_name':booking.last_name,
                'email': booking.user_email,
                'venue_city':booking.venue_city,
                'venue_address':booking.venue_address,
                'venue_name':booking.venue_name,
                'show_name': booking.show_name,
                'venue_id': booking.venue_id,
                'show_id':booking.show_id,
                'tag': booking.tag,
                'show_date':booking.show_date,
                'booked_date': booking.booked_date,
                'price': booking.price,
                'seats':booking.seats,
                
            })
        if len(booked_details) != 0:
            return jsonify({'success':True,'booked_details':booked_details})
        response = jsonify({'message': 'No Bookings made yet.'})
        return make_response(response, 404)
    
    def post(self, id):
        mybooking = bookedTicket.query.get(id)
        if mybooking:
            image_url = request.host_url+mybooking.image_path
            html = render_template('ticketPDF.html',image = image_url, venue_id=mybooking.venue_id,show_id=mybooking.show_id,user_email=mybooking.user_email,first_name=mybooking.first_name,last_name=mybooking.last_name,venue_city=mybooking.venue_city,venue_address=mybooking.venue_address,venue_name=mybooking.venue_name,image_path=mybooking.image_path,duration=mybooking.duration,tag=mybooking.tag,price=mybooking.price,show_date=mybooking.show_date,booked_date=mybooking.booked_date,show_name=mybooking.show_name,seats=mybooking.seats)
            pdf = pdfkit.from_string(html, False  )
            headers = {
                'Content-Type': 'application/pdf',
                'Content-Disposition': f"attachment;filename={mybooking.show_name}.pdf"
            }

            response = Response(pdf, headers=headers)
            return response
        else:
            response = jsonify({'message': 'No Ticket found.'})
            return make_response(response, 404)