# wifi-watcher

## Watch WiFi signal & reboot WiFi router if ability to see internet is absent

MIT License. Copyright (c) 2022 Jeff Bass. See LICENSE for details.

This is a prototype that runs on a Raspberry Pi Zero W. I may refine it into
a more robust program based on what is learned from the prototype.

The problem: My wife's dad is disabled. He lives 2,000+ miles away from us. My
wife monitors her dad and provides him guidance and help using a couple of
internet cameras and telephone calls. The monitoring works well when the
internet service is working correctly. But the router hangs and stops working
occasionally. As often as once every couple of days.

When my wife's dad's WiFi router occasionally "Freezes" and then his
house has no internet, she can't help him via the internet cameras and
iPad. Sometimes when this happens, the only thing that will fix it is to
unplug the router and plug it back in. That requires calling someone to
physically go to her dad's house to do that. Her dad is disabled and can't
unplug / replug the router himself. My wife has to call friends and relatives
to have someone drive over to help. It often takes a while for someone to come
and help, which means that there is no way to monitor her dad until the WiFi
router is restarted. (I find it shocking and disappointing that in 2022 there
are still internet providers whose modems and routers require manual power
cycling restart after a power failure or internet signal outage.)

The goal of this program is to watch for a working WiFi signal, using a ping to
google.com. If the ping fails, the WiFi router is not working and this program
will use a Raspberry Pi GPIO pin to turn a "PowerTail" AC switch off and then
back on. I modified the "PowerTail" AC switch per the instructions to have it
pass through the AC power with no signal from the RPi, and turn off the AC with
a GPIO pin signal from the RPi.

The main program loops forever and checks for working modem / router /
internet access by using the ping command to ping google.com. If there is not
a successful ping response, the router is assumed to be down and the program
power cycles the router and resumes the loop forever. There are timing delays
at each step so ensure that the router is not restarted too often and that
sufficient time is allowed for it to connect the internet after being
turned off and back on.

More information about the use of the ping command is
[here.](ping_info.md)

The program will start up when power is applied to the RPi or after power
outages using a systemd service. The wifi-watcher.service file is in this
folder. This file needs to be modified to point to the appropriate location of
the folder containing the wifi-watcher.py program.

## Project structure:
1. All code in in the wifi-watcher folder.
2. The main program is wifi-watcher.py
3. The watcher class is in watcher.py
4. Settings are "hardwired" in Settings class in watcher.py. All the settings
   such as how long to wait for a ping reply are in the Settings class. May
   change this to put settings into a YAML file later.
5. My virtual environment "wifi" contains python and all the needed modules.

## For Testing:

For testing on a Mac (as I do), these 2 settings are helpful. One allows running
the program without the GPIO library that runs only on a Raspberry Pi. The other
enables simulating pings and "shutting off" the modem.

```python
# these settings are in the Settings class in watcher.py
self.RPi = False  # True means running on RPi with GPIO pins; else testing
self.random_ping = True  # True -> simulate pings instead of sending
```

To run the program for testing, be sure to activate the appropriate virtual
environment.

```
cd wifi-watcher/wifi-watcher
workon wifi
python wifi-watcher.py
```

## For Production:

For running the program in production on a Raspebbery Pi, use the
[systemd service file](wifi-watcher.service).  Modify it to point to your
wifi-watcher.py program. Then copy it to the appropriate systemd service file
directory. Then run these commands at CLI prompt when logged in as user "pi"
with sudo privileges. Using systemd and systemctl is not hard. There are a lot
of resources and examples on the internet. Read them until you understand it.
Full details are in the man pages, but it is very hard to read the man pages
without a "big picture" understanding of systemd / systemctl and how they work.

All systemctl commands assume that the wifi-watcher service has been setup
correctly. The outline of how to do this is a few comment lines in the
wifi-watcher.service file.

```bash
sudo systemctl enable wifi-watcher  # run once to enable startup each reboot

sudo systemctl restart wifi-watcher  # starts or restarts the wifi-watcher.py

systemctl status wifi-watcher  # checks process status; sudo is unnecessary.
```

Also, for production on a Raspberry Pi, make sure the settings are appropriate.
In particular, you'll need to change these 2 settings after testing.

```python
# these settings are in the Settings class in watcher.py
self.RPi = True  # True means running on RPi with GPIO pins; else testing
self.random_ping = False  # False -> send actual pings to google.com
```

You will also need to change all the delay settings to values that are best for
your own modem / router. Be sure to allow enough time for the router to fully
reboot and reconnect to the internet. That can take a full 5 minutes on the
router I am writing this software to control.

## Dependencies and Installation

**wifi-watcher** has been tested with:

- Python 3.7.3 running on a Raspberry Pi Zero W
- Raspbian GNU/Linux 10 (buster) on the Raspberry Pi
- Python 3.9.9 running on a Mac (used for testing with appropriate settings)
- RPi.GPIO 0.6 and newer (imported only if using GPIO pins)
- A "PowerTail II" purchased from [Adafruit.](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-13-power-control)
  Other GPIO controlled AC power switches should work as well.

Later versions of these programs are likely to work, but haven't been tested by
me. If you get this working with other Raspian / RPi OS / Python / Rpi.GPIO
versions, consider making a pull request to add to the above list.  

## Contributing and asking questions

To contribute to this project, open a pull request. Please include appropriate
changes to the documentation if you make any changes to the code. To ask a
question, open an issue in this repository.
