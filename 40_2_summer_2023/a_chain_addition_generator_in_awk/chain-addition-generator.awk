#!/bin/awk -f
#chain-add : A chain addition generator
#Thanks to Justin Parrott for the inspiration
BEGIN {
printf "Enter number of rounds: ";
getline rounds < "/dev/stdin";
printf "Enter key: ";
getline key < "/dev/stdin";
split(key, num, "");
len = length(num);
for (i=1;i<=rounds;i++){
num[len+i] = ((num[i]+num[i+1])%10);
printf num[len+i]};
print}


