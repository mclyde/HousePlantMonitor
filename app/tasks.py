from app import app, db, threads
from app.Pynoccio import pynoccio
from models import Device, Motor
from sqlalchemy.sql import text
import threading
import time
import notifications
from datetime import datetime


class MonitorThread(threading.Thread):
	def __init__(self, device, motors):
		threading.Thread.__init__(self)
		self.device = device
		self.motors = motors

	def run(self):
		monitor(self.device, self.motors)



class ActionThread(threading.Thread):
	def __init__(self, motors):
		threading.Thread.__init__(self)
		self.motors = motors

	def run(self):
		motor_controller(self.motors)



def monitor(device, motors):
	global threads, exitFlag

	while not exitFlag:
		wait_and_check(device.pollinginterval*60)

		if not exitFlag:
			print "Checking {0} at {1}".format(device.name, str(datetime.now()))
			reading = get_reading(device.troop, device.scout, device.pin)

			if reading < device.atriggerlower:
				handle_low_reading(device, reading, motors)
			elif reading > device.atriggerupper:
				handle_high_reading(device, reading, motors)
			else:
				# make sure everything is reset
				if device.sentnotification is not 0:
					device.sentnotification=0


#Constantly check if we should stop monitoring
def wait_and_check(t):
	global exitFlag

	n =  t/10

	for _ in range(n):
		if exitFlag:
			return
		time.sleep(10)


def handle_low_reading(device, reading, motors):
	global threads

	if device.sentnotification is not 1:
		# Send notification
		send_notification(device, reading)
		device.sentnotification=1

	# Turn on solenoid to open valve
	# Move a shade backwards
	if motors:
		for m in motors:
			# only want to water or open shade
			if m.state or m.type == "water":
				t = ActionThread(m)
				t.start()
				threads.append(t)


def handle_high_reading(device, reading, motors):
	global threads

	if device.sentnotification is not 2:
		# Send notification
		send_notification(device, reading)
		device.sentnotification=2

	# Move a shade forwards
	if motors:
		for m in motors:
			# we don't want to open the shade if it is open or over-water
			if not m.state and not m.type == "water":
				t = ActionThread(m)
				t.start()
				threads.append(t)
		


def send_notification(device, reading):

		if device.text:
			print "send a text! {0}\n".format(str(datetime.now()))
			notifications.send_text(device, reading)

		if device.email:
			print "send an email! {0}\n".format(str(datetime.now()))
			notifications.send_email(device, reading)

		if device.tweet:
			print "send a tweet! {0}\n".format(str(datetime.now()))
			notifications.send_tweet(device, reading)



def motor_controller(motor):
	if motor.type == "water":
		print "Triggering motor {0}  {1}".format(motor.name, str(datetime.now()))
		action(motor.troop, motor.scout, motor.pin, "HIGH")
		wait_and_check(motor.delay)
		print "Untriggering motor {0}   {1}".format(motor.name, str(datetime.now()))
		action(motor.troop, motor.scout, motor.pin, "LOW")
	else:
		if motor.state:
			print "Untriggering motor {0}   {1}".format(motor.name, str(datetime.now()))
			action(motor.troop, motor.scout, motor.pin, "LOW")
			time.sleep((motor.untrig_time/1000) + motor.delay)
			motor.state=0
		else:
			print "Triggering motor {0}   {1}".format(motor.name, str(datetime.now()))
			action(motor.troop, motor.scout, motor.pin, "HIGH")
			time.sleep((motor.trig_time/1000) + motor.delay)
			motor.state=1



def setup():
	global threads, exitFlag

	exitFlag = 1
	if not threads:
		devices = Device.query.all()
		for d in devices:
			t = MonitorThread(d, d.motor)
			threads.append(t)
		start()
		return True
	else:
		return False


def start():
	global threads, exitFlag
	time.sleep(2)
	exitFlag = 0
	with app.app_context():
		for thread in threads:
			thread.start()


def stop():
	global threads, exitFlag

	if threads is not []:
		exitFlag = 1
		for thread in threads:
			thread.join()
			thread.device.sentnotification=0
			db.session.merge(thread.device)
			db.session.commit()

		threads = []



def action(troopid, scoutid, pin, setting):
	account = pynoccio.Account()
	account.token = app.config['SECURITY_TOKEN']

	account.load_troops()
        
	for t in account.troops:
		if t.id == troopid:
			for s in t.scouts:
				if s.id == scoutid:
					result = pynoccio.PinCmd(s).write(pin, setting)
					while not result.reply:
						result = pynoccio.PinCmd(s).write(pin, setting)
					return




def get_reading(troopid, scoutid, pin):
	account = pynoccio.Account()
	account.token = app.config['SECURITY_TOKEN']

	account.load_troops()
        
	for t in account.troops:
		if t.id == troopid:
			for s in t.scouts:
				if s.id == scoutid:
					reading = pynoccio.PinCmd(s).read(pin.lower())
					while not reading.reply:
						reading = pynoccio.PinCmd(s).read(pin.lower())
					return reading.reply

