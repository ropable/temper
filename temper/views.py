#!/usr/bin/python
import json
import subprocess
from datetime import datetime
from flask import request, render_template, jsonify
from operator import itemgetter
from temper import app, utils, cache


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temps')
#@cache.cached()
def temps_week():
    # Read up to 7 days-worth of log files.
    temps_li = utils.read_logs(n=7)
    current_temp = '{:.1f}'.format(temps_li[-1][1])
    return render_template('temp_graph.html', log_date=log_date, current_temp=current_temp, temps_li=json.dumps(temps_li))


@app.route('/temps/all')
@cache.cached()
def temps_all():
    # Read all log files.
    temps_li = utils.read_logs()
    current_temp = '{:.1f}'.format(temps_li[-1][1])
    return render_template('temp_graph.html', log_date=log_date, current_temp=current_temp, temps_li=json.dumps(temps_li))


@app.route('/temps/<int:year>/<int:month>/<int:day>')
@cache.memoize(timeout=60 * 60 * 24)  # Cache 24h
def log_date(year, month, day):
    # Read the log file for the specifed date.
    log_date = '{0}-{1}-{2}'.format(year, month, day)
    log_date = datetime.strptime(log_date, '%Y-%m-%d')
    temps_li = utils.read_log(log_date)
    current_temp = '{:.1f}'.format(temps_li[-1][1])
    return render_template('temp_graph.html', log_date=log_date, current_temp=current_temp, temps_li=json.dumps(temps_li))


@app.route('/leds')
def led_controller():
    # Read in the current GPIO pin config and pass it to the template.
    cfg = utils.read_gpio_config()
    return render_template('leds.html', gpio_config=cfg)


@app.route('/gpio_mode', methods=['POST'])
def gpio_mode():
    # Read the GPIO and mode arguments from the POST request.
    gpio = int(request.form['gpio'])
    mode = int(request.form['mode'])
    if gpio in app.config['GPIO_PINS'] and mode in [0, 1]:  # NOTE: mode == 0 evaluates to False. Duh!
        cfg = utils.read_gpio_config()
        i = map(itemgetter('gpio'), cfg).index(gpio)  # Index of the GPIO dict in the list.
        cfg[i]['mode'] = mode
        utils.write_gpio_config(cfg)
        subprocess.call('gpio -g write {0} {1}'.format(gpio, mode), shell=True)
        return jsonify({'gpio': gpio, 'mode': mode})
    else:
        return 'None'
