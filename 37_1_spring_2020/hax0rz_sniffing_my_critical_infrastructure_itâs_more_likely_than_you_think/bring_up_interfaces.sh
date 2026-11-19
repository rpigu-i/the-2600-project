iw reg set DE
iw dev wlan0 set type ocb
ip link set wlan0 up
iw dev wlan0 ocb join 5900 10MHZ


