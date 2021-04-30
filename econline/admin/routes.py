from flask import Blueprint
from flask import render_template, url_for, redirect, request, jsonify, make_response, flash
from flask_login import login_user, current_user, logout_user, login_required
from econline import bcrypt, db
import logging
from econline.models import Admin, Election, Candidate, Voter
from econline.functions import save_picture, send_mail, generate_confirmation_token
from econline.forms import LoginForm, NewAdminForm, NewElectionForm, EditElectionNameForm, EditElectionDateForm, AddCandidateForm, ImportVotersForm, EmailForm, MassEmailForm
import datetime
import csv
import io

admin = Blueprint('admin', __name__)

@admin.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_landing'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            return redirect(url_for('admin.admin_landing'))
        else:
            flash('Your email/password don\'t match.', 'danger')
            
    return render_template('admin-login.html', title="Admin Login", form=form)


@login_required
@admin.route('/admin/landing', methods=['POST', 'GET'])
def admin_landing():
    election_form = NewElectionForm()
    if request.method == "POST" and election_form.validate_on_submit():
        # converting dates and times to string then joining them
        start_at = election_form.start_date.data.strftime("%Y-%m-%d")+ " " + election_form.end_time.data.strftime("%H:%M")
        end_at = election_form.end_date.data.strftime("%Y-%m-%d") + " " + election_form.end_time.data.strftime("%H:%M")
        
        #chaging str back to datetime and inserting to db
        new_election = Election(name=election_form.name.data, start_at=datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M"), end_at=datetime.datetime.strptime(end_at, "%Y-%m-%d %H:%M"))
        db.session.add(new_election)
        db.session.commit()
        
        flash('New Election Added', 'success')
        return redirect(url_for('admin.admin_election', election_id=new_election.id))
    
    election_list = Election.query.all()
    
    return render_template("admin-landing.html", title="EC Landing", election_form=election_form, election_list=election_list)


@login_required
@admin.route('/admin/election', methods=['POST', 'GET'])
@admin.route('/admin/election/<election_id>', methods=['POST', 'GET'])
def admin_election(election_id):
    election = Election.query.filter_by(id=election_id).first()
    
    return render_template('admin-election.html', title=election.name, election=election)


@login_required
@admin.route('/admin/election/settings', methods=['POST', 'GET'])
@admin.route('/admin/election/settings/<election_id>', methods=['POST', 'GET'])
def election_settings(election_id):
    election = Election.query.filter_by(id=election_id).first()
    
    
    edit_name = EditElectionNameForm()
    if edit_name.submit_name.data and edit_name.validate_on_submit():
        election.name = edit_name.name.data
        db.session.commit()
        flash('Election Name Updated', 'success')
        return redirect(url_for('admin.election_settings', election_id=election.id))
    
    edit_date = EditElectionDateForm()
    if edit_date.submit_date.data and edit_date.validate_on_submit():
        start_at = edit_date.start_date.data.strftime("%Y-%m-%d")+ " " + edit_date.end_time.data.strftime("%H:%M")
        end_at = edit_date.end_date.data.strftime("%Y-%m-%d") + " " + edit_date.end_time.data.strftime("%H:%M")
        
        election.start_at = datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M")
        election.end_at = datetime.datetime.strptime(end_at, "%Y-%m-%d %H:%M")
        
        db.session.commit()
        flash('Election Date and Time Updated', 'success')
        return redirect(url_for('admin.election_settings', election_id=election.id))
    
    email_form = EmailForm()
    if email_form.send_email.data and email_form.validate_on_submit():
        emails = email_form.recipients.data.split(',')
        html = email_form.message.data
        subject = mail_form.subject.data
        for email in emails:
            send_mail(email, html, subject)
        
        flash('Email Sent', 'success')
        return redirect(url_for('admin.election_settings', election_id=election.id))
    
    mass_form = MassEmailForm()
    if mass_form.send_mass.data and mass_form.validate_on_submit():
        voters = Voter.qeury.filter_by(election_id=election.id).all()
        html = mass_form.message.data
        subject = mass_form.subject.data
        for voter in voters:
            send_mail(voter.email, html, subject)
        
        flash('Email Sent', 'success')
        return redirect(url_for('admin.election_settings', election_id=election.id))
        
        
    return render_template('election-settings.html', title=election.name, election=election, edit_name=edit_name, edit_date=edit_date, email_form=email_form, mass_form=mass_form)


@login_required
@admin.route('/admin/election/delete', methods=['POST'])
@admin.route('/admin/election/delete/<election_id>', methods=['POST'])
def election_delete(election_id):
    election = Election.query.filter_by(id=election_id).first()
    if election:
        db.session.delete(election)
        db.session.commit()
        flash('Election Deleted', 'info')
        return redirect(url_for('admin.admin_landing'))
    else:
        flash('Unable to Delete Election', 'warning')
        return redirect(url_for('admin.admin_landing'))
    

@login_required
@admin.route('/admin/election/candidates', methods=['POST', 'GET'])
@admin.route('/admin/election/candidates/<election_id>', methods=['POST', 'GET'])
def election_candidates(election_id):
    election = Election.query.filter_by(id=election_id).first()
    candidates = Candidate.query.filter_by(election_id=election.id).all()
    print(candidates)
    
    candidate_form = AddCandidateForm()
    if request.method=="POST" and candidate_form.validate_on_submit():
        if candidate_form.image_file.data:
            picture = save_picture(candidate_form.name.data, candidate_form.image_file.data)
            new_candidate = Candidate(election_id=election.id, name=candidate_form.name.data, portfolio=candidate_form.portfolio.data, campus=candidate_form.campus.data,
                                 image_file=picture)
        else:
            new_candidate = Candidate(election_id=election.id, name=candidate_form.name.data, portfolio=candidate_form.portfolio.data, campus=candidate_form.campus.data)
            
        db.session.add(new_candidate)
        db.session.commit()
        
        return redirect(url_for('admin.election_candidates', election_id=election.id))
    
    return render_template('election-candidates.html', title=election.name, election=election, candidates=candidates, candidate_form=candidate_form)


@login_required
@admin.route('/admin/election/<election_id>/candidate/<candidate_id>', methods=['POST', 'GET'])
def candidate_details(election_id, candidate_id):
    election = Election.query.filter_by(id=election_id).first()
    candidate = Candidate.query.filter_by(id=candidate_id).first()
    
    candidate_form = AddCandidateForm()
    if candidate_form.validate_on_submit():
        candidate.name = candidate_form.name.data
        candidate.portfolio = candidate_form.portfolio.data
        candidate.campus = candidate_form.campus.data
        
        if candidate_form.image_file.data:
            picture = save_picture(candidate_form.name.data, candidate_form.image_file.data)
            candidate.image_file = picture
        
        db.session.commit()
        flash('Candidate Details Updated', 'success')
        return redirect(url_for('admin.candidate_details', election_id=election.id, candidate_id=candidate.id))
    
    return render_template('candidate-details.html', title=election.name, election=election, candidate=candidate, candidate_form=candidate_form)


@login_required
@admin.route('/admin/election/candidate/delete', methods=['POST'])
@admin.route('/admin/election/<election_id>/candidate/delete/<candidate_id>', methods=['POST'])
def candidate_delete(election_id, candidate_id):
    candidate = Candidate.query.filter_by(id=candidate_id, election_id=election_id).first()
    
    if candidate:
        db.session.delete(candidate)
        db.session.commit()
        flash('Candidate Deleted', 'info')
        return redirect(url_for('admin.election_candidates', election_id=election_id))
    else:
        flash('Unable to Delete Election', 'warning')
        return redirect(url_for('admin.election_candidates', election_id=election_id))
    
    
@login_required
@admin.route('/admin/election/ballot', methods=['POST', 'GET'])
@admin.route('/admin/election/ballot/<election_id>', methods=['POST', 'GET'])
def election_ballot(election_id):
    election = Election.query.filter_by(id=election_id).first()
    
    return render_template('election-ballot.html', title=election.name, election=election)


@login_required
@admin.route('/admin/election/voters', methods=['POST', 'GET'])
@admin.route('/admin/election/voters/<election_id>', methods=['POST', 'GET'])
def election_voters(election_id):
    election = Election.query.filter_by(id=election_id).first()
    voters = Voter.query.filter_by(election_id=election.id).all()
    print(voters)
    # might change voters to obj so I can paginate it
    
    import_voters = ImportVotersForm()
    if request.method == "POST":
        f = request.files['voters']
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        
        for row in csv_input:
            voter = Voter(name=row[0], email=row[1], index_number=row[2], campus=row[3], election_id=election.id)
            db.session.add(voter)
            db.session.commit()
        
        return redirect(url_for('admin.election_voters', election_id=election.id))
    
    return render_template('election-voters.html', title=election.name, election=election, voters=voters, import_voters=import_voters)


@login_required
@admin.route('/admin/election/voters/delete', methods=['POST'])
@admin.route('/admin/election/voters/delete/<election_id>', methods=['POST'])
def delete_voters(election_id):
    voters = Voter.query.filter_by(election_id=election_id).all()
    if voters:
        for voter in voters:
            db.session.delete(voter)
            db.session.commit()

        flash('Voter Database Deleted', 'success')
    else:
        flash('No Voter Database detected!', 'danger')
    return redirect(url_for('admin.election_voters', election_id=election_id))


@login_required
@admin.route('/admin/election/analyse', methods=['POST', 'GET'])
@admin.route('/admin/election/analyse/<election_id>', methods=['POST', 'GET'])
def election_analyse(election_id):
    election = Election.query.filter_by(id=election_id).first()
    
    return render_template('election-analyse.html', title=election.name, election=election)


@login_required
@admin.route('/admin/election/launch', methods=['POST', 'GET'])
@admin.route('/admin/election/launch/<election_id>', methods=['POST', 'GET'])
def launch_election(election_id):
    election=Election.query.filter_by(id=election_id).first()
    voters = Voter.query.filter_by(election_id=election_id).all()
    
    election.status = "Ongoing"
    for voter in voters:
        unique_token = generate_confirmation_token(voter.email)
        voting_url = url_for('voters.voters_landing', token=unique_token, _external=True)
        html = "Voting has begun. Click on this link to vote: " + voting_url
        subject = "Vote for your BHJCR Executives"
        send_mail(voter.email, subject, html)
    
    db.session.commit()
    flash('The Voting Process has Begun!', 'info')
    return redirect(url_for('admin.election_settings', election_id=election.id))


@login_required
@admin.route('/admin/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))


@admin.route("/create", methods=['GET', 'POST'])
def create_admin():
    if request.authorization and (request.authorization.username == "admin" and request.authorization.password == "4xxvmt71dpwma3"):
        admin_list = Admin.query.all()
        form = NewAdminForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data).decode('utf-8')
                admin = Admin(email=form.email.data, password=hashed_password)
                db.session.add(admin)
                db.session.commit()
                
                flash('New Admin Added! Login', 'success')
                return redirect(url_for('admin.admin_login'))
            else:
                flash('New Admin not created! Check form!', 'danger')

        return render_template('create-admin.html', form=form, admin_list=admin_list)

    logging.warn(request.__dict__)
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@admin.route("/admin/<int:admin_id>/delete", methods=['POST','DELETE'])
def delete_admin(admin_id):
    if request.authorization and (request.authorization.username == "admin" and request.authorization.password == "4xxvmt71dpwma3"):
        admin = Admin.query.filter_by(id=admin_id).first()
        if admin:
            db.session.delete(admin)
            db.session.commit()
            flash('Admin deleted', 'success')
            return redirect(url_for('admin.create_admin'))
        else:
            flash('Admin does not exist!', 'danger')
            return redirect(url_for('admin.create_admin'))
        
    logging.warn(request.__dict__)
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})