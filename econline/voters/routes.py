from flask import Blueprint, render_template, url_for, flash
from econline.functions import confirm_token
from econline.models import Admin, Election, Candidate, Voter

voters = Blueprint('voters', __name__)

@voters.route('/voters/confirm/<token>')
def voters_landing(token):
    try:
        voter = confirm_token(token)
        voter = Voter.query.filter_by(email=voter).first()
        election = Election.qeury.filter_by(id=voter.election_id).first()
        
        
        return render_template('voters-landing.html', title=election.name)
    except:
        return "Invalid/Expired Token! Contact Administrators for help."
    # a special error page with a contact us form to the admin with a flashed message about their error


@voters.route('/voters/vote')
def voters_vote():
    return render_template('voters-vote.html')