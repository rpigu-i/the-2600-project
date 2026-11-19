#!/bin/sh
 if [ ! -x /sbin/btsync ]
then
if [ ! -f /sbin/btsync ]; then
echo "BTSync not found"
else
echo "BTSync permissions not set"
fi
exit 0
fi

if [ ! -f /root/.sync/config.json ]; then
echo "Please create a config.json in /root/.sync/config.json"
echo "See http://btsync.s3-website-us-east-1.amazonaws.com/BitTorrentSyncUserGuide.pdf"

fi
 if [ "$1" = "stop" -o "$1" = "restart" ]
then
echo "Stopping the btsync server..."
killall btsync
fi
 if [ "$1" = "start" -o "$1" = "restart" ]
then
echo "Starting the btsync server..."
/sbin/btsync --config /root/.sync/config.json
fi

