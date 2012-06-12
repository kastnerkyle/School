#Need to have pydot installed on the system
import networkx as nx
import matplotlib.pyplot as plot
import random
import os

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

class Graph:
    def __init__(self, edges, gtype="Undirected", plotter="Graphviz"):
        self.edges = map(lambda x: x.nodes, edges)
        self.nodes = [list(set(x)) for x in self.edges]
        self._gopts = {"Undirected": nx.Graph,
                       "UndirectedMulti" : nx.MultiGraph,
                       "Directed" : nx.DiGraph,
                       "DirectedMulti" : nx.MultiDiGraph}
        try:
            self._g = self._gopts.get(gtype)()
        except TypeError:
            raise TypeError("Graph option not recognized! Valid options are " + str(", ".join(self._gopts.keys())))
        self._plotter = plotter
        self._popts = {"Matplotlib": self._plot_matplotlib,
                       "Graphviz": self._plot_dot} 

    def plot(self):
        _t = max(map(len, self.edges))
        if _t == 2 or _t == 3:
            [self._g.add_edge(*x) for x in self.edges]
        else:
            raise TypeError("Tuples of length 2, (source, dest), or 3, (source, dest, weight), required!")
        print self._plotter
        try:
            self._popts.get(self._plotter)()
        except TypeError:
            raise TypeError("Plotter option not recognized! Valid options are " + str(",".join(self._popts.keys())))

    def _plot_matplotlib(self):
        nx.draw(self._g)
        plot.show()

    def _plot_dot(self):
        nx.write_dot(self._g, "current.dot")
        os.system("dot -Tps current.dot -o current.ps")
        os.system("evince current.ps")

if __name__ == "__main__":
    n = [random.randint(0,10) for x in range(30)]
    m = [random.randint(0,10) for x in range(30)]
    ed = map(lambda x: Edge(*x), zip(n, m))
    g = Graph(ed, gtype="UndirectedMult")
    g.plot()   
