from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/admin/login')
def admin_login():
    return "Hello Admin!"