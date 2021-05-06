from econline import app
from flask import render_template, url_for, session
from datetime import timedelta

@app.route('/')
def home():
    return render_template('index.html', title="Welcome")

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html', title="Thank You!")

@app.route('/error')
def flash_error():
    return render_template('flash-error.html', title="Oh No!")

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)

    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(403)
def internal_server_error(e):
    return render_template('403.html'), 403