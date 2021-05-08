import os
import threading
import time
import secrets
from PIL import Image
from flask_mail import Message
from econline import app, mail,db
from econline.models import Election
from itsdangerous import URLSafeTimedSerializer
import datetime


def start_end_election():
    while True:
        elections = Election.query.all()
        for election in elections:
            if election.start_at < datetime.datetime.now() and election.status == "Building":
                election.status = "Ongoing"
                db.session.commit()
            elif election.end_at < datetime.datetime.now():
                election.status = "Ended"
                db.session.commit()
        time.sleep(2)

#We start a thread instead of using asyncio...
t=threading.Thread(target=start_end_election)
t.start()
    

def save_picture(candidate_name,form_picture):
    random_hex = secrets.token_hex(3)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = candidate_name + random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/candidate_pictures', picture_fn)
    form_picture.save(picture_path)
    
    output_size = (500, 500) #minimizing the size of the image so it isn't saved so large in the database
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


def send_mail(to, subject, template):  # remember the send email at the registration route? Yeah ein this. Read on flask mails chale you'll be fine
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=('Business House Junior Common Room Elections 21', 'noreply@sender.com')
    )
    mail.send(msg)
    

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=864000):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email