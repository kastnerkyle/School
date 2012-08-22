#!/usr/bin/python
import networkx as nx
import pickle
from collections import Counter
import matplotlib.pyplot as plot
import heapq

#Identical to networkx implementation of dijkstra_path()
def almost_path(G,source,target,weight='weight'):
    (length,path)=single_source_almost(G,source,target=target,weight=weight)
    try:
        return path[target]
    except KeyError:
        print "Source not reachable from %s"%(source,target)

#Adapted heavily from networkx single_source_dijkstra()
def single_source_almost(G,source,target=None,cutoff=None,weight='weight'):
    if source==target:
        return (0, [source])
    dist = {}  # dictionary of final distances
    paths = {source:[source]}  # dictionary of paths
    seen = {source:0}
    fringe=[] # use heapq with (distance,label) tuples 
    heapq.heappush(fringe,(0,source))
    while fringe:
        (d,v)=heapq.heappop(fringe)
        if v in dist:
            continue # already searched this node.
        dist[v] = d
        if v == target:
            break
        #for ignore,w,edgedata in G.edges_iter(v,data=True):
        #is about 30% slower than the following
        if G.is_multigraph():
            edata=[]
            for w,keydata in G[v].items():
                minweight=min((dd.get(weight,1)
                               for k,dd in keydata.items()))
                edata.append((w,{weight:minweight}))
        else:
            edata=iter(G[v].items())

        for w,edgedata in edata:
            vw_dist = dist[v] + edgedata.get(weight,1)
            if cutoff is not None:
                if vw_dist>cutoff:
                    continue
            if w in dist:
                if vw_dist < dist[w]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif w not in seen or vw_dist < seen[w]:
                seen[w] = vw_dist
                heapq.heappush(fringe,(vw_dist,w))
                paths[w] = paths[v]+[w]
    return (dist,paths)

f = open("saved.graph")
g = pickle.load(f)
n = Counter([x[0] for x in g.edges()])
keys = sorted(n, key=n.get, reverse=True)
for i in range(25):
    print almost_path(g, keys[i], keys[i+1])

#nx.draw(g)
#plot.show()
