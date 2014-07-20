from app import app
from flask import render_template, flash, url_for, redirect, Response
import arduinoreaddemo

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html", title = 'Index')

@app.route('/config')
def config():
	presets = [
			{'name':'temp', 'pin':'A0'},
			{'name':'light', 'pin':'A1'},
			{'name':'button', 'pin':'13'}
	]
	return render_template("config.html", title = 'Sensor Configuration', presets = presets)

@app.route('/email')
def email():

	return render_template("email.html", title = 'Communication Settings')

@app.route('/readings')
def readings():

	return render_template("readings.html", title = 'Current Readings')

