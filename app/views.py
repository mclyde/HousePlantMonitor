from app import app
from app.Pynoccio import pynoccio
from flask import render_template, flash, url_for, redirect, Response
from flask_bootstrap import Bootstrap
import forms
import email
#import arduinoreaddemo

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
     form = forms.CommunicationsForm()
     form.validate_on_submit()
     return render_template("email.html", title = 'Communication Settings', form=form)

@app.route('/readings')
def readings():

	return render_template("readings.html", title = 'Current Readings')


@app.route('/show_scouts/')
def show_scouts():
    account = pynoccio.Account()
    account.token = app.config['SECURITY_TOKEN']

    account.load_troops()

    return render_template('scouts.html', title = 'Scouts Connected', troops = account.troops)
