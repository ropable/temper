Overview
========

A simple web application to log, display and serve temperatures via a Raspberry Pi and 1-wire DS18B20 temperature probes.

Requirements
============

To use the DB18B20 devices, the Pi needs to be running the Adafruit [Occidentalis](http://learn.adafruit.com/adafruit-raspberry-pi-educational-linux-distro/occidentalis-v0-dot-2) distribution. This is a version of the Raspbian Wheezy distro with some additional hardware support thrown in.

Hardware
========

The DS18B20 temperature sensor(s) data line must be connected to GPIO #4 (pin 7), and a 4.7K pullup resistor must be installed between the data and VCC lines. Schematic:

|VCC    |Data   |Ground (DS18B20)
|       |       |
|       |       |
|-4.7K--|       |
|       |       |
|       |       |
|3V     |GPIO4  |Ground (Raspberry Pi)

You can chain additional sensors in parallel to the first, and you only need one resistor.

As root, run the following the attach the temperature submodule:

    modprobe w1-gpio
    modprobe w1-therm

After this, run cat /sys/bus/w1/devices/28-*/w1_slave to read the temperature data from the bus.
