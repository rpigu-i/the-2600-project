BOOTPART=$(mount |grep /boot |cut -d " " -f 1)
BOOTDEV=${BOOTPART:0:$((${#BOOTPART}-1))}

