#!/bin/bash

file=${1:-$(pwd)}
stages=${2:-"1"}
pushd $file

if [[ $stages -lt 2 ]]; then
    for i in $(grep .xml.gz sitemap-index.xml | sed -e "s|<loc>||g" -e "s|</loc>||g"); do
        wget $i
    done
    stages=1
fi

if [[ $stages -lt 3 ]]; then 
    for i in $(ls | grep -v sitemap-index.xml); do
        gunzip $i
    done
    stages=3
fi

if [[ $stages -lt 4 ]]; then
    eval writeout=$(dirs +1)
    grep --no-filename \<loc\> $(ls *.xml| grep -v sitemap-index) | sed -e "s|<loc>||g" -e "s|</loc>||g" > $writeout/sites.txt
    sed -e "1d" -i $writeout/sites.txt
    sed -e "/.*Wiki.*:/d" -e "/File.*:/d" -e "/Top_10.*:/d" -e "/.*_talk.*/d" -e "/.*User.*/d" -e "/.*Gracenote.*/d" -e "/.*Category.*/d" -e "/.*Talk:/d" -e "/.*Help.*/d" -e "/.*Template.*/d" -e "/.*Forum.*/d" -e "/.*Fans.*/d" -i $writeout/sites.txt
    stages=4
fi
popd
