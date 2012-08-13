#!/usr/bin/perl
if ($#ARGV < 0) {
    print "Usage: buildBloom.pl <n-gramfile> [--outdir=output_dir]. Will write out a bloom filter to filter/<n-gramfile>.bf\n";
    exit;
}

use Getopt::Long;
use Bloom::Faster;

$outdir = "filter";
GetOptions('outdir=s' => \$outdir);

open $gram, $ARGV[0] or die $!;

$filt = new Bloom::Faster({n => 100000, e => 0.01});

while(<$gram>) {
    chomp;
    ($token, $count) = split("\t", $_);
    #Should never have a duplicate add, but still check
    if ($filt->add($token)) {
         print "Duplicate add for $token\n";
    }
}

mkdir "$outdir" unless -d "$outdir";
$infile = "$ARGV[0]";
#Get rid of leading directory
$infile =~ s!.*/!!;
#Get rid of .gram and replace with .bf numbers
$infile =~ s!\Q.gram\E!.bf!;
$outfile = "$outdir/$infile";
print "Saving bloom filter to $outfile" . "\n";
$filt->to_file("$outfile");
