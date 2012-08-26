#!/usr/bin/python
import networkx as nx
import pickle
from collections import Counter
import matplotlib.pyplot as plot
import numpy as np
from itertools import count, izip
#Identical to networkx implementation of dijkstra_path()

class NearMissWanderer(object):
    def __init__(self):
        f = open("saved.graph")
        self.g = pickle.load(f)
        n = Counter([x[0] for x in self.g.edges()])
        self.keys = sorted(n, key=n.get, reverse=True)
        self.expansion_depth = 4

    def _best(self, node, neighbors):
        weights = [self.g[node][n]['weight'] for n in neighbors]
        #Get minimum index and value of min weights
        if len(weights) == 0:
            return (None, None)
        minval, minindex = min(izip(weights, count()))
        best = neighbors[minindex]
        return (best, minval)     

    def get_best(self, node, exclude=[], neighbors=None):
        if neighbors == None:
            neighbors = self.g.neighbors(node)
        (best, weight) = self._best(node, neighbors)
        if best not in exclude:
            return best
        else:
            neighbors = [n for n in neighbors if n not in [best]]
            best = self.get_best(node, exclude, neighbors)
            return best
    
    def get_path(self, node, exclude=[]):
        depth = 0
        path = [] 
        while depth < self.expansion_depth:
            depth += 1 
            best = self.get_best(node, exclude)
            path.append(best)
            exclude.append(best) 
        return path

    def run(self):
        for source,target in zip(self.keys[0::2], self.keys[1::2]):
            try:
                exclude = [source, target]
                from_source = self.get_path(source, exclude)	
                from_target = self.get_path(target, exclude)
                path = from_source 
                path.extend(nx.dijkstra_path(self.g, from_source.pop(), from_target.pop()))
                path.extend(from_target[::-1])
                print path
            except RuntimeError:
                print "No path found - recursion limit!"
            except KeyError:
                print "Unable to find path between %s %s"%(from_source,from_target)
            except nx.exception.NetworkXNoPath:
                print "Node %s not reachable from %s"%(source,target)

if __name__ == "__main__":
    n = NearMissWanderer()
    n.run()
#nx.draw(g)
#plot.show()
