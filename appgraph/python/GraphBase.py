#Need to have pydot installed on the syste
import pygraphviz as pgv
import matplotlib.pyplot as plot
import os
import sys
from PyQt4 import QtGui as qtg

class Node:
    def __init__(self, name):
        self.name = name 

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def __len__(self):
        return 1

class Edge:
    def __init__(self, source, dest, is_directed=False, weight=1):
        self.directed = is_directed
        if weight == 1:
            self.nodes = (Node(str(source)), Node(str(dest)))
            self.weight = weight
        else:
            self.nodes = (Node(str(source)), Node(str(dest)), weight)
            self.weight = weight
        
    def __repr__(self):
        if self.directed:
            return "(" + str(self.nodes[0]) + " -> " + str(self.nodes[1])+")"
        else:
            return str(self.nodes)

    def __str__(self):
        return str(self.nodes)

    def __len__(self):
        return len(self.nodes)

class Graph:
    def __init__(self, edges=None, nodes=None, is_directed=False, is_strict=False):
        self.nodes = []
        self.edges = []
        if nodes != None:
            self.nodes = nodes
        if edges != None:
            self.edges = map(lambda x: x.nodes, edges)
            self.nodes = [list(set(x)) for x in self.edges]
        self._g = pgv.AGraph(directed=is_directed, strict=is_strict)

    def addEdge(self, source, dest, is_directed=False, weight=1):
        self.edges.append(source, dest)

    def getEdges(self):
        return self.edges

    def addNode(self, node):
        if str(node) not in self.nodes:
            self.nodes.append(str(node))

    def getNodes(self):
        return self.nodes

    def plot(self):
        _t = max(map(len, self.edges))
        if _t == 2 or _t == 3:
            self._g.add_edges_from(self.edges)
            self._g.layout(prog="dot")
            self._g.draw("graph.png")
        else:
            raise TypeError("Edges are made of tuples of length 2, (source, dest), or 3, (source, dest, weight)!")

if __name__ == "__main__":
    import random
    n = [random.randint(0,10) for x in range(30)]
    m = [random.randint(0,10) for x in range(30)]
    e = map(lambda x: Edge(*x, is_directed=True), zip(n, m))
    g = Graph(edges=e)
    g.plot()   

    app = qtg.QApplication(sys.argv)
    w = qtg.QWidget()
    w.show()
    sys.exit(app.exec_())
