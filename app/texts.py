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
    domain = get_carrier_domain(recipient.carrier)

    if recipient.phone is not None and recipient.phone != '' and domain is not None:
    	phone = recipient.phone + domain
    	send_text([phone], render_template("text.txt", recipient = phone, sensor = sensor))


def get_carrier_domain(carrier):
	c = str(re.sub('[&-]', '_', com.carrier.lower()).replace(' ', '_'))
	c = Carrier.query.filter_by(name=c).first()
	if c is not None:
		return c.domain
	return None