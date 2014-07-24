from flask_wtf import Form
from wtforms import TextField, ValidationError, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
import pdb

# straight from the wtforms docs:
class TelephoneForm(Form):
    number = TextField('Phone Number:')
    carrier = TextField('Carrier:')


class CommunicationsForm(Form):
    name = TextField('Username:', description='An unprotected username that will allow you to set up multiple notification endpoints.')
    email = TextField('Email Address:', description='The email address you would like to recieve notifiactions.', validators = [Required()])
    twitter = TextField('Twitter Username:', description='Twitter user to send notifications to.')
    
    mobile_phone = FormField(TelephoneForm, description='The number you would like to scoutnet to sent notifications to.')
    
    submit_button = SubmitField('Submit Form')

