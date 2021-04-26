from datetime import datetime
from econline import db, login_manager, app
from flask_login import UserMixin
import uuid

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(60), nullable = False)


class Election(db.Model):
    id = db.Column(db.String(20), primary_key=True, default=str(uuid.uuid4())[:8])
    name = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Building")
    votes_number = db.Column(db.Integer, nullable=False, default=0)
    

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    index_number = db.Column(db.Integer, unique=True, nullable=False)
    campus = db.Column(db.String(20), nullable=False)
    election_id = db.Column(db.String(20), db.ForeignKey('election.id'), nullable=False)
    

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.String(20), db.ForeignKey('election.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    portfolio = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    campus = db.Column(db.String(20), nullable=False)
    votes_number = db.Column(db.Integer, nullable=False, default=0)