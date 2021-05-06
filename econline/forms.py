from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SubmitField, IntegerField
from wtforms.fields.html5 import TimeField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from econline.models import Admin, Election, Voter
from flask_login import current_user
from datetime import datetime
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
    
class NewAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    def validate_username(self, email):
        user = Admin.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is not available')
            
            
class NewElectionForm(FlaskForm):
    name = StringField('Election Name', validators=[DataRequired(), Length(min=2, max=30)])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()], default=datetime.now())
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()], default=datetime.now())
    
    def validate_name(self, name):
        election = Election.query.filter_by(name=name.data).first()
        if election:
            raise ValidationError('That Election already exists!')
            
    def validate_start_date(self, start_date):
        if start_date.data < datetime.date(datetime.now()) or start_date.data > self.end_date.data:
            raise ValidationError('Check the dates')
    
    def validate_end_date(self, end_date):
        if end_date.data < datetime.date(datetime.now()):
            raise ValidationError('Check the dates')
            

class EditElectionNameForm(FlaskForm):
    name = StringField('Election Name', validators=[DataRequired(), Length(min=2, max=30)])
    submit_name = SubmitField('Submit Edit')
    
    def validate_name(self, name):
        election = Election.query.filter_by(name=name.data).first()
        if election:
            raise ValidationError('That Election already exists!')


class EditElectionDateForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()], default=datetime.now())
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()], default=datetime.now())
    submit_date = SubmitField('Submit Edit')
    
    def validate_start_date(self, start_date):
        if start_date.data < datetime.date(datetime.now()) or start_date.data > self.end_date.data:
            raise ValidationError('Check the dates')
    
    def validate_end_date(self, end_date):
        if end_date.data < datetime.date(datetime.now()):
            raise ValidationError('Check the dates')
            
            
class AddCandidateForm(FlaskForm):
    name = StringField('Candidate Name', validators=[DataRequired(), Length(min=2, max=100)])
    portfolio = SelectField(u'Portfolio', choices=[('President', 'President'), ('Vice President', 'Vice Preisdent'), ('Treasurer', 'Treasurer'), ('Financial Controller', ' Financial Controller'), ('General Secretary', 'General Secretary'), ('Coordinator', 'Coordinator'), ('Organizing Secretary', 'Organizing Secretary')])
    image_file = FileField('Candidate Picture', validators=[FileAllowed(['jpg', 'png'])])
    campus = SelectField(u'Campus', choices=[('Main', 'Main Campus'), ('City', 'City Campus')])
    
    
class ImportVotersForm(FlaskForm):
    voters = FileField('Import Voters', validators=[DataRequired(), FileAllowed(['csv'])])
    submit_voters = SubmitField('Import')
    

class VoterForm(FlaskForm):
    name = StringField('Voter Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    index_number = IntegerField('Index Number', validators=[DataRequired()])
    campus = SelectField(u'Campus', choices=[('Main', 'Main Campus'), ('City', 'City Campus')])
    level = SelectField(u'Level', choices=[('Level 100', 'Level 100'), ('Level 200', 'Level 200'), ('Level 300', 'Level 300'), ('Level 400', 'Level 400')])
    submit_voter = SubmitField('Submit')
    
    def validate_index_number(self, index_number):
        voter = Voter.query.filter_by(index_number=index_number.data).first()
        if voter:
            raise ValidationError('This Index Number is taken!')
    
    def validate_email(self, email):
        voter = Voter.query.filter_by(email=email.data).first()
        if voter:
            raise ValidationError('This Email is used by another voter!')
    

class EmailForm(FlaskForm):
    recipients = StringField('Email(s)', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    message = StringField('Message', widget=TextArea(), validators=[DataRequired()])
    send_email = SubmitField('Send Email')
    
    
class MassEmailForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    message = StringField('Message', widget=TextArea(), validators=[DataRequired()])
    send_mass = SubmitField('Send Email')
    
    
class IndexSearchForm(FlaskForm):
    index_number_search = IntegerField('Index Number', validators=[DataRequired()])
    search_index = SubmitField('Search')
    

class NameSearchForm(FlaskForm):
    name_search = StringField('Name', validators=[DataRequired()])
    search_name = SubmitField('Search')
    
    
class EmailSearchForm(FlaskForm):
    email_search = StringField('Email', validators=[DataRequired(), Email()])
    search_email = SubmitField('Search')
    
