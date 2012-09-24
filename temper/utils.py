#!/usr/bin/python
import os
import subprocess
import time
from datetime import datetime, date
from temper import app


def read_onewire_temp():
    '''
    Read in the output of /sys/bus/w1/devices/28-*/w1_slave
    If the CRC check is bad, wait and try again (up to 20 times).
    Return the temp as a float, or None if reading failed.
    '''
    crc_ok = False
    tries = 0
    temp= None
    while not crc_ok and tries < 20:
        # Bitbang the 1-wire interface.
        s = subprocess.check_output('cat /sys/bus/w1/devices/28-*/w1_slave', shell=True).strip()
        lines = s.split('\n')
        line0 = lines[0].split()
        if line0[-1] == 'YES':  # CRC check was good.
            crc_ok = True
            line1 = lines[1].split()
            temp = float(line1[-1][2:])/1000
        # Sleep approx 20ms between attempts.
        time.sleep(0.02)
        tries += 1
    return temp


def log_temp():
    '''
    Log a temperature reading to a file with a timestamp.
    '''
    # Open a file with today's date in /var/log/temps, write the temp to it.
    logfile = '/'.join([app.config['TEMP_LOGS'], 'temps_{0}.log'.format(datetime.strftime(datetime.now(), '%Y%m%d'))])
    f = open(logfile, 'a')
    f.write('{0},{1}\n'.format(datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S'), read_onewire_temp()))
    f.close()


def read_log(log_date=None):
    '''
    Read in the temperature log for the specifed date, split each line of comma separated values
    into a list of tuples and return them.
    '''
    # log_date should be a valid Python date object.
    if log_date:
        # Test to see if a log file exists for the nominated date.
        logfile = '/'.join([app.config['TEMP_LOGS'], 'temps_{0}.log'.format(datetime.strftime(log_date, '%Y%m%d'))])
    else:
        # Try using today's date instead.
        logfile = '/'.join([app.config['TEMP_LOGS'], 'temps_{0}.log'.format(datetime.strftime(date.today(), '%Y%m%d'))])
    if os.path.exists(logfile):
        # Open the logfile and iterate over it. Return a list of tuples:
        # (datetime_string, float)
        temps = []
        f = open(logfile, 'r')
        for l in f.readlines():
            l = l.strip().split(',')  # Strip newline char, split on comma.
            temps.append((l[0], float(l[1])))
        return temps
    else:
        return None


def read_logs(n=None):
    '''
    Read n number of temperature log files (or all files if n is None).
    '''
    logs = sorted(os.listdir(app.config['TEMP_LOGS']))
    temps = []
    if n and len(logs) > n:
        # Only return n logs.
        logs = logs[-n:]
    for log in logs:
        # Parse the date from the file name.
        log_date = datetime.strptime(log[6:14], '%Y%m%d')
        temps += read_log(log_date)
    return sorted(temps)


import json
def gpio_config():
    print os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    log_temp()
