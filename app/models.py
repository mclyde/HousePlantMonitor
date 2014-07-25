from app import db

class Device(db.Model):
	id = db.Column(db.Integer, primary_key = True)	# Unique identifier so we can self reference the table for a motor
	name = db.Column(db.String(64))
	troop = db.Column(db.Integer, index = True)		# The troop id # (from Pinnocc.io HQ)
	scout = db.Column(db.Integer, index = True)		# The scout id # (from Pinnocc.io HQ) that the device is connected to
	type = db.Column(db.Text, index = True)			# e.g. soil, temp, light, etc.
	pin = db.Column(db.String(2))					# e.g. D2, A4, etc.
	digital = db.Column(db.Boolean)					# 0 false 1 true
	dtrigger = db.Column(db.String(4))				# HIGH or LOW
	atriggerupper = db.Column(db.Integer)			# 0 to 1023 - upper threshold
	atriggerlower = db.Column(db.Integer)			# 0 to 1023 - lower threshold
	pollinginterval = db.Column(db.Integer)			# time to delay reports in minutes
	text = db.Column(db.Boolean)					# 0 false 1 true
	email = db.Column(db.Boolean)
	tweet = db.Column(db.Boolean)
	motor = db.relationship('Device')				# link to an id of the Device table because a motor is just another device

	def __repr__(self):
		return '<Device %r>' % (self.name)
