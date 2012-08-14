#!/usr/bin/perl

if( $#ARGV < 1 ) {
    print "Usage: inBloom.pl <ngram file> <filter>\n";
    exit;
}

use Bloom::Faster;
$in_filter = new Bloom::Faster("$ARGV[1]");
open $ngram, $ARGV[0] or die $!;
$matched = 0;
while (<$ngram>) {
    chomp;
    ($token, $count) = split("\t", $_);
    if ($in_filter->check("$token")) {
        $matched += 1;
    } 
}
print $matched . "\n";
close $ngram or die $!;
