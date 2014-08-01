from flask_mail import Message
from app import mail, db, models
from models import Communication
from flask import Flask, render_template
from decorators import async
from config import ADMIN, MAIL_PASSWORD
import smtplib
import re

#To send a text:
#import texts
#texts.sensor_notification(scout/sensor)


@async
def send_async_text(recipient, msg):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(ADMIN, MAIL_PASSWORD)
	server.sendmail('House Plant Monitor', recipient, msg)
	server.quit()


def send_text(recipient, text_body):
    msg = text_body
    send_async_text(recipient, msg)


def sensor_notification(sensor):
    recipient = db.session.query(Communication).get(1)
    if recipient.phone is not None and recipient.phone != '':
    	phone = recipient.phone + carrier_map(recipient.carrier)
    	send_text([phone], render_template("text.txt", recipient = phone, sensor = sensor))


def carrier_map(carrier):
	car = str(re.sub('[&-]', '_', carrier.lower()).replace(' ', '_'))

	if car == 'boost_mobile':
		return '@myboostmobile.com'
	elif car == 't_mobile':
		return '@tmomail.net'
	elif car == 'virgin_mobile':
		return '@vmobl.com'
	elif car == 'cingular':
		return '@cingularme.com'
	elif car == 'sprint_nextel':
		return '@messaging.sprintpcs.com'
	elif car == 'verizon':
		return '@vtext.com'
	elif car == 'nextel':
		return '@messaging.nextel.com'
	elif car == 'us_cellular':
		return '@email.uscc.net'
	elif car == 'suncom':
		return '@tms.suncom.com'
	elif car == 'powertel':
		return '@ptel.net'
	elif car == 'at_t':
		return '@txt.att.net'
	elif car == 'alltel':
		return '@message.alltel.com'
	elif car == 'metro_pcs':
		return '@MyMetroPcs.com'