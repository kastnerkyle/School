#Need to have pydot installed on the syste
import pygraphviz as pgv
import matplotlib.pyplot as plot
import os
import sys
from PyQt4 import QtGui as qtg
from PyQt4 import QtCore as qtc

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
        self.crossed = False
        self.color = 0
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

    def plot(self, fname="graph.png"):
        try:
            _t = max(map(len, self.edges))
            if _t == 2 or _t == 3:
                self._g.add_edges_from(self.edges)
            else:
                raise TypeError("Edges are made of tuples of length 2, (source, dest), or 3, (source, dest, weight)!")
        except:
            print("Empty graph created!")
        self._g.layout(prog="dot")
        self._g.draw(fname)

class MainView(qtg.QWidget):
    def __init__(self):
        super(MainView, self).__init__()
        self.graph = Graph()
        self.graph_pixmap = self.initImage()
        self.initUI()
  
    def initImage(self):
        graph_pixmap = qtg.QPixmap(self.createGraph())
        graph_pixmap = graph_pixmap.scaledToHeight(self.height())
        return graph_pixmap 

    def createGraph(self): 
        fname = "graph.png" 
        self.graph.plot(fname)  
        return fname   

    def initGraph(self, widgets):
        graph_host = qtg.QLabel(self)
        graph_host.setPixmap(self.graph_pixmap)
        widgets.append(graph_host)

    def initEntry(self, widgets):
        graph_data = qtg.QTableWidget()
        graph_data.setRowCount(100)
        graph_data.setColumnCount(2)
        widgets.append(graph_data)

    def initWander(self, widgets):
        button = qtg.QPushButton("Wander")
        widgets.append(button) 

    def initUI(self):
        left_widgets = []
        self.initGraph(left_widgets)
        
        hbox = qtg.QHBoxLayout()
        [hbox.addWidget(x) for x in left_widgets]

        hbox.addStretch(1)
        
        right_widgets = []
        self.initEntry(right_widgets)
        [hbox.addWidget(x) for x in right_widgets]
       
        vbox = qtg.QVBoxLayout()
        vbox.addLayout(hbox)

        vbox.addStretch(1)

        bottom_widgets = []
        self.initWander(bottom_widgets)
        [vbox.addWidget(x) for x in bottom_widgets]       
    
        self.setLayout(vbox)
        self.setWindowTitle("Graph Viewer v.01")
        self.show()

if __name__ == "__main__":

    app = qtg.QApplication(sys.argv)
    w = MainView()
    sys.exit(app.exec_())
