#!/usr/bin/awk -f

# A keyspace iterator for brute force, etc. This can be used, for example,
# in conjunction with a tool like curl to fetch https://site.com/*.html
# - Justin Parrott
#
# usage: ./ks [minlen [maxlen [string]]]
#
# Tested with nawk and gawk

function f(keyspace, kslen, prefix, count, i) {
	if (count > 1) {
		for (i = 1; i <= kslen; i++) {
			newpfx = sprintf("%s%c", prefix, keyspace[i])
			f(keyspace, kslen, newpfx, count - 1)
		}
	} else {
		for (i = 1; i <= kslen; i++)
			printf "%s%c\n", prefix, keyspace[i]
	}
}

BEGIN {
	minlen = 3
	maxlen = 8
	keyspacestr = "abcdefghijklmnopqrstuvwxyz"

	if (ARGC >= 2)
		minlen = ARGV[1]
	if (ARGC >= 3)
		maxlen = ARGV[2]
	if (ARGC >= 4)
		keyspacestr = ARGV[3]

	if (minlen > maxlen) {
		print "Minimum length is greater than maximum length"
		exit
	}

	n = split(keyspacestr, ksary, "")

	for (len = minlen; len <= maxlen; len++)
		f(ksary, n, "", len)

	exit;
}


