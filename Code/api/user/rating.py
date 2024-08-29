from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import  Show, Venue, Booking, db, User, Rating



class Rate(Resource):
    @jwt_required()
    def post(self,sid,vid):
        data = request.json
        showrate = data['showrate']
        venuerate = data['venuerate']
        user_email = get_jwt_identity()
        user = User.query.filter_by(email = user_email).first()


        show = Show.query.get(sid)
        venue = Venue.query.get(vid)
        user_id = user.id
        rating = Rating(show_id = sid,venue_id = vid, user_id=user_id,showrate= showrate,venuerate = venuerate)
        db.session.add(rating)
        db.session.commit()
        avg_showrate = 0
        avg_venuerate = 0
        showrate_sum = 0
        venuerate_sum =0
        all_ratings = Rating.query.all()
        for rating in all_ratings:
            showrate_sum = showrate_sum+ int(rating.showrate)
            venuerate_sum = venuerate_sum+ int(rating.venuerate)
        avg_showrate = round(showrate_sum/(len(all_ratings)),2)
        avg_venuerate = venuerate_sum/(len(all_ratings))
        bookings = Booking.query.filter_by(show_id = sid).all()

        if avg_showrate:
            for booking in bookings:
                show.avg_showrate = avg_showrate
                venue.avg_venuerate = avg_venuerate
                num_additional_stars = avg_showrate - 1
                price_multiplier = 1 + num_additional_stars * 0.1
                dynamic_price = int(int(show.price) * price_multiplier)
                booking.price = dynamic_price
            db.session.commit()

        return jsonify({'success':True})