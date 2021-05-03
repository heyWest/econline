from flask import Blueprint, render_template, url_for, flash, request, redirect
from econline.functions import confirm_token
from econline.models import Admin, Election, Candidate, Voter

voters = Blueprint('voters', __name__)

@voters.route('/voters/confirm/', methods=['POST', 'GET'])
def voters_landing():
    if request.method == 'POST':
        index_number = request.form['index_number']
        voter = Voter.query.filter_by(index_number=index_number).first()
        
        if voter:
            return redirect(url_for('voters.voters_vote', election_id=1, index_number=index_number))
        else:
            flash('The inputted index number is wrong!')
            
        
    return render_template('voters-landing.html', title="Confirm Voter")
#    try:
#        voter = confirm_token(token)
#        voter = Voter.query.filter_by(email=voter).first()
#        election = Election.qeury.filter_by(id=voter.election_id).first()
#        if election.status != "Ongoing":
#           flash('This Election is unvavilable!', 'warning')
#           return redirect(url_for('home'))
#        
#        return render_template('voters-landing.html', title=election.name)
#    except:
#        return "Invalid/Expired Token! Contact Administrators for help."
    # a special error page with a contact us form to the admin with a flashed message about their error


@voters.route('/voters/<election_id>/vote/<index_number>', methods=['POST', 'GET'])
def voters_vote(election_id, index_number):
    election = Election.qeury.filter_by(id=voter.election_id).first()
    if election.status != "Ongoing":
        flash('This Election is unvavilable!', 'warning')
        return redirect(url_for('home'))
    
    
    if request.method == 'POST':
        listing = request.form['votedList']
        candidates = listing.split(',')
        for candidate in candidates:
            print(candidate) #use this to increase the vote tally for candidates!
            #put an if statement to check if the voter is there before increasing tally for times when someone chooses not to vote
    return render_template('voters-vote.html', title="Vote")