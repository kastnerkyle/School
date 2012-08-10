#!/bin/bash

file=${1:-"sites.txt"}
lyrics=${2:-"lyrics"}
lines=$(perl -ne 'print if (rand() < .001)' $file)
for l in $lines; do
    #sleep for random time between 0 and 99
    sleepy=$[ ($RANDOM%100) ]
    echo "Sleeping for $sleepy seconds"
    sleep $sleepy
    name=$(echo $l | sed -e "s|http:.*com\/||g")
    echo "Fetching lyrics for $name"
    ./getLyrics.py $l > $lyrics/$name
done
