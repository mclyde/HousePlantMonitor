from flask_wtf import Form
from wtforms import TextField, ValidationError, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required


# straight from the wtforms docs:
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = TextField('Number')


class CommunicationsForm(Form):
    email1 = TextField('Email Address 1', description='The email address you would like to recieve notifiactions.')
    email2 = TextField('Email Address 2', description='Optional secondary email address.')
    
    mobile_phone = FormField(TelephoneForm, description='The number you would like to scoutnet to sent notifications to.')

    submit_button = SubmitField('Submit Form')

    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')

