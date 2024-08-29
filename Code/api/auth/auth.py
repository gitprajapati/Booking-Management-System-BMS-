from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request,make_response, abort
from models import db,User,Role,UserRoles, TokenBlocklist
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from datetime import datetime,timedelta
from datetime import datetime
from datetime import timedelta


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('email', type=str, required=True)
parser.add_argument('password', type=str, required=True)
parser.add_argument('first_name', type=str, required=True)
parser.add_argument('last_name', type=str, required=True)
parser.add_argument('userType', type=str, required=True)

class registerAPI(Resource):
    def post(self):
        args = parser.parse_args()
        username = args.get('username')
        email = args.get('email')
        password = args.get('password')
        first_name = args.get('first_name')
        last_name = args.get('last_name')
        user_type = args.get('userType')
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return {'error': 'Email already registered.'}, 409
        password=generate_password_hash(
                password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=password, first_name=first_name,last_name=last_name)
        role = Role.query.filter_by(id=int(user_type)).first()
        new_user.roles.append(role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': 'Registration successful.'})
            
        
    def get(self):
        admin = UserRoles.query.filter_by(role_id = 1).first()
        if admin:
            return jsonify({'admin_exists': True})
        else:
            return jsonify({'admin_exists': False})

class LoginAPI(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.query.filter_by(email=email).first(
            )
        if user:
            if check_password_hash(user.password, password):
                create_access_token(identity = "user.email")
                access_token = create_access_token(identity = user.email, expires_delta=timedelta(minutes=34242))
                user.login_timestamp = datetime.now()
                db.session.commit()
                login_user(user, remember=True)

                return jsonify({"access_token":access_token,"status":True})
                
            else:
                return {'error': 'Incorrect password, please try again.'}, 401

        else:
            return {'error': 'Email does not exist.'}, 422
            

class getRole(Resource):
    @jwt_required()
    def get(self):
        user_email = get_jwt_identity()
        user = User.query.filter_by(email = user_email).first()
        user_roles = db.session.query(Role.id).join(User.roles).filter(User.id == user.id).first()

        role = user_roles[0]
        
        if role == 1:
            return jsonify({'role': "admin"})
        
        return jsonify({'role': "user"})
    
    
class LogoutApi(Resource):
    @jwt_required()
    def delete(self):
        user_email = get_jwt_identity()
        user = User.query.filter_by(email = user_email).first()
        user.logout_timestamp = datetime.now()
        jti = get_jwt()["jti"]
        now = datetime.now()
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return jsonify(msg="JWT token revoked")


