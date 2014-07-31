from flask import render_template
from twitter import *

#To send a tweet
# from twitter import *
# make sure twitter tokens are valid for a developer account through twitter


def send_tweet(sensor):
	tweet = Twitter(auth=OAuth(app.config['TWITTER_TOKEN'], app.config['TWITTER_TOKEN_KEY'], app.config['TWITTER_CON_SEC'], app.config['TWITTER_CON_SEC_KEY']))  
	tweet.statuses.update(status=render_template("tweet.txt", sensor = sensor))