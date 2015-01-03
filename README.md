M2More
======

M2More is an open source IOT software for M2M devices based on basic sensors.
The hardware platform selected to integrate the sensors and communications was the Raspberry PI.
The initial idea is create simple web services with the data of the sensors to read via Internet

M2More uses:
- Python (http://www.python.org)
- Tornado (http://www.tornadoweb.org)
- RPI.GPIO (http://sourceforge.net/projects/raspberry-gpio-python/)
- WebIOPI (https://code.google.com/p/webiopi/)
- Supervisor (http://www.supervisord.org)

To communicate with the devices inside a LAN from the Internet we configured NO-IP hosts (http://www.noip.com/).
Through NO-IP the dynamic IP of our LAN looks like a static IP and it is possible to access from outside of the LAN.
Only it is necessary to configure our Raspberry PI with a static IP and put web services in the HTTP port 80.

M2More RPiBIO v 0.1

![RPiBIOv01](https://raw.github.com/gmartinvela/M2More/master/M2More/utils/images/RPiBIOv01.jpg)
