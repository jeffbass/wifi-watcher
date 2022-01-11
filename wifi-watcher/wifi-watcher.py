"""wifi-watcher: watch WiFi for outage then power cycle the WiFi router

This program watches for outage of WiFi signal, using a ping to
google.com. If the ping fails, the WiFi router is not working and this program
will use a GPIO pin to turn a "PowerTail" AC switch off and then back on.

This program is run as a systemd service, so it will restart every the RPi does.

Copyright (c) 2022 by Jeff Bass.
License: MIT, see LICENSE for more details.
"""

import os
import sys
import logging
import logging.handlers
import traceback
from time import sleep
from watcher import Watcher, Settings

def main():
    log = start_logging()
    try:
        log.info('Starting wifi-watcher.py')
        settings = Settings()  # get settings timeout periods, etc.
        watcher = Watcher(settings, log)  # Instantiate a WiFi Watcher with settings
        sleep(settings.wait_after_startup)
        # forever event loop
        while True:
            # watch WiFi for outage
            if watcher.wifi_down():
                watcher.wifi_power_cycle(settings)
            sleep(settings.time_between_checks)

    except KeyboardInterrupt:
        log.warning('Ctrl-C was pressed.')
    except SystemExit:
        log.warning('SIGTERM was received.')
    except Exception as ex:  # traceback will appear in log
        log.exception('Unanticipated error with no Exception handler.')
    finally:
        if 'watcher' in locals():
            watcher.closeall() # close GPIO
        log.info('Exiting wifi-watcher.py')

def start_logging():
    log = logging.getLogger()
    handler = logging.handlers.RotatingFileHandler('wifi-watcher.log',
        maxBytes=15000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s ~ %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    return log

if __name__ == '__main__' :
    main()
