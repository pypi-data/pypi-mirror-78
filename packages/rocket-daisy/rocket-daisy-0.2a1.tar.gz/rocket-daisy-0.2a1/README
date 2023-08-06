# Rocket-daisy

## Remote open control - key enabling technology for any ARM

---

Rocket is a user customizable remote control application intended mainly for electronics hobby projects.

Rocket connects 2 wheel drive remote control via WiFi (TCP). The network can be either in AP mode or STA mode. Using the APP you can control all movement directions plus arm and tool servos. In STA mode, your hobby target is a real Internet of Things device and can be controlled through WAN and LAN remotely.

> `Disclaimer: Don't use Rocket for life support systems or any other situations where system failure may affect user or environmental safety. Please don't use Rocket in projects where high-level security is required.`

All the commands send from Rocket are text strings, ending with command ending CR (carriage return), ASCII 13 which is hex code 0x4.
All required adjustments and command interpretations are stored and done in python.
Probably you will need to adapt the Rocket to meet the requirements of your hobby project. In that case you will need python knowledge regarding script and direction converter module adaptation.
In general Rocket depends, demands and uses integrated web server on target side. The URL of the web site depends on the network infrastructure. It is either  http://"your home ip address":8000 in STA, or http://192.168.4.1:8000 in AP mode.
By accessing the site for the first time you have to enter the default credentials: `user = webiopi password = raspberry`
After the log on accomplishing, on your browser appears website with joystick control. Each button use macros behind. Now you are able replace the demonstration code and achieve the desired functionality. 
Using this technique gives you the opportunity of debugging and testing your code in the office. As long as you working on the desktop environment, this could be the primary choice as well.
For the final release, controlling terrain car products requires mobile application. In this case the pilot need to disconnect from any other Wi-Fi networks and explicitly connect to the terrain car Access Point in order to control all functions.
The PyPi installation script gives you the opportunity to define/change the AP SSID and key by each sequential setup and ensure acceptable level of security.

I published recently google android app on the playstore, called "Rocket" https://play.google.com/store/apps/details?id=com.gulliversoft.rocket 
The "Rocket" allows you to trigger remotely any of the macros defined in your code, even they are not visible on the site.
In the current release V1.0, Rocket UI is capable with constrained range of 12 @daisy.macro commands.

###Commands

- `Forward()`
- `TurnLeft()`
- `Reverse()`
- `TurnRight()`
- `Stop()`
- `ArmUp()`
- `ArmDown()`
- `TiltUp()`
- `TiltDown()`
- `Lights()`
- `FlashAll()`
- `Move(short int, short int)`

##Setup
The easiest way of installing "Rocket", is to use the command `pip3 install rocket-daisy`. This requires you have access to internet.
After the pip3 execution is done, you need to call `python3 -m rocket`. The rocket logo appears after a while and the prompt requires your attention. The prompt `Access point SSID:` requests new WiFi identification for your hobby model.
In order to prevent collisions, you need unique name for each hobby model. In the next step you need to input new WPA password, which will be associated with the name you gave in the step before.
In the next steps the setup goes through python environment and services ensuring the rocket functionality on your platform.

---

Copyright 2020-2021 Martin Shishkov - gulliversoft, licensed under GPL3
