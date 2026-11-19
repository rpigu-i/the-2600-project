#!/bin/bash
. /usr/share/scripts/liveos_boilerplate.sh
#
#  Written for Ninja OS by the development team.
#  licensed under the GPLv3 http://www.gnu.org/licenses/gpl-3.0.html
#
# This script runs at start up, stays resident and watches for the OS drive to
# be unplugged. If so it shuts the system down.

TICK=".0333"

tamper_reboot(){
    # This function reboots the machine if tampering is found with any of
    # components. We try a few shutdown methods until one sticks
    notify-send "Tampering Detected" "Rebooting..." --icon=software-update-urgent
    echo "Tampering Detected, Rebooting"
    /tmp/emergency_bin/busybox reboot -f
    /var/emergency_bin/busybox reboot -f
    /usr/bin/reboot -f
    systemctl --force reboot
}

tamper_check(){
    # This function checks if any of the binaries needed for emergency actions
    # are tampered with. busybox is needed for this script, and pv is needed for
    # zeroize.
    [ -f /tmp/emergency_bin/busybox ] || tamper_reboot
    [ -f /var/emergency_bin/pv ] || tamper_reboot
}
shutdown_check() {
   # If this script is killed by shutdown, regardless, it will reboot the system
   # Therefor the shutdown command will reboot. The solution is to check for
   # shutdown status before checking for tampering.
   local status_reboot=$(systemctl is-active systemd-reboot.service)
   local status_poweroff=$(systemctl is-active systemd-poweroff.service)
   [ $status_poweroff == "active" ] && poweroff -f
   [ $status_reboot == "active" ] && reboot -f
}

# If someone tries to disrupt the script while running, reboot.
trap "tamper_reboot" 1 2 9 15 17 19 23

while [ -b $BOOTDEV ];do
     # Every tick we check if the system has been tampered with
     shutdown_check
     tamper_check
     /tmp/emergency_bin/busybox sleep ${TICK}
done

#reboot the system.
/tmp/emergency_bin/busybox reboot -f

