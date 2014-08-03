# =======================================================================================
# Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
# Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
# =======================================================================================

from app import app, db, models
from app.Pynoccio import pynoccio
from flask import render_template, flash, url_for, redirect, Response, request, g, session
from flask_bootstrap import Bootstrap
from forms import CommunicationsForm, TelephoneForm, ConfigForm
from models import *
import emails
import texts
import tweets
import sqlite3

DEVICE_CLASSES = {
	'input':  ['Photometer', 'Soil Sensor', 'Thermometer'],
	'output': ['Email', 'Text Message', 'Tweet', 'Motor: Shades', 'Motor: Water']
}

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title = 'Home')

@app.route('/config')
def config():
	account = pynoccio.Account()
	account.token = app.config['SECURITY_TOKEN']
	account.load_troops()

	devices = models.Device.query.all()
	motors = models.Motor.query.all()

	troopPins = {}
	scoutPins = {}
	pins = {}
	for troop in account.troops:
		for scout in troop.scouts:

			#print 'class is ' + pynoccio.PinCmd(scout).report.digital.reply.__class__.__name__
			#help = pynoccio.PinCmd(scout).report.digital.reply
			#if isinstance(help, str):
			#	print 'help = ' + help

			# Handle inconsistent returns from Pinoccio API
			pinDTemp = pynoccio.PinCmd(scout).report.digital.reply
			while isinstance(pinDTemp, str):
				pinDTemp = pynoccio.PinCmd(scout).report.digital.reply	# get array of ints
			pinDModes = pinDTemp.mode
			pinATemp = pynoccio.PinCmd(scout).report.analog.reply
			while isinstance(pinATemp, str):
				pinATemp = pynoccio.PinCmd(scout).report.analog.reply
			pinAModes = pinATemp.mode
			# End handling

			for pinNum in range(0, 7):
				pinName = 'D'+`pinNum+2`
				device = models.Device.query.filter_by(pin=pinName, troop=troop.id, scout=scout.id).first()
				motor = models.Motor.query.filter_by(pin=pinName, troop=troop.id, scout=scout.id).first()
				if pinDModes[pinNum] < 0 or (not device and not motor):
					pins[pinName] = {'pin':pinName, 'power':'INACTIVE', 'device':None, 'mode': None}
				elif pinDModes[pinNum] == 0 or pinDModes[pinNum] == 2:
					pins[pinName] = {'pin':pinName, 'power':'ACTIVE', 'device':device.name, 'mode':'INPUT'}
				elif pinDModes[pinNum] == 1:
					pins[pinName] = {'pin':pinName, 'power':'ACTIVE', 'device':motor.name, 'mode':'OUTPUT'}
			for pinNum in range(0, 8):
				pinName = 'A'+`pinNum`
				device = models.Device.query.filter_by(pin=pinName, troop=troop.id, scout=scout.id).first()
				if pinAModes[pinNum] < 0 or (not device and not motor):
					pins[pinName] = {'pin':pinName, 'power':'INACTIVE', 'device':None, 'mode': None}
				elif pinAModes[pinNum] == 0 or pinAModes[pinNum] == 2:
					pins[pinName] = {'pin':pinName, 'power':'ACTIVE', 'device':device.name, 'mode':'INPUT'}
				elif pinAModes[pinNum] == 1:
					pins[pinName] = {'pin':pinName, 'power':'ACTIVE', 'device':motor.name, 'mode':'OUTPUT'}

			scoutPins[scout.name] = pins
			pins = {}
		troopPins[troop.name] = scoutPins

	return render_template("config.html", title = 'Sensor Configuration', troopPins = troopPins
		, troops = account.troops)

@app.route('/configform', methods=['GET', 'POST'])
def configform():
	form = ConfigForm()
	form.type.choices = DEVICE_CLASSES.get(form.type.data) or []

	if form.validate_on_submit():
		if form.deviceClass.data == 'output':
			print "HI"
		if form.deviceClass.data == 'input':
			print "BYE"
	return render_template('configform.html', title = 'Device Configuration')

@app.route('/communications', methods=['GET', 'POST'])
def communications():
    form = CommunicationsForm()

    if form.validate_on_submit():
        g.name = form.name.data
        g.email = form.email.data
        g.twitter = form.twitter.data
        g.phone = form.mobile_phone.number.data
        g.carrier = form.mobile_phone.carrier.data
        com = Communication(id = 1, name = g.name, email = g.email, twitter = g.twitter, phone = g.phone, carrier = g.carrier.lower())
        db.session.merge(com)
        db.session.commit()
        flash('Communications Saved')
        return redirect(url_for('communications'))
    
    com = db.session.query(Communication).first()
    if com is not None and com != []:
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

