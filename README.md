HousePlantMonitor
=================
A system to monitor houseplant health using a Pinoccio Scout (https://pinocc.io/) network and home server. Users will need at least one Pinoccio Scout device with at least one sensor (input device) wired in, such as a soil monitor, thermometer or photometer. The system can handle multiple devices, scouts and even troops simultaneously.

Once the dependencies are installed and the code pulled from Github, simply run the startup script run.py, then navigate to localhost:5000 in the browser of your choice. You will be able to use the configuration page to add the devices that are physically connected to the scouts into your local system and set their behavior.

##Components
Python (https://docs.python.org/2/license.html)

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
