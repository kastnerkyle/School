#Need to have pydot installed on the syste
import pygraphviz as pgv
import matplotlib.pyplot as plot
import os
import sys
from PyQt4 import QtGui as qtg
from PyQt4 import QtCore as qtc
import pickle

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
        self.is_directed = is_directed
        self.is_strict = is_strict
        if nodes != None:
            self.nodes = nodes
        if edges != None:
            self.edges = map(lambda x: x.nodes, edges)
            self.nodes = [list(set(x)) for x in self.edges]
   
    def __getstate__(self):
        return {"nodes": self.nodes,
                "edges": self.edges,
                "is_directed": self.is_directed,
                "is_strict": self.is_strict}
                       

    def __setstate__(self, state):
           self.nodes = state["nodes"]
           self.edges = state["edges"]
           self.is_directed = state["is_directed"]
           self.is_strict = state["is_strict"]  
            
    def clearAll(self):
        self.clearEdges()
        self.clearNodes()

    def clearEdges(self):
        del self.edges[:]

    def clearNodes(self):
        del self.nodes[:]

    def addEdge(self, source, dest, is_directed=False, weight=1):
        self.edges.append((source, dest))
        self.addNode(source)
        self.addNode(dest)

    def getEdges(self):
        return self.edges

    def addNode(self, node):
        if str(node) not in self.nodes:
            self.nodes.append(str(node))

    def getNodes(self):
        return self.nodes

    def plot(self, fname="graph.png"):
        _g = pgv.AGraph(directed=self.is_directed, strict=self.is_strict)
        try:
           _t = max(map(len, self.edges))
           if _t == 2 or _t == 3:
               _g.add_edges_from(self.edges)
           else:
               raise TypeError("Edges are made of tuples of length 2, (source, dest), or 3, (source, dest, weight)!")
        except:
            print("Empty graph created!")
        _g.layout(prog="dot")
        _g.draw(fname)

class MainView(qtg.QWidget):
    def __init__(self):
        super(MainView, self).__init__()
        self.graph = Graph()
        self.graph_host = qtg.QLabel() 
        self.graph_pixmap = qtg.QPixmap(self.createGraph(self.graph)).scaledToHeight(self.height())
        self.table = qtg.QTableWidget()
        self.save_fname = "graph.pickle"
        try:
            f = open(self.save_fname, "rb")
            self.graph = pickle.load(f)
            self.graph_pixmap = qtg.QPixmap(self.createGraph(self.graph))
            self.graph_host.setPixmap(self.graph_pixmap)
            #TODO: Repopulate table
            print "Loaded previous graph from " + self.save_fname
        except IOError:
            self.graph = Graph()
        self.initUI()
  
    def createGraph(self, graph): 
        fname = "graph.png" 
        graph.plot(fname)  
        return fname   

    def initGraph(self, widgets):
        widgets.append(self.graph_host)

    def initTable(self, widgets):
        self.table.setRowCount(100)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Source", "Destination"])
        widgets.append(self.table)

    def genGetTableData(self, table, graph, graph_host):
        def getTableData(click):
            #Clear all nodes and edges
            graph.clearAll()
            #Match any cells with text in them
            table_items = table.findItems(".+", qtc.Qt.MatchRegExp)
            table_items = [{"row":x.row(), "name":str(x.text())} 
                           for x in table_items]
            #Sort into list of [source1, dest1, source2, dest2, source3, dest3]
            table_items = [x["name"] for x in 
                           sorted(table_items, key=lambda x: x["row"])]
            #Split sorted list into list of tuples (source, dest)
            table_items = map(None, *([iter(table_items)]*2))
            #Remove any tuples without both source and dest
            print table_items
            table_items = [filter(None, x) for x in table_items]
            table_items = filter(lambda x: len(x) == 2, table_items)
            #Add edges to graph
            [graph.addEdge(x[0], x[1]) for x in table_items]
            #Plot new edges
            graph_pixmap = qtg.QPixmap(self.createGraph(graph))
            graph_host.setPixmap(graph_pixmap)
        return getTableData

    def initWander(self, widgets):
        button = qtg.QPushButton("Wander")
        get = self.genGetTableData(self.table, self.graph, self.graph_host)
        button.clicked[bool].connect(get)
        widgets.append(button)

    def genSaveTableData(self, graph):
        def saveTableData(click):
            f = open(self.save_fname, "wb")
            pickle.dump(graph, f) 
            f.close()
        return saveTableData 

    def initSave(self, widgets):
        button = qtg.QPushButton("Save")
        save = self.genSaveTableData(self.graph)
        button.clicked[bool].connect(save)
        widgets.append(button) 

    def initUI(self):
        left_widgets = []
        self.initGraph(left_widgets)
        
        hbox = qtg.QHBoxLayout()
        [hbox.addWidget(x) for x in left_widgets]

        hbox.addStretch(1)
        
        right_widgets = []
        self.initTable(right_widgets)
        [hbox.addWidget(x) for x in right_widgets]
       
        vbox = qtg.QVBoxLayout()
        vbox.addLayout(hbox)

        vbox.addStretch(1)

        bottom_widgets = []
        self.initWander(bottom_widgets)
        self.initSave(bottom_widgets)
        [vbox.addWidget(x) for x in bottom_widgets]       
    
        self.setLayout(vbox)
        self.setWindowTitle("Graph Viewer v.01")
        self.show()

if __name__ == "__main__":
    app = qtg.QApplication(sys.argv)
    w = MainView()
    sys.exit(app.exec_())
