#!/usr/bin/python
import os
import json
import subprocess
import time
from datetime import datetime, date, timedelta
from temper import app

script_path = os.path.dirname(os.path.abspath(__file__))

def read_onewire_temps():
    '''
    Read in the output of /sys/bus/w1/devices/28-*/w1_slave
    NOTE: each OneWire device returns two lines of output.
    If the CRC check is bad, wait and try again (up to 20 times).
    Return the temp as a float, or None if reading failed.
    '''
    crc_ok = False
    tries = 0
    temps = []
    crc = []
    while not crc_ok and tries < 20:
        # Bitbang the 1-wire interface.
        s = subprocess.check_output('cat /sys/bus/w1/devices/28-*/w1_slave', shell=True).strip()
        lines = s.split('\n')
        data = zip(lines[0::2], lines[1::2])  # Convert lines into a list of tuples.
        device_count = len(data)
        for i in data:
            line0 = i[0].split()
            if line0[-1] == 'YES':  # CRC check was good.
                crc.append(True)
            else:
                crc.append(False)
        if all(crc):
            crc_ok = True
            for i in data:
                line1 = i[1].split()
                temps.append(round(float(line1[-1][2:])/1000, 1))
        else:
            crc = []
        # Sleep approx 20ms between attempts.
        time.sleep(0.02)
        tries += 1
    return temps


def log_temps():
    '''
    Log temperature readings to a files with a timestamp.
    For each temperature reading, open a file with today's date in /var/log/temps,
    then write the temp to it.
    Log name: temps_X_YYmmdd.log
    '''
    temps = read_onewire_temps()
    for idx, temp in enumerate(temps):
        logfile = '/'.join([app.config['TEMP_LOGS'], 'temps_{0}_{1}.log'.format(
            idx, datetime.strftime(datetime.now(), '%Y%m%d'))])
        f = open(logfile, 'a')
        f.write('{0},{1}\n'.format(datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S'), temp))
        f.close()


def read_log(log_date=None):
    '''
    Read in the temperature logs for the specifed date, split each line of comma separated values
    into a list of tuples and return them as a dict: {'sensor1': [(date, temp), ...], ...}
    log_date should be a valid Python date object.
    '''
    if not log_date:
        log_date = date.today()  # Use today's date instead.
    log_date = datetime.strftime(log_date, '%Y%m%d')
    logs = sorted(['/'.join([app.config['TEMP_LOGS'], f]) for f in os.listdir(app.config['TEMP_LOGS']) if log_date in f])
    d = {}
    for idx, log in enumerate(logs):
        temps = []
        f = open(log, 'r')
        for l in f.readlines():
            l = l.strip().split(',')  # Strip newline char, split on comma.
            if l[1] == 'None':  # Account for failed temp readings.
                pass
            else:
                temps.append((l[0], float(l[1])))
        # Finally add the temps to our dict.
        d[app.config['TEMP_SENSORS'][idx]] = temps
    return d


def read_n_logs(n=None):
    '''
    Read n days' worth of temperature log files.
    '''
    logs = {}
    # If n is specified, return only n logs.
    if n:
        n -= 1  # 1 becomes 0, so we return today's logs.
        while n >= 0:
            check_date = date.today() - timedelta(days=n)
            d = read_log(check_date)
            for k, v in d.iteritems():
                if k in logs:  # Sensor has existing data; merge it.
                    logs[k] += v
                else:  # No existing data for this sensor.
                    logs[k] = v
            n -= 1
    return logs


def read_gpio_config():
    '''
    Read the GPIO pin config from the config file.
    '''
    cfg = open(os.path.join(script_path, app.config['GPIO_CFG']), 'r')
    gpio = json.loads(cfg.readline())
    cfg.close()
    return gpio


def write_gpio_config(cfg):
    '''
    Write the GPIO pin config to the config file.
    '''
    if not isinstance(cfg, list):
        return
    cfg_file = open(os.path.join(script_path, app.config['GPIO_CFG']), 'w')
    cfg_file.write(json.dumps(cfg))
    cfg_file.close()
    return


if __name__ == "__main__":
    log_temps()
