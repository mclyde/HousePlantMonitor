# =======================================================================================
# Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
# Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
# =======================================================================================

from models import Communication, Carrier
from config import ADMIN, TWITTER_TOKEN, TWITTER_TOKEN_KEY, TWITTER_CON_SEC, TWITTER_CON_SEC_KEY
from app import mail, db, models
from flask_mail import Message
from decorators import async
from twitter import *
import re

#To send email:
#import notifications
#notifications.send_email(scout/sensor, reading)

#To send a text:
#import notifications
#notifications.send_text(scout/sensor, reading)

#To send a tweet
# from twitter import *
# make sure twitter tokens are valid for a developer account through twitter
#notifications.send_tweet(scout/sensor, reading)

htmlmsg = """
<p>{0}</p>
<p>{1} is reading: {2}!</p>
<hr>
<p><a href="http://127.0.0.1:5000/readings">readings</a> will show you more about {1}</p>
<p>Don't let your plants DIE!!</p>
<p>Regards,</p>
<p>Your friendly House Plant Monitor</p>
"""

txtmsg = """
{0} is reading: {1}

Don't let your plants DIE!!

Regards,
Your friendly House Plant Monitor
"""


tweetmsg = """
Notification from {0}

Reading: {1}
"""


@async
def send_async_email(msg):
    try:
       mail.send(msg)
    except:
        pass

def send_email(sensor, reading):
    recipient = db.session.query(Communication).get(1)
    subject = "[House Plant Monitor] Scout: {0} reading notification".format(sensor.name)
    msg = Message(subject = subject, sender = ADMIN, recipients = [recipient.email])
    msg.body = txtmsg.format(recipient.name, sensor.name, reading)
    msg.html = htmlmsg.format(recipient.name, sensor.name, reading)
    send_async_email(msg)


def send_text(sensor, reading):
    recipient = db.session.query(Communication).get(1)
    domain = get_carrier_domain(recipient.carrier)

    if recipient.phone is not None and recipient.phone != '' and domain is not None:
        phone = recipient.phone + domain
        subject = ""
        msg = Message(subject = subject, sender = ADMIN, recipients = [phone])
        msg.body = txtmsg.format(sensor.name, reading)
        send_async_email(msg)


def get_carrier_domain(carrier):
    c = str(re.sub('[&-]', '_', carrier.lower()).replace(' ', '_'))
    c = Carrier.query.filter_by(name=c).first()
    if c is not None:
        return c.domain
    return None



def send_tweet(sensor, reading):
    tweet = Twitter(auth=OAuth(TWITTER_TOKEN, TWITTER_TOKEN_KEY, TWITTER_CON_SEC, TWITTER_CON_SEC_KEY))  
    tweet.statuses.update(status=tweetmsg.format(sensor.name, reading))



