#!/bin/sh
#
# So someone mentioned wanting to "switch" tor exit nodes.  You
# can't really choose the node your existing instance of tor comes
# through, but what you can do is spawn a new instance of tor,
# giving you the option of (likely) a new exit node.  The more
# instances you spawn, the more exit-nodes you'll likely have to
# choose from.  Anyway, this script uses the idea to spawn several
# tor processes to scan a mark.  I used ncat for the sake of
# accessability.
#
# This script can also be used to directly scan onion addresses.
#
# Example: ./tscan.sh scanme.nmap.org
#
#    - Justin Parrott
#
# P.S. It appears that the connection timeout functionality of ncat
# doesn't have an effect when connecting through a proxy, so 
# scanning dark boxes takes a pretty long time; be patient.
#

NUMTHREADS=10	# number of parallel connects to run
STARTPORT=1	# start the scan at this target port
STOPPORT=1024	# stop the scan at this target port
NUMTORS=10	# number of tor instances we'll create
TORSP=9051	# NUMTORS tor processes listen starting here
VERBOSE=0	# show the failed connects also

usage() {
	echo "usage: $0 [options] host" >&2
	echo " -P torport     First tor port, intrements for each instance" >&2
	echo " -s startport   Where to start the scanning (port number)" >&2
	echo " -S stopport    Where to stop the scanning (port numberr)" >&2
	echo " -t numthreads  Number of connections to execute in parallel" >&2
	echo " -T numtors     Number of tor instances to start" >&2
	echo " -v             Verbose (print the closed ports as well)" >&2
	exit 1
}

while getopts P:s:S:t:T:v opt
do
	case "$opt" in
	P)	TORSP="$OPTARG";;
	s)	STARTPORT="$OPTARG";;
	S)	STOPPORT="$OPTARG";;
	t)	NUMTHREADS="$OPTARG";;
	T)	NUMTORS="$OPTARG";;
	v)	VERBOSE=1;;
	\?)	usage;;
	esac
done
shift $((OPTIND - 1))

if [ $# -ne 1 ]
then
	usage
fi
HOST="$1"

echo '# Spawning TOR processes' >&2
set --
i=0
while [ $i -lt $NUMTORS ]
do
	tor -f NONE --allow-missing-torrc --quiet \
	    SocksPort $((TORSP+i)) \
	    DataDirectory /tmp/tor-$i &
	set -- $@ $!
	i=$((i+1))
done
torprocs="$@"
echo "# Tor PIDs: $torprocs" >&2

echo '# Waiting 10 seconds for bootstrapping' >&2
sleep 10

tcping()
{
	ncat --proxy-type socks5 \
	    --proxy 127.0.0.1:$((TORSP+RANDOM%NUMTORS)) \
	    -z "$host" "$port" >/dev/null 2>&1
	if [ $? = 0 ]
	then
		echo "$port open"
	elif [ $VERBOSE -eq 1 ]
	then
		echo "$port closed"
	fi
}

echo '# Beginning scan' >&2
i="$STARTPORT"
running_threads=0
set --
while [ "$i" -le "$STOPPORT" ]
do
	port="$i" host="$HOST" tcping &
	set -- $@ $!
	running_threads=$((running_threads + 1))
	i=$((i+1))

	if [ $running_threads -eq "$NUMTHREADS" ]
	then
		while [ "$1" != "" ]
		do
			wait $1
			shift
		done
		running_threads=0
	fi
done

echo '# killing TOR processes' >&2
kill -INT $torprocs 2>/dev/null
wait

echo '# finished' >&2

#anyway, just a thought.. ymmv



