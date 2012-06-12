#ifndef _EDGE_H_
#define _EDGE_H_

#include "Node.h"

class Edge {
    private:
        Node source;
        Node dest;  
        enum { 
                 "UNDIRECTED",
                 "DIRECTED"
             } directionality;

    public:
      Edge(Node source, Node dest, std::string directionality);
      ~Edge();
};
#endif
