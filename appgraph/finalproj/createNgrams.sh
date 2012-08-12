#!/bin/bash


lyrics_dir=${1:-"lyrics"}
out_dir=${2:-"grammified"}
ngrams_prog=${3:-"ngrams/ngrams"}

if [[ ! -e $out_dir ]]; then
    mkdir -p $out_dir
fi

run_ngram() {
    #$1 is the lyrics directory, $2 is the filename
    gram_count=3
    $ngrams_prog --type=word --n=$gram_count --in=$1/$2 > $out_dir/$2.gram
}

cleanup_ngrams() {
    pushd $1
    rm $(ls -l | grep 257 | awk '{print $9}')
    popd
}

for f in $(ls $lyrics_dir); do
    run_ngram $lyrics_dir $f
done

cleanup_ngrams $out_dir
