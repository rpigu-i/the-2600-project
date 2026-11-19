#!/bin/sh
# Credit to Harrison Sand
# All I did was modify it to infinite loop
iw dev wlan0 ocb leave
while :
do
 for freq in $(cat freq.txt); do
  echo "$freq 10MHZ"
  iw dev wlan0 ocb join $freq 10MHZ
  sleep 1
  iw dev wlan0 ocb leave
  echo "$freq 5MHZ"
  iw dev wlan0 ocb join $freq 5MHZ
  sleep 1
  iw dev wlan0 ocb leave
 done
done


