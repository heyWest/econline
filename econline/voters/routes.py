from flask import Blueprint

voters = Blueprint('voters', __name__)

@voters.route('/voters')
def voters_landing():
    return "Hello Voter!"