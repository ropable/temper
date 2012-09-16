#!/usr/bin/python
import subprocess
import time
from datetime import datetime


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
    # Open a file with today's date in /var/log/temps, write the temp to it.
    f = open('/var/log/temps/temps_{0}.log'.format(datetime.strftime(datetime.now(), '%Y%m%d')), 'a')
    f.write('{0},{1}\n'.format(datetime.now().isoformat(), read_onewire_temp()))
    f.close()


if __name__ == "__main__":
    log_temp()
