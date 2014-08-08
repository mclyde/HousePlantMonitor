# =======================================================================================
# Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
# Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
# =======================================================================================

from app import app, db, models
from app.Pynoccio import pynoccio
from flask import render_template, flash, url_for, redirect, Response, request, g, session
from flask_bootstrap import Bootstrap
from models import *
import sqlite3

def getStatus(troop, scout, pin):
	device = models.Device.query.filter_by(troop=troop, scout=scout, pin=pin).first()
	motor = models.Motor.query.filter_by(troop=troop, scout=scout, pin=pin).first()
	attrs = {}
	if device:
		attrs = {	'name':device.name,
					'pin':pin,
					'troop':troop,
					'scout':scout,
					'type':device.type,
					'atriggerupper':device.atriggerupper,
					'atriggerlower':device.atriggerlower,
					'dtrigger':device.dtrigger,
					'pollinginterval':device.pollinginterval,
					'text':device.text,
					'email':device.email,
					'tweet':device.tweet,
					'motor':device.motor,
					'this':'device'
		}
	elif motor:
		attrs = {	'name':motor.name,
					'pin':pin,
					'troop':troop,
					'scout':scout,
					'type':motor.type,
					'trig_time':motor.trig_time,
					'untrig_time':motor.untrig_time,
					'delay':motor.delay,
					'this':'motor'
		}

	return attrs

