#!/usr/bin/perl

if( $#ARGV < 1 ) {
    print "Usage: inBloom.pl <ngram file> <filter>\n";
    exit;
}

use Bloom::Faster;
$in_filter = new Bloom::Faster("$ARGV[1]");
open $ngram, $ARGV[0] or die $!;
while (<$ngram>) {
    chomp;
    ($token, $count) = split("\t", $_);
    if ($in_filter->check("$token")) {
        print "$token is in the filter seen!\n";
    } 
}
close $ngram or die $!;
