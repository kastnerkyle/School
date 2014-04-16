#!/bin/bash

rm publication.bib
xelatex $1
bibtex "${1%.*}.aux"
xelatex $1
evince "${1%.*}.pdf"
