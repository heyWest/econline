from flask import Blueprint, render_template, url_for, flash, request, redirect
from app.functions import confirm_token
from app.models import Admin, Election, Candidate, Voter
from app.extensions import db

voters = Blueprint('voters', __name__)

@voters.route('/voters/confirm/<token>', methods=['POST', 'GET'])
def voters_landing(token):
    token = token
    try:
        email = confirm_token(token)
    except:
        flash("Your token has expired. Contact the EC Officials.")
        return redirect(url_for('home'))
    
    
    voter = Voter.query.filter_by(email=email).first()
    election = Election.query.filter_by(id=voter.election_id).first()
    
    if voter.confirmed:
        flash("You have already voted!", 'danger')
        return redirect(url_for('flash_error'))

    if election.status != "Ongoing":
        flash('This Election is unvavilable!', 'warning')
        return redirect(url_for('flash_error'))
    
    if voter.tries >= 3:
        flash('Too many authentication attempts. You have been blocked. Kindly contact the EC for clearance.')
        return redirect(url_for('flash_error'))
    
    
    if request.method == 'POST':
        index_number = request.form['index_number']
        campus = request.form['campus']
        
        voter = Voter.query.filter_by(index_number=index_number, email=email, campus=campus, has_voted=False).first()
        if voter:
            voter.confirmed = True
            db.session.commit()
            return redirect(url_for('voters.voters_vote', election_id=voter.election_id, index_number=index_number))
        else:
            flash('The inputed index/campus number is wrong!')
            voter.tries += 1
            db.session.commit()
            return redirect(url_for('voters.voters_landing', token=token))

    return render_template('voters-landing.html', title="Confirm Voter", token = token, voter=voter, election=election)
    

@voters.route('/voters/<election_id>/vote/<index_number>', methods=['POST', 'GET'])
def voters_vote(election_id, index_number):
    voter = Voter.query.filter_by(index_number=index_number).first()
    election = Election.query.filter_by(id=voter.election_id).first()
    if election.status != "Ongoing":
        flash('This Election is unvavilable!', 'warning')
        return redirect(url_for('flash_error'))
    
    if voter.confirmed == False:
        flash("You need to confirm your details. Check your mail!")
        return redirect(url_for('flash_error'))
    
    if voter.has_voted:
        flash("You have already voted!")
        return redirect(url_for('flash_error'))
    
    candidate = Candidate

    if request.method == 'POST':
        if voter.campus == "Main":
            # main campus candidates
            president_vote = request.form['votedPresidentMain']
            president_main = Candidate.query.filter_by(election_id=voter.election_id, campus=voter.campus, portfolio="President").first()
            if president_vote == "Yes":
                president_main.yes_votes +=1
                db.session.commit()
            else:
                president_main.no_votes += 1
                db.session.commit()

            vice_main_vote = request.form['votedVicePresidentMain']
            vice_main = Candidate.query.filter_by(election_id=voter.election_id, campus=voter.campus, portfolio="Vice President").first()
            if vice_main_vote == "Yes":
                vice_main.yes_votes += 1
                db.session.commit()
            else:
                vice_main.no_votes += 1
                db.session.commit()

            financial_vote = request.form['votedFinancial']
            financial = Candidate.query.filter_by(election_id=voter.election_id, campus=voter.campus, portfolio="Financial Controller").first()
            if financial_vote == "Yes":
                financial.yes_votes += 1
                db.session.commit()
            else:
                financial.no_votes += 1
                db.session.commit()

            #main but as array
            organa = request.form['votedOrganizing']
            organa_vote = Candidate.query.filter_by(election_id=voter.election_id, campus=voter.campus, name=organa).first()
            if organa_vote:
                organa_vote.votes_number += 1
                db.session.commit()

            general = request.form['votedGeneral']
            general_vote = Candidate.query.filter_by(election_id=voter.election_id, campus=voter.campus, name=general).first()
            if general_vote:
                general_vote.votes_number +=1 
                db.session.commit()


            voter.has_voted = True
            db.session.commit()

            return redirect(url_for('thank_you'))

        elif voter.campus == "City":
            #city campus candidates
            vice_city_vote = request.form['votedVicePresidentCity']
            vice_city = Candidate.query.filter_by(election_id=voter.election_id, campus=voter.campus, portfolio="Vice President").first()
            if vice_city_vote == "Yes":
                vice_city.yes_votes += 1
                db.session.commit()
            else:
                vice_city.no_votes += 1
                db.session.commit()

            treasurer_vote = request.form['votedTreasurer']
            treasurer = Candidate.query.filter_by(election_id=voter.election_id, campus=voter.campus, portfolio="Treasurer").first()
            if treasurer_vote == "Yes":
                treasurer.yes_votes += 1
                db.session.commit()
            else:
                treasurer.no_votes += 1
                db.session.commit()

            coordinator_vote = request.form['votedCoordinator']
            coordinator = Candidate.query.filter_by(election_id=voter.election_id, campus=voter.campus, portfolio="Coordinator").first()
            if coordinator_vote == "Yes":
                coordinator.yes_votes += 1
                db.session.commit()
            else:
                coordinator.no_votes +=1
                db.session.commit()


            voter.has_voted = True
            db.session.commit()

            return redirect(url_for('thank_you'))

    return render_template('voters-vote.html', title="Vote", voter=voter, candidate=candidate)