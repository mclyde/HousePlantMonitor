from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	devices = [
			{'name':'light meter', 'pins':['1', '2', '3'], 'active':'true'},
			{'name':'soil moisture sensor', 'pins':['4', '5'], 'active':'true'}
	]
	return render_template("index.html", title = 'Home', devices = devices)
