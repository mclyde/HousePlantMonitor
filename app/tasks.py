from app import app, db, threads
from app.Pynoccio import pynoccio
from models import Device, Motor
import threading
import time
import emails
import texts
import tweets


class MonitorThread(threading.Thread):
	def __init__(self, device):
		threading.Thread.__init__(self)
		self.device = device

	def run(self):
		monitor(self.device)



class ActionThread(threading.Thread):
	def __init__(self, motor):
		threading.Thread.__init__(self)
		self.motor = motor

	def run(self):
		action(self.motor)



def monitor(device):
	global threads, exitFlag
	while True and not exitFlag:
		time.sleep(device.pollinginterval)

		reading = get_reading(device.troop, device.scout, device.pin)

		print "Reading %s from device %s lower: %s upper: %s" % (reading, device.pin, device.atriggerlower, device.atriggerupper)
		if reading < device.atriggerlower or reading > device.atriggerupper:
			# Eventually want to send out message
			if device.text:
				print "send a text!\n"
				#texts.send_notification()

			if device.email:
				print "send an email!\n"
				#emails.send_notification()

			if device.tweet:
				print "send a tweet!\n"
				#tweets.send_tweet()
			
			#if device.motor is not None:
			#	motor = Motor.query.filter_by(id=device.motor).get(1)
				#motor.state = (not motor.state)
				#db.session.commit()
			#	t = ActionThread(motor)
			#	threads.append(t)
		

	#thread.exit()


def action(motor):
	print "Started %s motor!!\n" %(motor.name)
	#if motor.state: #last time it was triggered so effectively 'ON'
	#trigger
	#sleep for trig time + delay
	#turn off
	#sleep for untrig time




def setup():
	global threads, exitFlag
	exitFlag = 1
	devices = Device.query.all()
	for d in devices:
		t = MonitorThread(d)
		threads.append(t)
	start()


def start():
	global threads, exitFlag
	time.sleep(2)
	exitFlag = 0
	for thread in threads:
		thread.start()


def stop():
	global threads, exitFlag
	if threads is not []:
		exitFlag = 1
		for thread in threads:
			thread.join()

		threads = []





def get_reading(troopid, scoutid, pin):
	account = pynoccio.Account()
	account.token = app.config['SECURITY_TOKEN']

	account.load_troops()
        
	for t in account.troops:
		if t.id == troopid:
			for s in t.scouts:
				if s.id == scoutid:
				# might have to do a loop till we get a valid reading?
					reading = pynoccio.PinCmd(s).read(pin.lower())
					return reading.reply #.reply??
