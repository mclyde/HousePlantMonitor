from app import db

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
	motor = db.relationship('Motor', backref = 'owner') # id of Motor

	def __repr__(self):
		return '<Device %r>' % (self.name)

class Communication(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    email = db.Column(db.String(120), index = True)
    twitter = db.Column(db.String(120))
    phone = db.Column(db.String(15))
    carrier = db.Column(db.String(120))

    def __repr__(self):
        return '<Communication %r>' % (self.name)

class Motor(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64))
	scout = db.Column(db.Integer, index = True)
	troop = db.Column(db.Integer, index = True)	
	type = db.Column(db.Text, index = True)
	pin = db.Column(db.String(2))
	trig_time = db.Column(db.Integer)				# milliseconds
	untrig_time = db.Column(db.Integer)				# milliseconds
	delay = db.Column(db.Integer)					# seconds
	state = db.Column(db.Boolean)					# 0 = last untrig 1 = last trig
	device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

	def __repr__(self):
		return '<Motor %r>' % (self.name)

class Soil():
	type = 'soil'

	def __init__(self, name, pin, troop, scout, mode):
		self.name = name
		self.pin = pin
		self.troop = troop
		self.scout = scout
		self.mode = mode




