wordlistcleanser.sh:

#!/bin/bash
#
# wordlistcleanser.   gerbil 2018 [twitter: @gerbilByte]
#
# This file is used to clean rockyou.txt from all the crap to leave just single words.
# It will also cleanse other wordlists too.
#
# Usage:
# wordlistcleanser.sh infile [outfile]
#
# WARNING: If an output file isn't specified, then the input will be overwritten (permissions allowing).
#
# Example:
# ./wordlistcleanser.sh /usr/share/wordlists/rockyou.txt ./wewillrockyou.txt

infile=$1
outfile=$2
version="1.0"
author="gerbil"

if [ $# -lt 1 ];
 then
 printf "\nwordlistcleanser v%s  -  %s 2018\n\nThis is a simple script that will remove \'phrases\', emails and websites from wordlist files.\nEmails and websites will be stored as files under the current directory.\n\n" ${version} ${author}
 printf "Usage:\n\t%s infile.txt [outfile.txt]\n\nWARNING: If an output file isn't specified, then the input will be overwritten (permissions allowing).\n\nExample:\n\t./wordlistcleanser.sh ./rockyou.txt ./wewillrockyou.txt\n\nHave fun! :)\n-%s\n" $0 ${author}
 exit
fi

baseinfile=`basename ${infile}`
baseinfile=${baseinfile%.*}
printf "Cleaning %s...\n" ${infile};

#Check input file exists... 
if ! [ -a ${infile} ];
 then #input file doesn't exist.
 printf "  %s doesn't exist!\n" ${infile}
 exit
fi

#Check if input file is to be overwritten or not...
if [ ${outfile}X == X ];
 then #no output file specified, therefore destruct mode! ;P
 outfile=${infile}
 printf "  No output file specified, therefore output will be stored at %s\n" ${outfile}
# rm -f ${infile} # just to save space
else
 printf "  Output file : ${outfile}\n"
fi

#Removing phrases...
printf "Removing phrases...\n"
grep -v ' ' ${infile} > /tmp/ry1.txt

#Extracting then removing websites...
printf "Extracting then removing websites...\n"
grep http[s]*:// /tmp/ry1.txt > ./${baseinfile}_websites.txt
grep -v http[s]*:// /tmp/ry1.txt > /tmp/ry2.txt
rm -f /tmp/ry1.txt # just to save space

#Extracting then removing emails...
printf "Extracting then removing emails...\n"
egrep '[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}' /tmp/ry2.txt > ./${baseinfile}_emails.txt
egrep -v '[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}' /tmp/ry2.txt > ${outfile}
rm -f /tmp/ry2.txt # just to save space

#Get stats on leftover file (length of each word and count of each, I know there are no words longer than 1000 characters)...
printf "Getting stats on %s, extracted emails and extracted websites...\n" ${outfile}
printf "Emails extracted: `wc -l ./${baseinfile}_emails.txt`\n" > ./${outfile%.*}_stats.txt
printf "Websites extracted: `wc -l ./${baseinfile}_websites.txt`\n" >> ./${outfile%.*}_stats.txt
printf "\nStats on %s : \n\n" ${outfile} >> ./${outfile%.*}_stats.txt
awk 'BEGIN{charcounts[1000]=0;len=0;printf("word length : count\n------------:------\n");}{charcounts[length($0)]++;}END{for(i=0;i<=1000;i++){printf("%11i : %i\n",i,charcounts[i]);}}' ${outfile} | grep -v ': 0'$ >> ./${outfile%.*}_stats.txt

printf "Cleansing completed.\n\n"



