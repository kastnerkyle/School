#!/usr/bin/python
import networkx as nx
import glob
import pickle 
import random

distance_dir = "distances"
songs_with_distances = glob.glob(distance_dir + "/*")

if __name__ == "__main__":
    band_graph = nx.Graph()
    band_song_graph = nx.Graph()
    max_in_all_files = 0
    for sf in songs_with_distances:
        f = open(sf)
        for line in f:
            [ngram_type, count] = map(int, line.split(",")[-2:])
            count = (ngram_type*count)
            if count > max_in_all_files:
               max_in_all_files = count
        f.close()
    print "Max value is " + str(max_in_all_files) + ", weights normalized by this value"
    chosen_songs = []
    for i in range(2):
        chosen_songs.append(random.choice(songs_with_distances))
     
    for sf in chosen_songs:
        try:
            [source_band, source_song] = sf.split(":")
            source_band = source_band[len(distance_dir)+1:]
        except ValueError:
            source_band = sf[len(distance_dir)+1:]
            source_song = "Unknown_Song"
        f = open(sf)
        for line in f:
            [ngram_type, count] = map(int, line.split(",")[-2:])
            match_band_and_song = "".join(line.split(",")[:-2])
            count = (ngram_type*count)
            try:
               [match_band, match_song] = match_band_and_song.split(":")[0:2]
            except ValueError:
               match_band = match_band_and_song
               match_song = "Unknown_Song"
            fr = source_band + ":" + source_song
            to = match_band + ":" + match_song
            #Check for reverse edge since graph is undirected
            if count > 0 and (to, fr) not in band_song_graph.edges() and (fr, to) not in band_song_graph.edges():
                band_song_graph.add_edge(fr,to,weight = 1 - (float(count)/max_in_all_files))
                #print "Added " + fr + "->" + to + " to the graph"
            elif (to,fr) in band_song_graph.edges() and count > 0:
                band_song_graph.edge[to][fr]["weight"] += 1 - (float(count)/max_in_all_files)
                #print to + "->" + fr + " already in graph - adding"  
                
        f.close()
        print "Finished " + sf
    d = open("saved.graph", "w")
    pickle.dump(band_song_graph, d)
    d.close
