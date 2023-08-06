#!/bin/bash

# Project skidloader
# This is the script required for autostarting
# all dependent executables
# and is getting called by rocket.services launcher
# at the boot time

# Author: Martin Shishkov
# Created : 05.03.2020
#

 echo "gulliversoft, starting rc priority loop"
 ln -s /dev/ttyUSB0 /dev/serial0;
 sudo $PWD/RIB_App & 
 tail -F /var/log/syslog | grep --line-buffered '(rib_support/src/socketHandler.cpp): Listening to server-socket: 0'|
	 {	read line;
		echo $line;
		echo "############# starting rocket-daisy";
		python3 -m rocket -c /etc/daisy/config &
		tail -F /var/log/syslog | grep --line-buffered 'provide-name: Remote_open_control_kit_enabled_target_(Rocket)Shm'|
			{	read line;
				echo $line;
				echo "############# starting digger consumer";
				sudo $PWD/Digger_Consumer_App &
				echo "############# starting motion";
				./motion -b;
				tail -F /var/log/syslog | grep --line-buffered 'motion_init: Started motion-stream server on ### gulliversoft ### RIB side channel with portforward'|
					{	read line; 
						echo $line;
						echo "############# starting motion consumer";
						sudo $PWD/Digger_Motion_Consumer_App; 
					};
			};
		exit 0;
	}
