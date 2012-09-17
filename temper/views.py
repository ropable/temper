from flask import request, render_template
from temper import app, utils
from datetime import datetime



@app.route('/')
def index():
    temps_list = utils.read_log()
    return render_template('index.html')

@app.route('/<int:year>/<int:month>/<int:day>')
def log_date(year, month, day):
    log_date = '{0}-{1}-{2}'.format(year, month, day)
    log_date = datetime.strptime(log_date, '%Y-%m-%d')
    return render_template('index.html', log_date=log_date)
