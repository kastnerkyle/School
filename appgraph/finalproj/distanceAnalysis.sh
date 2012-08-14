#!/bin/bash
ngrams_dir=${1:-"grammified"}
filters_dir=${2:-"filters"}
distance_dir=${3:-"distances"}
base_dir=$(pwd)

get_filt_type() {
    echo ${1##*bf\.}
}

get_filt_family() {
    echo ${1%.*}
}

get_filt_name() {
    echo ${1%%.bf*}
}

get_gram_name() {
    echo ${1%%.gram*}
}

get_gram_type() {
    echo ${1##*gram\.}
}

get_distance() {
    pushd $base_dir 2>&1 > /dev/null
    echo $(./inBloom.pl $ngrams_dir/$1 $filters_dir/$2)
    popd 2>&1 > /dev/null
}

job () {
    echo "Start processing for $k"
    pushd ../$ngrams_dir 2>&1 > /dev/null
    for j in $(ls *.$2); do
        score=$(get_distance $j $1)
        echo $(get_gram_name $j),$2,$score >> ../$distance_dir/$(get_filt_name $1)
    done
    echo "$k processing complete"
    popd 2>&1 > /dev/null
}

if [[ ! -e $distance_dir ]]; then 
    mkdir -p $distance_dir
fi

pushd $filters_dir 2>&1 > /dev/null
max_jobs=8
for i in $(ls *.1); do
    if [[ -e $(get_filt_name $i) ]]; then
        echo "" > ../$distance_dir/$(get_filt_name $i) 
    fi 
    for k in $(get_filt_family $i).{1,2,3}; do
        job $k $(get_filt_type $k) &
        while [[ `jobs | wc -l` -gt max_jobs ]]; do 
           sleep 1
        done
    done
done
popd 2>&1 > /dev/null
