# =======================================================================================
# Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
# Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
# =======================================================================================

from app import app, db, models
from app.Pynoccio import pynoccio
from flask import render_template, flash, url_for, redirect, Response, request, g, session
from flask_bootstrap import Bootstrap
from forms import CommunicationsForm, TelephoneForm
from models import *
import emails
import texts
import tweets
import sqlite3
import tasks

ANALOG_PINS = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7']
DIGITAL_PINS = ['D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8']

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title = 'Home')

# ======================================================================
# Page to display all pins and their current states
# ======================================================================
@app.route('/config', methods=['GET'])
def config():
	account = pynoccio.Account()
	account.token = app.config['SECURITY_TOKEN']
	account.load_troops()

	troopPins = {}
	scoutPins = {}
	pins = {}
	for troop in account.troops:
		for scout in troop.scouts:

			# Handle inconsistent returns from Pinoccio API
			pinDTemp = pynoccio.PinCmd(scout).report.digital.reply
			while isinstance(pinDTemp, str):
				pinDTemp = pynoccio.PinCmd(scout).report.digital.reply
			pinDModes = pinDTemp.mode
			pinATemp = pynoccio.PinCmd(scout).report.analog.reply
			while isinstance(pinATemp, str):
				pinATemp = pynoccio.PinCmd(scout).report.analog.reply
			pinAModes = pinATemp.mode
			# End handling

			# Collect all digital pins for the scout
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

			# Collect all analog pins for the scout
			for pinNum in range(0, 8):
				pinName = 'A'+`pinNum`
				device = models.Device.query.filter_by(pin=pinName, troop=troop.id, scout=scout.id).first()
				motor = models.Motor.query.filter_by(pin=pinName, troop=troop.id, scout=scout.id).first()
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

# ======================================================================
# Configuration form for adding or changing a device or motor
# ======================================================================
@app.route('/configform/<troop>/<scout>/<pin>', methods=['GET', 'POST'])
def configform(troop, scout, pin):
	if request.method == 'POST':

		# TODO: Add delete device/motor option

		# Prepare scout object for Pinoccio API query
		account = pynoccio.Account()
		account.token = app.config['SECURITY_TOKEN']
		account.load_troops()
		account.troop(int(troop)).load_scouts()
		report_scout = account.troop(int(troop)).scout(int(scout))

		# Check DB for pin's previous device, if any
		current_device = models.Device.query.filter_by(troop=troop, scout=scout, pin=pin).first()
		current_motor = models.Motor.query.filter_by(troop=troop, scout=scout, pin=pin).first()

		# If the user chose to add an input device
		if request.form.get('deviceClass') == 'inputs':

			# Get current state of new device
			if pin in ANALOG_PINS:
				pinATemp = pynoccio.PinCmd(report_scout).report.analog.reply
				while isinstance(pinATemp, str):
					pinATemp = pynoccio.PinCmd(report_scout).report.analog.reply
				pinAStates = pinATemp.state
				digital = False

			elif pin in DIGITAL_PINS:
				pinDTemp = pynoccio.PinCmd(report_scout).report.digital.reply
				while isinstance(pinDTemp, str):
					pinDTemp = pynoccio.PinCmd(report_scout).report.digital.reply
				pinDStates = pinDTemp.state
				digital = True

			else:
<<<<<<< HEAD
				print "ERROR"			# TODO: Gracefully exit

			# TODO: Flash warning if pin STATE is disabled
=======
				print "ERROR"			# TODO
                
			threshold = request.form.get("threshold").split('-')
			lower = threshold[0].strip()
			upper = threshold[1].strip()
>>>>>>> b6ebdf19c9f59ad2a3b8297359956b7543f82fb6

			output_settings = request.form.get('triggerDevice')
			pynoccio.PinCmd(report_scout).makeinputup(pin)
			threshold_values = request.form.get('threshold').split("-")
			threshold_values = [int(element) for element in threshold_values]

			ref_motor = []
			if (output_settings != 'text' and output_settings != 'email' and output_settings != 'tweet'):
				ref_motor = [models.Motor.query.get(int(output_settings))]

			new_device = models.Device(
				name = request.form.get('deviceName') or 'Unnamed Sensor',
				troop = troop,
				scout = scout,
				type = request.form.get('subset'),
				mode = 2,
				pin = pin,
				digital = digital,
<<<<<<< HEAD
				dtrigger = request.form.get('dtrigger') or 'HIGH',
				atriggerupper = threshold_values[1] or 1023,
				atriggerlower = threshold_values[0] or 0,
				pollinginterval = request.form.get('pollingInterval') or 15,
=======
				dtrigger = 'HIGH',		# TODO
				atriggerupper = upper or 1023,	# TODO
				atriggerlower = lower or 0,		# TODO
				pollinginterval = request.form.get('polling'),	# TODO
>>>>>>> b6ebdf19c9f59ad2a3b8297359956b7543f82fb6
				text = True if output_settings == 'text' else False,
				email = True if output_settings == 'email' else False,
				tweet = True if output_settings == 'tweet' else False,
				motor = ref_motor
			)
			print new_device.name
			print new_device.scout
			print new_device.troop
			print new_device.type
			print new_device.mode
			print new_device.pin
			print new_device.digital
			print new_device.dtrigger
			print new_device.atriggerupper
			print new_device.atriggerlower
			print new_device.pollinginterval
			print new_device.text
			print new_device.email
			print new_device.tweet
			print new_device.motor
<<<<<<< HEAD

=======
            #print request.form.get('amount')
>>>>>>> b6ebdf19c9f59ad2a3b8297359956b7543f82fb6
			db.session.add(new_device)
			#out_motor = models.Motor.query.get(int(output_settings))
			#out_motor.device_id = models.Device.query.filter_by(troop=troop, scout=scout, pin=pin).first().id

		# If the user chose to add an output motor
		elif request.form.get('deviceClass') == 'outputs':

			# Get current state of new motor
			pinDTemp = pynoccio.PinCmd(report_scout).report.digital.reply
			while isinstance(pinDTemp, str):
				pinDTemp = pynoccio.PinCmd(report_scout).report.digital.reply
			pinDStates = pinDTemp.state
			# TODO: Flash warning if pin STATE is disabled

			pynoccio.PinCmd(report_scout).makeoutput(pin)
			new_motor = models.Motor(
				name = request.form.get('deviceName') or 'Unnamed Motor',
				scout = scout,
				troop = troop,
				type = request.form.get('subset'),
				mode = 1,
				pin = pin,
				trig_time = request.form.get('trigTime') or 1000,
				untrig_time = request.form.get('untrigTime') or 1000,
				delay = request.form.get('delay') or None,
				state = 0,
				device_id = None
			)
			print new_motor.name
			print new_motor.scout
			print new_motor.troop
			print new_motor.type
			print new_motor.mode
			print new_motor.pin
			print new_motor.trig_time
			print new_motor.untrig_time
			print new_motor.delay
			print new_motor.state
			print new_motor.device_id

			db.session.add(new_motor)

		else:
			print "ERROR"				# TODO: Gracefully exit
		if current_device:
			db.session.delete(current_device)
		if current_motor:
			db.session.delete(current_motor)
		db.session.commit()
		return redirect(url_for('config'))

	else:
		motorSet = models.Motor.query.all();
		motors = []
		for motor in motorSet:
			motors.append( {motor.name : motor.id} )
		motors = sorted(motors)

		return render_template('configform.html', title = 'Device Configuration'
			, motors = motors)

# ======================================================================
# Page to configure email, text and twitter settings
# ======================================================================
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

# ======================================================================
# Displays current readings of all input devices
# ======================================================================
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


# ======================================================================
# Make task start command available to clientside
# ======================================================================
@app.route('/startMonitoring', methods=['GET'])
def startMonitoring():
    tasks.setup()
    return Response("", status=200)

# ======================================================================
# Make task stop command available to clientside
# ======================================================================
@app.route('/stopMonitoring', methods=['GET'])
def stopMonitoring():
    try:
        stopped = tasks.stop()
        if stopped:
            return Response("", status=200)
    except Exception:
        pass
    return Response("", status=200)
