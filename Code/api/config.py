class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite3'
    SECRET_KEY = "adaojdgpojpokdoiownvgowui3hr"
    SECURITY_PASSWORD_SALT = "fgwomrmwojgpoejpo'weow,lvg9402"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    JWT_SECRET_KEY = "gdokojdishriwp[[ote]FCNAJnndnUCFNJAV"
    UPLOAD_FOLDER = 'static/shows_image/'
    STATIC_FOLDER = 'static'
    JWT_SECRET_KEY = 'fsdifsdjvioihyfdrstfyui78efjvi'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS =  ['access', 'refresh']

class DevelopmentConfig(Config):
    DEBUG = True
