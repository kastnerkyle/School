#ifndef _GRAPH_H_
#define _GRAPH_H_

#include "Edge.h"
#include <list>

class Graph {
    protected:
        std::list<Edge> Edges;

    public:
        Graph();
        setEdges(std::list<Edge> Edges);  
        ~Graph();
};
#endif
