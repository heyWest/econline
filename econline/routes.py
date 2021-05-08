from econline import app
from flask import render_template, url_for, session, request, flash
from datetime import timedelta
from econline.functions import send_mail

@app.route('/')
def home():
    return render_template('index.html', title="Welcome")

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html', title="Thank You!")

@app.route('/error')
def flash_error():
    return render_template('flash-error.html', title="Oh No!")

@app.route('/contact-us', methods=['POST', 'GET'])
def contact_us():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        recipient = 'bhjcrelections21@gmail.com'
        html = message + " My email is: " + email
        subject = name + " - " + subject
        
        send_mail(recipient, subject, html)
        
        subject_1 = 'Email Received!'
        html_1 = 'We have received your email. Thank you for contacting us. \nThis is an automatic email. Please do not reply.'
        
        send_mail(email, subject_1, html_1)
        
        flash('The email has been sent!', 'success')
        
    return render_template('contact-us.html', title='Contact Us')

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