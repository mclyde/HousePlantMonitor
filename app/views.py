from app import app, db
from app.Pynoccio import pynoccio
from flask import render_template, flash, url_for, redirect, Response, request, g, session
from flask_bootstrap import Bootstrap
from twitter import *
from forms import CommunicationsForm, TelephoneForm
from models import Communication
import emails
import texts

#To send a tweet
# from twitter import *
# make sure twitter tokens are valid for a developer account through twitter
#tweet = Twitter(auth=OAuth(app.config['TWITTER_TOKEN'], app.config['TWITTER_TOKEN_KEY'], app.config['TWITTER_CON_SEC'], app.config['TWITTER_CON_SEC_KEY']))  
#tweet.statuses.update(status="Tweet sent from House Plant Monitor") 

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title = 'Home')

@app.route('/config')
def config():
	presets = [
			{'name':'temp', 'pin':'A0'},
			{'name':'light', 'pin':'A1'},
			{'name':'button', 'pin':'13'}
	]
	return render_template("config.html", title = 'Sensor Configuration', presets = presets)

@app.route('/communications', methods=['GET', 'POST'])
def communications():
    form = CommunicationsForm()

    if form.validate_on_submit():
        g.name = form.name.data
        g.email = form.email.data
        g.twitter = form.twitter.data
        g.phone = form.mobile_phone.number.data
        g.carrier = form.mobile_phone.carrier.data
        com = Communication(id = 1, name = g.name, email = g.email, twitter = g.twitter, phone = g.phone, carrier = g.carrier)
        db.session.merge(com)
        db.session.commit()
        flash('Communications Saved')
        return redirect(url_for('communications'))
    
    com = db.session.query(Communication).first()
    if com is not None:
        form.name.data = com.name
        form.email.data = com.email
        form.twitter.data = com.twitter
        form.mobile_phone.number.data = com.phone
        form.mobile_phone.carrier.data = com.carrier

    return render_template('communications.html', title = 'Communication Settings', form=form)

@app.route('/readings')
def readings():
    account = pynoccio.Account()
    account.token = app.config['SECURITY_TOKEN']

    account.load_troops()
        
    for t in account.troops:
        for s in t.scouts:
            islead = pynoccio.ScoutCmd(s).isleadscout
            if not islead.reply:
                var = pynoccio.PinCmd(s).report.analog
                #Now you can do what you want with the analog report   

    return render_template("readings.html", title = 'Current Readings')


@app.route('/show_scouts/')
def show_scouts():
    
    account = pynoccio.Account()

    account.token = app.config['SECURITY_TOKEN']

    account.load_troops()

    return render_template('scouts.html', title = 'Scouts Connected', troops = account.troops)
