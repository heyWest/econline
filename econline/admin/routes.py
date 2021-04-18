from flask import Blueprint
from flask import render_template, url_for

admin = Blueprint('admin', __name__)

@admin.route('/admin/login')
def admin_login():
    return render_template('admin-login.html', title="Admin Login")