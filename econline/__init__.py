from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os 


app=Flask(__name__)

#config
app.config['SECRET_KEY'] = os.environ['EC_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['EC_URI']
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['SECURITY_PASSWORD_SALT'] = os.environ['SECURITY_PASSWORD_SALT']


#instances
db = SQLAlchemy(app)



login_manager = LoginManager(app)
login_manager.blueprint_login_views = {
    'admin' : '/admin/login'
}
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)


#mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TL'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ['BHJCR_MAIL']
app.config['MAIL_PASSWORD'] = os.environ['BHJCR_MAIL_PASSWORD']
mail = Mail(app)



#Importing routes
from econline import routes
from econline.admin.routes import admin
from econline.voters.routes import voters

app.register_blueprint(admin)
app.register_blueprint(voters)