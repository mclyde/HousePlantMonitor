import serial
import io

def foo():
	connected = False
	ser = serial.Serial('/dev/tty.usbmodem1451', 115200, timeout=5)
	while not connected:
		serin = ser.read()
		if serin > 0:
			connected = True
	ser.write('1')
	while ser.read() == '1':	# Allow Python to do s.t. while Arduino is working
		ser.read()
	ser.close()
	return "Blinking complete"

def tempRead():
	connected = False
	ser = serial.Serial('/dev/tty.usbmodem1451', 115200, timeout=5)
	while not connected:
		serin = ser.read()
		if serin > 0:
			connected = True
	temp = ser.read()
	ser.close()
	return temp
