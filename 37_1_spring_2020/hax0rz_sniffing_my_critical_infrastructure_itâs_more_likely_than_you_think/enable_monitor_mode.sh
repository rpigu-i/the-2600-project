iw dev wlan0 interface add wlan1 type monitor
ifconfig wlan1 up
# Enable promiscuous mode (not sure if this
# is necessary on both interfaces, shouldn't hurt either way)
ifconfig wlan0 promisc
ifconfig wlan1 promisc


