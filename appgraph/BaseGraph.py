import networkx as nx
import matplotlib.pyplot as plot
import random

class Edge:
    def __init__(self, n1, n2, weight=1):
        if weight == 1:
            self.nodes = (n1, n2)
            self.weight = weight
        else:
            self.nodes = (n1, n2, weight)
            self.weight = weight

    def __str__(self):
        return str(self.nodes)

    def __repr__(self):
        return (self.nodes)

    def __len__(self):
        return len(self.nodes)

    def getSource(self):
        return self.nodes[0]

    def getDest(self):
        return self.nodes[1]

class Graph:
    def __init__(self, edges, gtype="Undirected"):
        self.edges = map(lambda x: x.nodes, edges)
        self._gopts = {"Undirected": nx.Graph(),
                       "UndirectedMulti" : nx.MultiGraph(),
                       "Directed" : nx.DiGraph(),
                       "DirectedMulti" : nx.MultiDiGraph()} 
        self._g = self._gopts[gtype]

    def plot(self):
        _t = max(map(len, self.edges))
        if _t == 2:
            self._g.add_edges_from(self.edges)
        elif _t == 3:
            self._g.add_weighted_edges_from(self.edges)
        else:
            raise TypeError("Tuples of length 2 or 3(weighted) required!")
        nx.draw(self._g)
        plot.show()

n = [random.randint(0,10) for x in range(30)]
m = [random.randint(0,10) for x in range(30)]
ed = map(lambda x,y: Edge(x,y), n, m)
g = Graph(ed, gtype="UndirectedMulti")
g.plot()    
