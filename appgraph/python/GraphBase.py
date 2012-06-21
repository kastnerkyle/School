#Need to have pydot installed on the system
import pygraphviz as pgv
import os
import sys
from PyQt4 import QtGui as qtg
from PyQt4 import QtCore as qtc
import pickle

class Node:
    def __init__(self, name):
        self.name = str(name)
        self.num_connections = 1
        self.connected_to = []

    def addConnection(self, connector):
        self.num_connections = self.num_connections + 1
        self.connected_to.append(connector)

    def removeConnection(self, connector):
       if connector in self.connected_to:
            del self.connected_to[self.connected_to.index(connector)]
       else:
            print `connector` + " is not connected to node " + `self`

    def Details(self):
        return str({"NodeName": self.name,
                    "ConnectedTo": self.connected_to,
                    "NumConnections": self.num_connections})
 
    def __eq__(self, other):
        return (self.name == other.name)

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return 1

class Edge:
    def __init__(self, source, dest, is_directed=False, weight=1):
        self.directed = is_directed
        self.crossed = False
        self.color = i
        if weight == 1:
            self.nodes = (Node(source), Node(dest))
            self.weight = weight
        else:
            self.nodes = (Node(source), Node(dest), weight)
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
            [self.addNode(x) for x in nodes]
        if edges != None:
            [self.addEdge(x) for x in edges]
   
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
        self.addNode(source, connection=dest)
        self.addNode(dest, connection=source)

    def getEdges(self):
        return self.edges

    def addNode(self, node, connection=None):
        primary_node = Node(node)
        if primary_node not in self.nodes:
            self.nodes.append(primary_node)
        if connection is not None:
            connection_node = Node(connection)
            self.nodes[self.nodes.index(primary_node)].addConnection(connection_node)
            
    def getNodes(self):
        return self.nodes

    def plot(self, fname="graph.png"):
        _g = pgv.AGraph(directed=self.is_directed, strict=self.is_strict)
        try:
            _g.add_edges_from(self.edges)
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
            #Empty list so that I can reuse the initTable function
            self.initTable([])
            self.fillTable()
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
 
    def fillTable(self):
        for i,j in zip(self.graph.edges, range(self.table.rowCount())):
            self.table.setItem(j, 0, qtg.QTableWidgetItem(i[0]))
            self.table.setItem(j, 1, qtg.QTableWidgetItem(i[1]))

    def initTable(self, widgets):
        self.table.setRowCount(100)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Source", "Destination"])
        widgets.append(self.table)

    def getTableData(self, click):
        #Clear all nodes and edges
        self.graph.clearAll()
        #Match any cells with text in them
        table_items = self.table.findItems(".+", qtc.Qt.MatchRegExp)
        table_items = [{"row":x.row(), "name":str(x.text())} 
                       for x in table_items]
        #Sort into list of [source1, dest1, source2, dest2, source3, dest3]
        table_items = [x["name"] for x in 
                       sorted(table_items, key=lambda x: x["row"])]
        #TODO Fix bug with separated source and dest
        #Split sorted list into list of tuples (source, dest)
        table_items = map(None, *([iter(table_items)]*2))
        #Remove any tuples without both source and dest
        table_items = [filter(None, x) for x in table_items]
        table_items = filter(lambda x: len(x) == 2, table_items)
        #Add edges to graph
        [self.graph.addEdge(x[0], x[1]) for x in table_items]
        #Plot new edges
        self.graph_pixmap = qtg.QPixmap(self.createGraph(self.graph))
        self.graph_host.setPixmap(self.graph_pixmap)

    def updateGraph(self, click):
        print "Update!"

    def initUpdate(self, widgets):
        button = qtg.QPushButton("Update")
        button.clicked[bool].connect(self.getTableData)
        button.clicked[bool].connect(self.updateGraph)
        widgets.append(button)

    def wanderGraph(self, click):
        print "Wander!"
        print self.graph.nodes

    def initWander(self, widgets):
        button = qtg.QPushButton("Wander")
        button.clicked[bool].connect(self.wanderGraph)
        widgets.append(button)

    def saveTableData(self, click):
        f = open(self.save_fname, "wb")
        pickle.dump(self.graph, f) 
        f.close()

    def initSave(self, widgets):
        button = qtg.QPushButton("Save")
        button.clicked[bool].connect(self.saveTableData)
        widgets.append(button) 
    
    def clearTableData(self, click):
        for i in range(self.table.rowCount()):
            self.table.setItem(i, 0, qtg.QTableWidgetItem())
            self.table.setItem(i, 1, qtg.QTableWidgetItem())
                    
    def initClear(self, widgets):
        button = qtg.QPushButton("Clear")
        button.clicked[bool].connect(self.clearTableData)
        button.clicked[bool].connect(self.getTableData)
        widgets.append(button)

    def debugClass(self, click):
        print [(x.name, x.num_connections) for x in self.graph.nodes]
        print [x.connected_to for x in self.graph.nodes]
        print self.graph.nodes

    def initDebug(self, widgets):
        button = qtg.QPushButton("Debug")
        button.clicked[bool].connect(self.debugClass)
        widgets.append(button)

    def initUI(self):
        top_left_widgets = []
        self.initGraph(top_left_widgets)
        
        top_right_widgets = []
        self.initTable(top_right_widgets)

        bottom_widgets = []
        self.initClear(bottom_widgets)
        self.initUpdate(bottom_widgets)
        self.initDebug(bottom_widgets)
        self.initWander(bottom_widgets)
        self.initSave(bottom_widgets)

        hbox_top = qtg.QHBoxLayout()
        [hbox_top.addWidget(x) for x in top_left_widgets]
        hbox_top.addStretch(1)
        [hbox_top.addWidget(x) for x in top_right_widgets]

        hbox_bottom = qtg.QHBoxLayout()
        [hbox_bottom.addWidget(x) for x in bottom_widgets] 
        
        vbox = qtg.QVBoxLayout()
        vbox.addLayout(hbox_top)
        vbox.addStretch(1)
        vbox.addLayout(hbox_bottom)
 
        self.setLayout(vbox)
        self.setWindowTitle("Graph Viewer v.01")
        self.show()

if __name__ == "__main__":
    app = qtg.QApplication(sys.argv)
    w = MainView()
    sys.exit(app.exec_())
