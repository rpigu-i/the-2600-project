#!/bin/bash
#
# Written for the NinjaOS by the development team.
# licensed under the GPLv3 http://www.gnu.org/licenses/gpl-3.0.html
# Lets make our emergency parachute with our specially compiled stripped down
# version of busybox
mkdir /tmp/emergency_bin
cp /var/emergency_bin/busybox /tmp/emergency_bin/
# This is done at boot time, instead of install time because it puts the file in
# the top AUFS layer which is tmpfs which is in ram, which does not go away with
# the boot media is removed.
chmod 555 /tmp/emergency_bin/busybox

/etc/systemd.system/multi-user.target.wants/emergency_reboot.service
-----
[Unit]
Description=Emergency Parachute

[Service]
Type=simple
ExecStart=/usr/share/scripts/drive_watch.sh
ExecStop=/usr/bin/true
TimeoutStopSec=1
StandardOutput=tty
RemainAfterExit=no

[Install]
WantedBy=multi-user.target


/etc/systemd.system/multi-user.target.wants/parachute.service
-----
[Unit]
Description=Parachute for emergency RAM based shutdown
Before=NetworkManager.service

[Service]
Type=oneshot
ExecStart=-/usr/share/scripts/parachute.sh
TimeoutSec=0
StandardInput=tty
RemainAfterExit=yes

