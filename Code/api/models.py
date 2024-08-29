from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import datetime
from sqlalchemy import Float


db = SQLAlchemy()

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id')) 


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200))
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=False)
    password = db.Column(db.String(200))
    created = db.Column(db.DateTime(), default=datetime.date.today())
    logout_timestamp = db.Column(db.DateTime())
    login_timestamp = db.Column(db.DateTime())
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary= 'user_roles', backref='roled',lazy = "subquery")

    
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)

class Role(db.Model,RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    avg_venuerate = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    venue_shows = db.relationship('Show', backref='venue', cascade='all',lazy = "subquery")

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tag = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.String(100), nullable=False)
    out_date = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(8))
    avg_showrate = db.Column(Float)
    capacity = db.Column(db.Integer, nullable=False)
    caption = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venue.id', ondelete="CASCADE"), nullable=False)
    image_path = db.Column(db.String(128))
    show_booking = db.relationship('Booking', backref='show', cascade='all',lazy = "subquery")

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id', ondelete="CASCADE"), nullable=False)

class bookedTicket(db.Model):
    __tablename__ = 'bookedticket'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(200))
    user_email = db.Column(db.String(50), nullable=False)
    venue_city = db.Column(db.String(50), nullable=False)
    venue_address = db.Column(db.String(50), nullable=False)
    venue_name = db.Column(db.String(50), nullable=False)
    show_name = db.Column(db.String(50), nullable=False)
    image_path = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(8))
    tag = db.Column(db.String(10))
    show_date = db.Column(db.String(100), nullable=False)
    booked_date = db.Column(db.DateTime())
    price = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)

class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer, nullable=False)
    showrate = db.Column(db.Integer, nullable=False)
    venuerate = db.Column(db.Integer, nullable=False)

