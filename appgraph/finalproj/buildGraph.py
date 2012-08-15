#!/usr/bin/python
import networkx as nx
import glob
distance_dir = "distances"
songs_with_distances = glob.glob(distance_dir + "/*")

for sf in songs_with_distances:
   try:
       [source_band, source_song] = sf.split(":")
   except ValueError:
       print "Malformed song title " + sf + " skipping"
       continue
   f = open(sf)
   for line in f:
       [ngram_type, count] = line.split(",")[-2:]
       match_band_and_song = line.split(",")[1]
       try:
          [match_band, match_song] = match_band_and_song.split(":")[0:2]
       except ValueError:
          print "Match song " + match_band_and_song_split + " malformed"
   f.close()
