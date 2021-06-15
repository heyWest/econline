from flask import render_template, url_for, session, request, flash, Blueprint
from datetime import timedelta
from app.functions import send_mail

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
@main.route('/index')
def home():
    return render_template('home.html', title="Welcome")

@main.route('/thank-you')
def thank_you():
    return render_template('thank-you.html', title="Thank You!")

@main.route('/error')
def flash_error():
    return render_template('flash-error.html', title="Oh No!")

@main.route('/contact-us', methods=['POST', 'GET'])
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