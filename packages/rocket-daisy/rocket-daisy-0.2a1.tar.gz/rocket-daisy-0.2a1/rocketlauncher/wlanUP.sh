#############################################
#!/bin/bash Project rocket-sitara Remote controling of simatic iot2050 Reliable way to manage all modules together Created : 26.07.2020
#############################################

echo "##############- rocket launcher, copyright Shishkov 2020 -##############"
sleep 10
lspci -vnn -d 14e4:
sleep 1
tail -F /var/log/syslog | grep --line-buffered 'Kernel modules: bcma'| {
read line;
echo $line;
echo "######## RL step1 done, PCI device bcma 14e4 detected";
modprobe b43 pio=0 hwpctl=1 verbose=3 qos=0;
tail -F /var/log/syslog | grep --line-buffered 'b43-phy0 debug: Wireless interface started'| {
read line;
echo $line;
echo "######## RL step2 done, driver loaded, b43-phy0, Wireless interface started"
tail -F /var/log/syslog | grep --line-buffered 'b43-phy0 debug: Adding Interface type 2'| {
read line;
echo $line;
echo "######## RL step3, force up wifi";
rfkill unblock wifi;
sleep 5;
ip link set wlp1s0b1 up;
echo "############## wlp1s0b1 is up";
iw wlp1s0b1 set power_save off;
echo "wifi powersave disabled";
ifconfig wlp1s0b1 192.168.4.1;
echo "############## setting static ip of the wlan interface";
sleep 1;
echo "############ starting hostapd";
sudo hostapd -dd /etc/hostapd/hostapd.conf &
sudo bash ./rocketlauncherS.sh;
exit 0; };};}
