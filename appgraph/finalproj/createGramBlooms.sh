#!/bin/bash

lyrics_dir=${1:-"lyrics"}
ngrams_dir=${2:-"grammified"}
ngrams_prog=${3:-"ngrams/ngrams"}

if [[ ! -e $grams_dir ]]; then
    mkdir -p $grams_dir
fi

run_ngram() {
    #$1 is the lyrics directory, $2 is the filename
    #Use NGRAM count of 4 in order to make NGRAMS 1-3 identical during file cleaning...
    ngram_count=3
    $ngrams_prog --type=word --n=$ngram_count --in=$1/$2 > $ngrams_dir/$2.gram
}

cleanup_ngrams() {
    pushd $1
    echo "Removing n-gram files with errors"
    rm $(ls -l | grep 257 | awk '{print $9}')
    echo "Splitting n-gram files for each n"
    for f in $(ls *.gram); do
        sed -e '/1\-GRAMS/,/2\-GRAMS/!d' $f > $f.1
        sed -e '/2\-GRAMS/,/3\-GRAMS/!d' $f > $f.2
        sed -e '/3\-GRAMS/,//!d' $f > $f.3
    done
    echo "All n-gram files split into gram.{1,2,3} files"
    rm $(ls *.gram)
    echo "Cleaning each file to only contain list of <token>\t<count>"
    for f in $(ls); do 
        sed -e '1,3d' -i $f
        if [[ ! ${f##*\.} -eq 3 ]]; then
            head -n -2 $f > tmp.tmp && mv tmp.tmp $f
        fi 
    done
    echo "Beginning and end of each file cleaned"
    popd
}

make_blooms () {
    for f in $(ls $1); do
        ./buildBloom.pl $1/$f --outdir=filter
    done
}

for f in $(ls $lyrics_dir); do
    run_ngram $lyrics_dir $f
done

cleanup_ngrams $ngrams_dir

make_blooms $ngrams_dir
