#!/bin/sh

# Consider that perhaps nmap is unavailable to you, but netcat is.
# Netcat has scanning functionality, but it can be a little slow.
# This script will speed things up by running several instances of
# netcat in parallel.
#
#    - Justin Parrott

NUMTHREADS=10
TIMEOUT=3
STARTPORT=1
STOPPORT=1024

usage() {
	echo "usage: $0 [options] host"
	echo "  -s startport        Where to start the scanning (integer)"
	echo "  -S stopport         Where to stop the scanning (integer)"
	echo "  -t numthreads       Number of processes to execute in parallel"
	echo "  -w timeout          Timeout per connect (integer)"
	exit 1
}

while getopts s:S:t:w: opt
do
	case $opt in
	s)	STARTPORT="$OPTARG";;
	S)	STOPPORT="$OPTARG";;
	t)	NUMTHREADS="$OPTARG";;
	w)	TIMEOUT="$OPTARG";;
	\?)	usage;;
	esac
done
shift $((OPTIND - 1))

if [ $# -ne 1 ]
then
	usage
fi
HOST="$1"

tcping()
{
	nc -z -w "$to" "$host" "$port"
}

i="$STARTPORT"
running_threads=0
while [ "$i" -le "$STOPPORT" ]
do
	port="$i" host="$HOST" to="$TIMEOUT" tcping &
	running_threads=$((running_threads + 1))
	i=$((i+1))

	if [ $running_threads -eq "$NUMTHREADS" ]
	then
		wait
		running_threads=0
	fi
done

wait


