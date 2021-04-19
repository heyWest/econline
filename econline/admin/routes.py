from flask import Blueprint
from flask import render_template, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required

from econline.models import Admin
from econline.forms import LoginForm

admin = Blueprint('admin', __name__)

@admin.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_landing'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data, password=form.password.data).first()
        if admin:
            login_user(admin)
            return redirect(url_for('admin.admin_landing'))
        else:
            flash('Your email/password is incorrect.')
            
    return render_template('admin-login.html', title="Admin Login", form=form)


@login_required
@admin.route('/admin/landing')
def admin_landing():
    return "Welcome Admin"


@login_required
@admin.route('/admin/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))