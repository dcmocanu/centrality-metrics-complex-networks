# Author: Decebal Constantin Mocanu;
# Proof of concept implementation of the Game of Thieves (GoT) - a metric to compute nodes and links centrality in complex networks or graphs;
# This is a pre-alpha free software and was tested with Python 2.7.12, Matplotlib 2.1.0, Numpy 1.14, NetworkX 2.0;
# The code is distributed in the hope that it may be useful, but WITHOUT ANY WARRANTIES; The use of this software is entirely at the user's own risk;
# For an easy understanding of the code functionality please read the following article.

# If you use this code please cite its corresponding article:
#@article{Mocanu2018GOT,
#  author =        {Mocanu, Decebal Constantin and Exarchakos, Georgios and Liotta, Antonio},
#  journal =       {Scientific Reports},
#  title =         {Decentralized dynamic understanding of hidden relations in complex networks},
#  volume =        {8},
#  year =          {2018},
#  doi =           {10.1038/s41598-018-19356-4},
#  url =           {https://www.nature.com/articles/s41598-018-19356-4}
#}

import numpy as np
import networkx as nx

def generateWeightedNetwork(G):
    # Input:
    #   G - the network analyzed
    # Output:
    #   G - a network with random generated weights values
    for edge in G.edges():
        v=np.random.randint(1,10)
        G.add_edge(edge[0], edge[1], value=v)
    return G

def generateUnweightedNetwork(G):
    # Input:
    #   G - the network analyzed
    # Output:
    #   G - a network with the same  weights values
    for edge in G.edges():
        v=1
        G.add_edge(edge[0], edge[1], value=v)
    return G

def edgesRemovalProcedure(G,edgesSorted):
    # Input:
    #   G - the network analyzed
    #   edgesSorted - edges sorted according with their centrality
    # Output:
    #   nodesGiant - an array with the remaining size of the giant component after each edge removed
    #   nodesGiant - an array with the remaining number of connected components after each edge removed
    M = G.number_of_edges()
    nodesGiant=np.zeros(M)
    noComponents=np.zeros(M)
    H=G.copy()
    for k in range(M):
        H.remove_edge(edgesSorted[k][0][0],edgesSorted[k][0][1])
        conngen=nx.connected_components(H)
        conn=sorted(conngen, key = len, reverse=True)
        nodesGiant[k]=len(conn[0])
        noComponents[k]=len(conn)
    return [nodesGiant,noComponents]

def nodesRemovalProcedure(G,nodesSorted):
    # Input:
    #   G - the network analyzed
    #   nodesSorted - nodes sorted according with their centrality
    # Output:
    #   nodesGiant - an array with the remaining size of the giant component after each node removed
    #   nodesGiant - an array with the remaining number of connected components after each node removed
    N=G.number_of_nodes()
    nodesGiant=np.zeros(N)
    noComponents=np.zeros(N)
    H=G.copy()
    for k in range(N-1):
        H.remove_node(nodesSorted[k])
        conngen=nx.connected_components(H)
        conn=sorted(conngen, key = len, reverse=True)
        nodesGiant[k]=len(conn[0])
        noComponents[k]=len(conn)
    return [nodesGiant,noComponents]

def generateNetwork(N,cnType,weighted):
    # Input:
    #   N - number of nodes
    #   cnType  - network type (i.e. scale-free, small-world, Erdos-Renyi random graph)
    #   weighted - weighted or unweighted network
    # Output:
    #   G - a network with random generated topology acoording with the input parameters

    if (cnType == "scale-free"):
        G = nx.powerlaw_cluster_graph(N, 5, 0.3)
        while (nx.is_connected(G) == False):
            G = nx.powerlaw_cluster_graph(N, 5, 0.3)
    if (cnType == "small-world"):
        G = nx.newman_watts_strogatz_graph(N, 6, 0.6)
        while (nx.is_connected(G) == False):
            G = nx.newman_watts_strogatz_graph(N, 6, 0.6)
    if (cnType == "Erdos-Renyi"):
        G = nx.fast_gnp_random_graph(N, 0.01)
        while (nx.is_connected(G) == False):
            G = nx.fast_gnp_random_graph(N, 0.01)

    if (weighted):
        G = generateWeightedNetwork(G)
    else:
        G = generateUnweightedNetwork(G)

    return G