import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    DEBUG = False
    
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV = 'development'
    SECRET_KEY = os.getenv('EC_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECURITY_PASSWORD_SALT =  os.getenv('SECURITY_PASSWORD_SALT')
    
    MAIL_SERVER = 'smtp.gmail.com'      # using google's mail service
    MAIL_PORT = 465 # well this is the mail port
    MAIL_USE_TL = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('BHJCR_MAIL')
    MAIL_PASSWORD = os.getenv('BHJCR_MAIL_PASSWORD')
    
    
class TestingConfig(BaseConfig):
    DEBUG = True
    

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "production_database_uri"


