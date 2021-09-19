from flask import Flask, render_template
from datetime import timedelta

# setting up routes import
from .main.routes import main
from .admin.routes import admin
from .voters.routes import voters

# import extensions
from .extensions import *

# errorhandlers
from .errorhandlers import page_not_found
from .errorhandlers import method_not_allowed
from .errorhandlers import internal_server_error
from .errorhandlers import forbidden


#application factory design pattern
def create_app():
    app = Flask(__name__)

    app.config.from_object('config.DevelopmentConfig')

    # initializing extensions
    login_manager.init_app(app)
    login_manager.blueprint_login_views = {
        'admin': '/admin/login'
    }
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        app.permanent_session_lifetime = timedelta(minutes=300)
        app.register_blueprint(main)
        app.register_blueprint(admin)
        app.register_blueprint(voters)
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(405, method_not_allowed)
        app.register_error_handler(500, internal_server_error)
        app.register_error_handler(403, forbidden)

        return app






