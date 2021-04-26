from econline import app
from flask import render_template, url_for, session
from datetime import timedelta

@app.route('/')
def home():
    return render_template('index.html', title="Welcome")


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=300)
