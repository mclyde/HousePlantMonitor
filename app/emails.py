from flask_mail import Message
from app import mail, db, models
from models import Communication
from flask import render_template
from decorators import async
from config import ADMIN

#To send email:
#import emails
#emails.sensor_notification(scout/sensor)

@async
def send_async_email(msg):
    try:
       mail.send(msg)
    except:
        pass

def send_email(subject, sender, recipient, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipient)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)

def sensor_notification(sensor):
    recipient = db.session.query(Communication).get(1)
    send_email("[House Plant Monitor] Scout: %s reading notification" % sensor.scout, ADMIN, [recipient.email], render_template("notification.txt", recipient = recipient, sensor = sensor), render_template("notification.html", recipient = recipient, sensor = sensor))
