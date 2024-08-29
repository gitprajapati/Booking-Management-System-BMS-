from flask import Flask
from flask_restful import Api
from caching import cache
from config import DevelopmentConfig
from models import db,User,Role, TokenBlocklist
from os import path
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from celery_worker import celery,ContextTask
from admin.venues import Venues
from auth.auth import registerAPI, LogoutApi,LoginAPI, getRole
from admin.shows import shows
from user.shows import bookingShow,purchase,myBooking, allShows
from user.venue import getVenue
from user.rating import Rate
from user.search import searchShow,searchVenue,ExportCSV



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


CORS(app,supports_credentials=True)

@app.after_request
def add_cors_headers(response):

    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    return response

@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response

db.init_app(app)

# ------------------------------JWT-------------------------


app.config["JWT_SECRET_KEY"] = "afsvfbnmnbfv"  

jwt = JWTManager(app)
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None
# ------------------------------Celery-------------------------
celery=celery

CELERY_BROKER_URL="redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/2"

celery.conf.update(
    broker_url="redis://127.0.0.1:6379/1",
    result_backend="redis://127.0.0.1:6379/2",
    timezone="Asia/Kolkata"
)

celery.Task=ContextTask
app.app_context().push()
# -----------------------------Caching--------------------------------

cache.init_app(app)

# ------------------------------Login manager-------------------------

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
# -----------------------------------API----------------------------------
api = Api(app)
api.init_app(app)
app.app_context().push()
# ----------------------------------------------------------------------------
@app.before_request
def create_tables():
    with app.app_context():
        if not path.exists('api/test.sqlite3'):
            db.create_all()
            admin_role = Role.query.filter_by(name='admin').first()
            user_role = Role.query.filter_by(name='user').first()

            if not admin_role:
                admin_role = Role(name='admin')
                db.session.add(admin_role)

            if not user_role:
                user_role = Role(name='user')
                db.session.add(user_role)

            db.session.commit()
database = create_tables()
database


api.add_resource(registerAPI, '/api/register')
api.add_resource(Venues, '/api/venues','/api/venues/<int:id>')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(getRole, '/api/check-role')
api.add_resource(shows, '/api/shows/<int:id>')
api.add_resource(allShows, '/api/allshows')
api.add_resource(bookingShow, '/api/showbooking/<int:id>')
api.add_resource(purchase, '/api/purchase/<int:id>')
api.add_resource(myBooking,'/api/mybooking','/api/mybooking/<int:id>')
api.add_resource(getVenue, '/api/venue/<int:id>')
api.add_resource(Rate,'/api/rating/<int:sid>/<int:vid>')
api.add_resource(searchShow,'/api/searchshow')
api.add_resource(searchVenue,'/api/searchvenue')
# api.add_resource(dotask, '/api/dotask')
api.add_resource(ExportCSV, '/api/exportcsv/<int:id>')
api.add_resource(LogoutApi, '/api/logout')

if __name__ == '__main__':
    app.run(debug = True)