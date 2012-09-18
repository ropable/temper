import json
from flask import request, render_template
from temper import app, utils
from datetime import datetime


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

'''
@app.route('/')
def index():
    temps_list = utils.read_log()
    return render_template('index.html', home_page=True)
'''

@app.route('/')
@app.route('/temps/')
def log_date_today():
    temps_li = utils.read_log()
    return render_template('temp_graph.html', log_date=log_date, temps_li=json.dumps(temps_li))

@app.route('/temps/<int:year>/<int:month>/<int:day>')
def log_date(year, month, day):
    log_date = '{0}-{1}-{2}'.format(year, month, day)
    log_date = datetime.strptime(log_date, '%Y-%m-%d')
    temps_li = utils.read_log(log_date)
    return render_template('temp_graph.html', log_date=log_date, temps_li=json.dumps(temps_li))

'''
@app.route('/api/temps/<int:year>/<int:month>/<int:day>')
def log_date(year, month, day):
    log_date = '{0}-{1}-{2}'.format(year, month, day)
    log_date = datetime.strptime(log_date, '%Y-%m-%d')
    return render_template('index.html', log_date=log_date)
'''
