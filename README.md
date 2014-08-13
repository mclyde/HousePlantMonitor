HousePlantMonitor
=================
A system to monitor houseplant health using a Pinoccio Scout (https://pinocc.io/) network and home server. Users will need at least one Pinoccio Scout device with at least one sensor (input device) wired in, such as a soil monitor, thermometer or photometer. The system can handle multiple devices, scouts and even troops simultaneously.

Once the dependencies are installed and the code pulled from Github, simply run the database creation script db_create.py and then the startup script run.py. Navigate to localhost:5000 in the browser of your choice and you will be able to use the Configure Sensors page to add the devices that are physically connected to the scouts into your local system and set their behavior. Click the "Start Monitoring" button to begin the service, which will continue until you click the "Stop Monitoring" button or kill the process (e.g. ctrl-C in the terminal, shutting off the host machine, etc.) The browser need not remain open. All configuration settings will persist even when the server is stopped and devices may be added or deleted whether or not monitoring is in progress.

##Supported Devices
Analog soil moisture sensors, thermometers and photometers can be attached to analog pins (those beginning with 'A' on the Configure Sensors page). While an interface for digital input devices is in place, no such devices exist in the database as yet.

When an input device reading reaches one of the thresholds set during configuration, one of several behaviors may be triggered. If the user has entered his or her email, text or twitter contact information on the Communication Settings page any one of the relevant messages may be sent out as desired. For greater automation, the system also currently supports both analog and digital motors. Analog pins may be used to trigger a motor attached to a window shade to close at a certain threshold and reopen at another, or they may be set to activate a motor on a watering device that will disperse water for a fixed (configurable) amount of time. Digital pins may also be used to trigger a solenoid water spigot in the same way.

##Components
Python 2.7 (https://docs.python.org/2/license.html)

Flask (http://flask.pocoo.org/docs/license/)

Pinoccio API (https://docs.pinocc.io/ - public API)

Pynoccio (https://github.com/drogge/Pynoccio - no license)

JQuery (http://jquery.org/license)

JQueryUI (https://github.com/jquery/jquery-ui/blob/master/LICENSE.txt)

Bootstrap (https://github.com/twbs/bootstrap/blob/master/LICENSE)

##Dependencies
Users will need to download and install Python 2.7 and the following libraries:
* flask
* flask-bootstrap
* sqlalchemy
* flask-wtf
* flask-mail
* decorators
* twitter
* sqlite3

##Contribution and Use

Copyright Matt Clyde (mclyde@pdx.edu), Shawn Forgie (forgie@pdx.edu) and Blake Wellington (eblake@pdx.edu) 2014. All resources are available for use under the GPL v2 license (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE).
