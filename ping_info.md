# Ping Info for detecting that the WiFi router is Down

When everything is working OK, a command from the shell like:

ping -c 3 google.com

will result in a returncode = 0 if ping worked; it will result in a

Man page for ping command. Some excerpts.

 -c count
    Stop after sending count ECHO_REQUEST packets. With deadline option, ping waits for count ECHO_REPLY packets, until the timeout expires.

    If ping does not receive any reply packets at all it will exit with code 1. If a packet count and deadline are both specified, and fewer than count
    packets are received by the time the deadline has arrived, it will also exit with code 1. On other error it exits with code 2. Otherwise it exits with
    code 0. This makes it possible to use the exit code to see if a host is alive or not.

Some experiments:
>>> c = ["ping", "-c", "3", "google.com"]
>>> import subprocess
>>> subprocess.run(c, capture_output=True, text=True)
CompletedProcess(args=['ping', '-c', '3', 'google.com'], returncode=0,
stdout='PING google.com (142.250.189.14) 56(84) bytes of data.\n
64 bytes from lax31s16-in-f14.1e100.net (142.250.189.14): icmp_seq=1 ttl=116 time=13.1 ms\n
64 bytes from lax31s16-in-f14.1e100.net (142.250.189.14): icmp_seq=2 ttl=116 time=13.3 ms\n
64 bytes from lax31s16-in-f14.1e100.net (142.250.189.14): icmp_seq=3 ttl=116 time=15.1 ms\n
\n
--- google.com ping statistics ---\n3 packets transmitted, 3 received, 0% packet loss, time 5ms\n
rtt min/avg/max/mdev = 13.081/13.839/15.148/0.929 ms\n',
stderr='')


>>> c = ["ping", "-c", "3", "rpi08"]  # rpi08 was known to be in a Host Down state
>>> subprocess.run(c, capture_output=True, text=True)
CompletedProcess(args=['ping', '-c', '3', 'rpi08'], returncode=1,
stdout='PING rpi08.lan (192.168.86.34) 56(84) bytes of data.\n
From rpi24.lan (192.168.86.39) icmp_seq=1 Destination Host Unreachable\n
From rpi24.lan (192.168.86.39) icmp_seq=2 Destination Host Unreachable\n
From rpi24.lan (192.168.86.39) icmp_seq=3 Destination Host Unreachable\n\n
--- rpi08.lan ping statistics ---\n3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 119ms\npipe 3\n',
stderr='')
>>> exit()

Will use both -c 3 parameter and test the returncode.
Further testing confirmed that returncode is type int.
