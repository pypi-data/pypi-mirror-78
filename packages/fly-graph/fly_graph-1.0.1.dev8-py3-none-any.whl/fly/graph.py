#! python3

# package fly.graph

'''
Graphs for FLY language
'''

from typing import TypeVar, Generic
#from logging import Logger

import networkx as nx

# The type used to represent nodes (or 'vertices') into a graph.
V = TypeVar('V')

# The type used to represent edges into a graph.
E = TypeVar('E')

class Graph():
    """
    A class used to represent a graph for use into FLY language.

    It basically wraps the NetworkX representation of graphs according
    to FLY API for graphs.

    Attributes
    ----------
    graph : object
        the Graph object from NetworkX library

    isDirected : bool
        Denotes whether graph is directed

    isWeighted : bool
        Denotes whether graph is weighted

    Methods
    -------
    clear()
        Empties graph nodes and edges sets.

    addNode(node)
        Adds a specified node to graph.

    addNodes(nodes)
        Adds a specified list of nodes to graph.

    nodeDegree(node)
        Gets the number of edges the specified node is part of.

    nodeInDegree(node)
        Gets the number of edges the specified node is target of.

    nodeOutDegree(node)
        Gets the number of edges the specified node is source of.

    neighbourhood(node)
        Gets the edges the specified node is part of.

    nodeInEdges(node)
        Gets the edges the specified node is target of.

    nodeOutEdges(node)
        Gets the edges the specified node is source of.

    nodeSet()
        Gets the nodes of graph.

    numNodes()
        Gets the number of nodes in graph.

    removeNode(node)
        Removes a specified node from graph.

    hasNode(node)
        Checks whether graph has a specified node.

    addEdge(first_node, second_node)
        Adds an edge between two specified nodes to graph.

    getEdge(first_node, second_node)
        Gets the edge of graph between two specified nodes.

    edgeSet()
        Gets the edges of graph.

    numEdges()
        Gets the number of edges of graph.

    getEdgeWeight(first_node, second_node)
        Gets weight of the edge of graph between two specified nodes.

    setEdgeWeight(first_node, second_node, weight)
        Sets weight of the edge of graph between two specified nodes.

    removeEdge(first_node, second_node)
        Removes the edge of graph between two specified nodes.

    hasEdge(first_node, second_node)
        Checks whether graph has node between two specified nodes or not.

    importGraph(path, separator, is_directed, is_weighted)
        Imports a graph from file.

    exportGraph(fly_graph, path, separator, is_directed, is_weighted)
        Exports a graph to file.

    bfsEdges(root_node)
        Gets edges of BFS rooted in specified node.

    bfsNodes(root_node)
        Gets nodes of BFS rooted in specified node.

    bfsTree(root_node)
        Gets the BFS rooted in specified node.

    dfsEdges(root_node)
        Gets edges of DFS rooted in specified node.

    dfsNodes(root_node)
        Gets nodes of DFS rooted in specified node.

    dfsTree(root_node)
        Gets the DFS rooted in specified node.

    isConnected()
        Checks whether graph is connected or not.

    isStronglyConnected()
        Checks whether graph is strongly connected or not.

    connectedComponents()
        Gets connected components of graph.

    connectedSubgraphs()
        Gets connected subgraphs of graph.

    numberConnectedComponents()
        Gets the number of connected components of graph.

    nodeConnectedComponents(node)
        Gets connected component for specified node.

    stronglyConnectedComponents()
        Gets strongly connected components of graph.

    stronglyConnectedSubgraphs()
        Gets strongly connected subgraphs of graph.

    isDAG()
        Checks whether graph is DAG or not.

    topologicalSort()
        Gets a topological sort for graph.

    getMST()
        Gets minimum spanning tree from graph by running Prim's algorithm on it.
    """

    # TODO consider documenting methods into class docblock

    # initializer
    def __init__(self, node_set=[], edge_set=[], is_directed=False, is_weighted=False) -> None:
        """
        Builds an instance of FLY Graph.

        It consists of an instance of NetworkX graph, a boolean value that
        indicates whether graph is directed or not (by default, it is set to
        False) and another boolean value that indicates whether graph is
        weighted or not (by default, it is set to False). 

        Parameters
        ----------
        is_directed : bool
            Denotes whether graph is directed or not (default: False)

        is_weighted : bool
            Denotes whether graph is weighted or not (default: False)
        """
        self.graph = nx.DiGraph() if is_directed else nx.Graph()
        if node_set: self.graph.add_nodes_from(node_set)
        if edge_set: self.graph.add_edges_from(edge_set)
        self.isDirected = isinstance(self.graph, nx.DiGraph)
        self.isWeighted = is_weighted

    def __repr__(self):
        return f"Graph(node_set={self.graph.nodes}, edge_set={self.graph.edges}, is_directed={self.isDirected}, is_weighted={self.isWeighted})"

    def __str__(self):
        nodes = str(self.graph.nodes).replace('\'', '')
        edges = str(self.graph.edges).replace('\'', '')
        to_string = f"({nodes}, "
        if self.isDirected:
            to_string += f"{edges}), directed"
        else:
            to_string += f"{edges.replace('(', '{').replace(')', '}')})"
        if self.isWeighted:
            to_string += ", weighted"
        return to_string

    def clear(self) -> None:
        """
        Empties graph nodes and edges sets.
        """
        self.graph.clear()

    #
    # Nodes
    #

    def addNode(self, node: V) -> None:
        """
        Adds a node to graph.

        Parameters
        ----------
        node : V
            The node to add to graph

        """
        self.graph.add_node(node)

    def addNodes(self, nodes: list) -> None:
        """
        Adds a list of nodes to graph.

        Parameters
        ----------
        nodes : list
            The list of nodes to add to graph
        """
        self.graph.add_nodes_from(nodes)

#    def add_nodes(self, *nodes: V) -> None:
#        """
#        """
#        for node in nodes:
#            self.add_node(node)

    def nodeDegree(self, node: V) -> int:
        """
        Gets the number of edges the node is part of.

        Parameters
        ----------
        node : V
            The node to check for degree

        Returns
        -------
        int
            Number of edges the node is part of
        """
        return self.graph.degree(node)

    def nodeInDegree(self, node: V) -> int:
        """
        Gets the number of edges the specified node is target of.

        Parameters
        ----------
        node : V
            The node to check for 'in' degree

        Returns
        -------
        int
            Number of edges the node is target of
        """
        return self.graph.in_degree(node)

    def nodeOutDegree(self, node: V) -> int:
        """
        Gets the number of edges the specified node is source of.

        Parameters
        ----------
        node : V
            The node to check for 'out' degree

        Returns
        -------
        int
            Number of edges the node is souce of
        """
        return self.graph.out_degree(node)

    def neighbourhood(self, node: V) -> list:
        """
        Gets the edges the specified node is part of.

        Parameters
        ----------
        node : V
            The node which we want the neighbourhood of

        Returns
        -------
        list
            Neighbourhood of specified node

        """
        return list(self.graph.adj[node])

    def nodeInEdges(self, node: V) -> list:
        """
        Gets the edges the specified node is target of.

        Parameters
        ----------
        node : V
            The node which we want the incoming edges of

        Returns
        -------
        list
            Incoming edges of specified node
            
        """
        return list(self.graph.in_edges(nbunch=node))

    def nodeOutEdges(self, node: V) -> list:
        """
        Gets the edges the specified node is source of.

        Parameters
        ----------
        node : V
            The node which we want the outgoing edges of

        Returns
        -------
        list
            Outgoing edges of specified node
        """
        return list(self.graph.out_edges(nbunch=node))

    def nodeSet(self) -> list:
        """
        Gets the nodes of graph.

        Returns
        -------
        list
            Graph nodes set
        """
        return list(self.graph.nodes)

    def numNodes(self) -> int:
        """
        Gets the number of nodes in graph.

        Returns
        -------
        int
            Number of graph nodes
        """
        return self.graph.order()

    def removeNode(self, node: V) -> None:
        """
        Removes a specified node from graph.

        Parameters
        ----------
        node : V
            The node we want to remove from graph

        """
        self.graph.remove_node(node)

    def hasNode(self, node: V) -> bool:
        """
        Checks whether graph has a specified node.

        Parameters
        ----------
        node : V
            The node we want to check to be in graph

        Returns
        -------
        bool
            'True' if node is in graph, 'False' otherwise
        """
        return self.graph.has_node(node)

    #
    # Edges
    #

    def addEdge(self, first_node: V, second_node: V) -> None:
        """
        Adds an edge between two specified nodes to graph.

        Parameters
        ----------
        first_node : V
            Source node of edge

        second_node : V
            Target node of edge
        """
        self.graph.add_edge(first_node, second_node)

    def getEdge(self, first_node: V, second_node: V) -> E:
        """
        Gets the edge of graph between two specified nodes.

        Parameters
        ----------
        first_node : V
            Source node of edge

        second_node : V
            Target node of edge

        Returns
        -------
        E
            Graph edge which specified nodes are source and target of
        """
        edge_list = self.graph.edges([first_node, second_node])
        for pair in edge_list:
            (source, target) = pair
            if source == first_node and target == second_node:
                return pair
        return None

    def edgeSet(self) -> list:
        """
        Gets the edges of graph.

        Returns
        -------
        list
            Graph edge set
        """
        return list(self.graph.edges)

    def numEdges(self) -> int:
        """
        Gets the number of edges of graph.

        Returns
        -------
        int
            The number of graph edges
        
        """
        return self.graph.size()

    def getEdgeSource(self, edge: E) -> V:
        # TODO document
        (source, target) = edge
        return source

    def setEdgeSource(self, edge: E, new_source: V) -> None:
        # TODO document
        (source, target) = edge
        self.graph.remove_edge(source, target)
        self.graph.add_edge(new_source, target)

    def getEdgeTarget(self, edge: E) -> V:
        # TODO document
        (source, target) = edge
        return target

    def setEdgeTarget(self, edge: E, new_target: V) -> None:
        # TODO document
        (source, target) = edge
        self.graph.remove_edge(source, target)
        self.graph.add_edge(source, new_target)

    def getEdgeWeight(self, first_node: V, second_node: V) -> float:
        """
        Gets weight of the edge of graph between two specified nodes.

        Parameters
        ----------
        first_node : V
            Source node of edge

        second_node : V
            Target node of edge

        Returns
        -------
        float
            Weight of edge which specified nodes are edge and target of
        """
        return self.graph[first_node][second_node]['weight'] #if self.isWeighted else 1.0

    def setEdgeWeight(self, first_node: V, second_node: V, weight: float) -> None:
        """
        Sets weight of the edge of graph between two specified nodes.

        Parameters
        ----------
        first_node : V
            Source node of edge

        second_node : V
            Target node of edge

        weight : float
            Weight of edge
        """
        self.graph[first_node][second_node]['weight'] = weight #if self.isWeighted else 1.0

    def removeEdge(self, first_node: V, second_node: V) -> None:
        """
        Removes the edge of graph between two specified nodes.

        Parameters
        ----------
        first_node : V
            Source node of edge

        second_node : V
            Target node of edge
        """
        self.graph.remove_edge(first_node, second_node)

    def hasEdge(self, first_node: V, second_node: V) -> bool:
        """
        Checks whether graph has node between two specified nodes or not.

        Parameters
        ----------
        first_node : V
            Source node of edge

        second_node : V
            Target node of edge

        Returns
        -------
        bool
            'True' if an edge exists between specified nodes, 'False' otherwise
        """
        return self.graph.has_edge(first_node, second_node)

    #
    # I/O
    #

    @staticmethod
    def importGraph(path, separator: str, is_directed=False, is_weighted=False) -> object:
        """
        Imports a graph from a CSV file.

        Graph has to be represented as 'edge list' in order to be properly read
        from file.

        Parameters
        ----------
        path : str
            Path of source file

        separator : str
            Separator character of CSV file

        is_directed : bool
            Denotes whether graph is directed or not (default: False)

        is_weighted : bool
            Denotes whether graph is weighted or not (default: False)

        Returns
        -------
        object
            FLY graph read from file
        """
        fly_graph = Graph(is_directed=is_directed, is_weighted=is_weighted)
        fly_graph.graph = nx.read_weighted_edgelist(path, delimiter=separator, create_using=nx.DiGraph if is_directed else nx.Graph) #if fly_graph.isWeighted else nx.read_edgelist(path, delimiter=separator, data=False)
        return fly_graph

    @staticmethod
    def exportGraph(fly_graph: object, path, separator: str) -> None:
        """
        Exports a graph to file.

        Parameters
        ----------
        fly_graph : object
            FLY graph to save in file

        path : str
            Path of destination file

        separator : str
            Separator character of CSV file
        """
        nx.write_weighted_edgelist(fly_graph.graph, path, delimiter=separator) #if is_weighted else nx.write_edgelist(fly_graph.graph, path, delimiter=separator)

    #
    # Graph traversal
    #

    def bfsEdges(self, root_node: V) -> list:
        """
        Gets edges of BFS rooted in specified node.

        Parameters
        ----------
        root_node : V
            Root node of BFS tree

        Returns
        -------
        list
            Edges of BFS tree extracted from graph
        """
        return list(nx.bfs_edges(self.graph, root_node))

    def bfsNodes(self, root_node: V) -> list:
        """
        Gets nodes of BFS rooted in specified node.

        Parameters
        ----------
        root_node : V
            Root node of BFS tree

        Returns
        -------
        list
            Nodes o BFS tree extracted from graph
        """
        return [root_node] + [v for u, v in nx.bfs_edges(self.graph, root_node)]

    def bfsTree(self, root_node: V) -> object:
        """
        Gets the BFS rooted in specified node.

        Parameters
        ----------
        root_node : V
            Root node of BFS tree

        Returns
        -------
        object
            BFS tree extracted from graph
        """
        tree = Graph()
        tree.graph.add_edges_from(self.bfsEdges(root_node))
        tree.graph.add_nodes_from(self.bfsNodes(root_node))
        return tree

    def dfsEdges(self, root_node: V) -> list:
        """
        Gets edges of DFS rooted in specified node.

        Parameters
        ----------
        root_node : V
            Root node of DFS tree

        Returns
        -------
        list
            Edges of DFS tree extracted from graph
        """
        return list(nx.dfs_edges(self.graph, source=root_node))

    def dfsNodes(self, root_node: V) -> list:
        """
        Gets nodes of DFS rooted in specified node.

        Parameters
        ----------
        root_node : V
            Root node of DFS tree

        Returns
        -------
        list
            Nodes of DFS tree extracted from graph
        """
        return [root_node] + [v for u, v in nx.dfs_edges(self.graph, source=root_node)]

    def dfsTree(self, root_node: V) -> object:
        """
        Gets the DFS rooted in specified node.

        Parameters
        ----------
        root_node : V
            Root node of DFS tree

        Returns
        -------
        object
            DFS tree exrcted from graph
        """
        tree = Graph()
        tree.graph.add_edges_from(self.dfsEdges(root_node))
        tree.graph.add_nodes_from(self.dfsNodes(root_node))
        return tree

    #
    # Connectivity
    #

    def isConnected(self) -> bool:
        """
        Checks whether graph is connected or not.

        Returns
        -------
        bool
            'True' if graph is connected, 'False' otherwise
        """
        return nx.is_connected(self.graph)

    def isStronglyConnected(self) -> bool:
        """
        Checks whether graph is strongly connected or not.

        Returns
        -------
        bool
            'True' if graph is strongly connected, 'False' otherwise
        """
        return nx.is_strongly_connected(self.graph)

    def connectedComponents(self) -> list:
        """
        Gets connected components of graph.

        Returns
        -------
        list
            Graph connected components
        """
        return list(set for set in nx.connected_components(self.graph))

    def connectedSubgraphs(self) -> list:
        """
        Gets connected subgraphs of graph.

        Returns
        -------
        list
            Graph connected subgraphs
        """
        subgraphs = list()
        for set in nx.connected_components(self.graph):
            subgraph = Graph(is_directed = self.isDirected, is_weighted = self.isWeighted)
            subgraph.addNodes(set)
            for edge in self.graph.edges:
                if edge[0] in set and edge[1] in set:
                    subgraph.addEdge(edge[0], edge[1])
            subgraphs.append(subgraph)
        return subgraphs
#        return list(self.graph.subgraph(set).copy() for set in nx.connected_components(self.graph))

    def numberConnectedComponents(self) -> int:
        """
        Gets the number of connected components of graph.

        Returns
        -------
        int
            Number of Graph connected components
        """
        return nx.number_connected_components(self.graph)

    def nodeConnectedComponent(self, node: V) -> list:
        """
        Gets connected component for specified node.

        Parameters
        ----------
        node : V
            The node which we want to know the connected component of

        Returns
        -------
        list
            Connected component of specified node
        """
        return nx.node_connected_component(self.graph, node)

    def stronglyConnectedComponents(self) -> list:
        """
        Gets strongly connected components of graph.

        Returns
        -------
        list
            Strongly connected component of specified node
        """
        return list(set for set in nx.kosaraju_strongly_connected_components(self.graph))

    def stronglyConnectedSubgraphs(self) -> list:
        """
        Gets strongly connected subgraphs of graph.

        Returns
        -------
        list
            Graph strngly connected components
        """
        subgraphs = list()
        for set in nx.kosaraju_strongly_connected_components(self.graph):
            subgraph = Graph(is_directed = self.isDirected, is_weighted = self.isWeighted)
            subgraph.addNodes(set)
            for edge in self.graph.edges:
                if edge[0] in set and edge[1] in set:
                    subgraph.addEdge(edge[0], edge[1])
            subgraphs.append(subgraph)
        return subgraphs
#        return list(self.__class__().graph = (self.graph.subgraph(set).copy for set in nx.kosaraju_strongly_connected_components(self.graph)))

    #
    # DAG and topological sorting
    #

    def isDAG(self) -> bool:
        """
        Checks whether graph is a directed acyclic graph (DAG) or not.

        Returns
        -------
        bool
            'True' if graph is DAG, 'False' otherwise
        """
        return nx.is_directed_acyclic_graph(self.graph)

    def topologicalSort(self) -> list:
        """
        Gets a topological sort for graph.

        Returns
        -------
        list
            Graph topological-sorted nodes
        """
        return list(nx.topological_sort(self.graph))

    #
    # Minimum spanning tree
    #

    def getMST(self) -> object:
        """
        Gets minimum spanning tree from graph by running Prim's algorithm on it.

        Returns
        -------
        object
            Graph minimum spanning tree
        """
        mst = self.__class__()
        mst.graph = nx.minimum_spanning_tree(self.graph, algorithm='prim')
        return mst
#
# Run tests as standalone module
#
if __name__ == "__main__":
    print("Run FLY Graph tests")

    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    from ..tests import graph_test, graph_io_test

    graph_test
    graph_io_test
