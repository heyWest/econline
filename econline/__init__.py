from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os 


app=Flask(__name__)

#config
app.config['SECRET_KEY'] = os.environ['EC_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['EC_URI']


#instances
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)



#Importing routes
from econline import routes
from econline.admin.routes import admin
from econline.voters.routes import voters

app.register_blueprint(admin)
app.register_blueprint(voters)