from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import TimeField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from econline.models import Admin, Election
from flask_login import current_user
from datetime import datetime


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
    