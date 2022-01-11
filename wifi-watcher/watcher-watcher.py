"""watcher-watcher: watch the WiFi-watcher program for hangs

This program watches the wifi-watcher program in case it hangs. The wifi-watcher
program imports and uses RPi.GPIO, which occasionally hangs or freezes. This
can cause the Python program using it to hang or freeze. This program is a
simple forever-loop that uses systemctl, journalctl and psutil to confirm that
the wifi-watcher program is running and using incremental cpu time. If it is
not, then this program uses systemctl restart wifi-watcher to restart it.

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
from watcher import WatcherWatcher

TIME_BETWEEN_CHECKS = 100  # seconds between checks of wifi-watcher

def main():
    log = start_logging()
    ww = WatcherWatcher()
    try:
        log.info('Starting watcher-watcher.py')
        # forever event loop
        while True:
            # Make sure
            if ww.is_frozen():
                ww.restart_wifi_watcher()
            sleep(TIME_BETWEEN_CHECKS)
            
    except KeyboardInterrupt:
        log.warning('Ctrl-C was pressed.')
    except SystemExit:
        log.warning('SIGTERM was received.')
    except Exception as ex:  # traceback will appear in log
        log.exception('Unanticipated error with no Exception handler.')
    finally:
        log.info('Exiting watcher-watcher.py')

def start_logging():
    log = logging.getLogger()
    handler = logging.handlers.RotatingFileHandler('watcher-watcher.log',
        maxBytes=15000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s ~ %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    return log

if __name__ == '__main__' :
    main()
