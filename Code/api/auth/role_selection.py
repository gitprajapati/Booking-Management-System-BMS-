from functools import wraps
from flask import jsonify
from models import User 

from flask_jwt_extended import get_jwt_identity

from functools import wraps
from flask import jsonify, Response

def is_admin():
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()
    return current_user.roles[0].name == 'admin'

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not is_admin():
            response = jsonify(msg='Only admin can access.')
            response.status_code = 403
            return response
        result = fn(*args, **kwargs)
        if isinstance(result, Response):
            response = result
            if response.is_json:
                response_data = response.get_json()
                response_data['msg'] = 'Admin access granted'
                response.set_data(jsonify(response_data).get_data())
            return response
        return jsonify(result)
    return wrapper
