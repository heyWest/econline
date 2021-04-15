from flask import Flask

app=Flask(__name__)

app.config['SECRET_KEY'] = 'facf980d98edffa2d563e876aba7a646'


from econline import routes
from econline.admin.routes import admin
from econline.voters.routes import voters

app.register_blueprint(admin)
app.register_blueprint(voters)