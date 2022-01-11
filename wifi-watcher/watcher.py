"""watcher.py -- Classes for Settings, Watcher, WatcherWatcher

Copyright (c) 2022 by Jeff Bass.
License: MIT, see LICENSE for more details.
"""

import os
import sys
import random
import logging
import logging.handlers
import traceback
import subprocess
from time import sleep

class Settings:
    """ Settings to Watch the WiFi for outages & restart the WiFi Router

    The Settings for various kinds of delays, etc. are hard coded in this class.
    While OK for this prototype, a more formal settings process will be needed.

    """

    def __init__(self):
        # set various delay and wait times; all are in seconds
        self.RPi = False  # True means running on RPi with GPIO pins; else testing
        self.random_ping = False  # True -> simulate pings instead of sending
        self.pin = 18  # GPIO pin for controlling the PowerTail
        self.wait_after_startup = 10  # don't do anything until router starts
        self.wait_for_ping_reply = 20  # ping should not take long
        self.delay_before_power_cycle = 15  # seconds to wait BEFORE power off
        self.time_power_off = 15  # seconds to hold power to router off
        self.time_between_checks = 30  # seconds between checks of WiFi status

class Watcher:
    """ Methods to Watch the WiFi for outages & restart the WiFi Router

    One Watcher is instantiated during the startup of the wifi-watcher.py
    program.

    The first principle is "First, Do No Harm".
    1. Assume the WiFi router is working until proven otherwise
    2. Don't send power cycle signals without appropriate delays
    3. Give the router time to restart after a power failure.

    Parameters:
        settings (Settings object): settings for wait times, power cycle times
    """

    def __init__(self, settings, log):
        # Is this startup due to a power failure? or due to a systemd restart?
        self.log = log
        global GPIO
        self.pin = settings.pin
        if settings.RPi:   # running on a real RPi with GPIO pins
            import RPi.GPIO as GPIO
        else:
            GPIO = dummy_GPIO()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)  # using GPIO Pin 18 for on / off
        GPIO.output(self.pin, False)  # turn on the router; this is Default
        if settings.random_ping:
            self.ping_internet_OK = self.random_ping_OK  # use for testing

    def wifi_down(self):
        # Determine is WiFi is down
        # if ping is OK, return false; if ping times out, retry one more time,
        # then if no response, return True
        if self.ping_internet_OK():
            return False
        sleep(10)
        if self.ping_internet_OK():
            return False
        else:
            return True

    def wifi_power_cycle(self, settings):
        """ Turns off the router using the GPIO pins

        This assumes that the PowerTail AC controller has been set to that
        the Default State is Power ON for the controlled plug. Sending NO
        Signal to the PowerTail AC controller leaves the power to the
        controlled AC plug On.

        Sending a True signal to the Signal Pin of the PowerTail will Turn Off
        the power to the controlled AC plug.

        Sending a False signal to the Signal Pin of the PowerTail will Turn On
        the power to the controlled AC plug.
        """
        sleep(settings.delay_before_power_cycle)
        GPIO.output(self.pin, True)  # turn off router
        sleep(settings.time_power_off)
        GPIO.output(self.pin, False)  # turn on the router
        self.log.warning('Power cycled router to restart it.')

    def ping_internet_OK(self):
        # use the linux "ping" command to get response from google.com.
        command = ["ping", "-c", "3", "google.com"]
        timed_out = False
        try:
            result = subprocess.run(command, timeout=15, capture_output=True)
        except subprocess.TimeoutExpired:
            timed_out = True
            print("Ping to Google TIMED OUT)")
            return False
        if result.returncode == 0:
            print("Pinged Google OK")
            return True
        else:
            print("Ping to Google FAILED")
            return False

    def random_ping_OK(self):
        num = random.randint(0,9)
        if num >= 6:
            print("Internet OK")
            return True
        else:
            print("NO PING")
            return False

    def closeall(self):
        # Close GPIO pins
        GPIO.cleanup()

class WatcherWatcher:
    """ Methods to Watch the wifi-watcher program

    These methods are stubs for initial testing; will update later
    """

    def __init__(self):
        pass

    def is_frozen(self):
        return False

    def restart_wifi_watcher(self):
        pass

class dummy_GPIO:
    """ Methods that allow software testing on computers that are not RPis
        and therefore don't have GPIO pins
    """
    def __init__(self):
        self.BCM = 'BCM'
        self.OUT = 'OUT'
        print("Set Up GPIO OK.")

    def setmode(self, mode):
        print("Set GPIO mode to", mode)

    def setwarnings(self, warn):
        print("Set GPIO warnings to", warn)

    def setup(self, pin, pin_mode):
        print("Set GPIO mode on", pin, "to", pin_mode)

    def output(self, pin, state):
        print("set GPIO pin", pin, "to", state)

    def cleanup(self):
        print("Closing GPIO")
