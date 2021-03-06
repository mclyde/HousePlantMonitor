# =======================================================================================
# Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
# Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
# =======================================================================================

from app import db


#To insert the default data for carriers
#INSERT into carrier (name, domain) VALUES('boost_mobile', '@myboostmobile.com'),('t_mobile', '@tmomail.net'),('virgin_mobile', '@vmobl.com'), ('cingular', '@cingularme.com'),('sprint_nextel', '@messaging.sprintpcs.com'),('verizon', '@vtext.com'),('nextel', '@messaging.nextel.com'),('us_cellular', '@email.uscc.net'),('suncom', '@tms.suncom.com'),('powertel', '@ptel.net'),('at_t', '@txt.att.net'),('alltel', '@message.alltel.com'),('metro_pcs', '@MyMetroPcs.com');

class Carrier(db.Model):
	__tablename__ = 'carrier'
	name = db.Column(db.String(120), index = True, primary_key = True)
	domain = db.Column(db.String(120))
	

class Communication(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    email = db.Column(db.String(120), index = True)
    twitter = db.Column(db.String(120))
    phone = db.Column(db.String(15))
    carrier = db.Column(db.String(120), db.ForeignKey('carrier.name'))

    def __repr__(self):
        return '<Communication %r>' % (self.name)


class Device(db.Model):
	id = db.Column(db.Integer, primary_key = True)	# Unique identifier so we can self reference the table for a motor
	name = db.Column(db.String(64))
	troop = db.Column(db.Integer, index = True)		# The troop id # (from Pinnocc.io HQ)
	scout = db.Column(db.Integer, index = True)		# The scout id # (from Pinnocc.io HQ) that the device is connected to
	type = db.Column(db.Text, index = True)			# e.g. soil, temp, light, etc.
	mode = db.Column(db.Integer)					# -1 DISABLED 0 INPUT, 1 OUTPUT, 2 INPUT_PULLUP
	pin = db.Column(db.String(2))					# e.g. D2, A4, etc.
	digital = db.Column(db.Boolean)					# 0 false 1 true
	dtrigger = db.Column(db.String(4))				# HIGH or LOW
	atriggerupper = db.Column(db.Integer)			# 0 to 1023 - upper threshold
	atriggerlower = db.Column(db.Integer)			# 0 to 1023 - lower threshold
	pollinginterval = db.Column(db.Integer)			# time to delay reports in minutes
	text = db.Column(db.Boolean)					# 0 false 1 true
	email = db.Column(db.Boolean)
	tweet = db.Column(db.Boolean)
	sentnotification = db.Column(db.Integer)		# 0 ok state, 1 low reading, 2 high reading
	motor = db.relationship('Motor', backref = 'device') # id of Motor

	def __repr__(self):
		return '<Device %r>' % (self.name)

class Motor(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64))
	scout = db.Column(db.Integer, index = True)
	troop = db.Column(db.Integer, index = True)
	type = db.Column(db.Text, index = True)
	mode = db.Column(db.Integer)
	pin = db.Column(db.String(2))					# -1 DISABLED 0 INPUT, 1 OUTPUT, 2 INPUT_PULLUP
	trig_time = db.Column(db.Integer)				# milliseconds
	untrig_time = db.Column(db.Integer)				# milliseconds
	delay = db.Column(db.Integer)					# seconds
	state = db.Column(db.Boolean)					# 0 = last untrig 1 = last trig
	device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

	def __repr__(self):
		return '<Motor %r>' % (self.name)

		
