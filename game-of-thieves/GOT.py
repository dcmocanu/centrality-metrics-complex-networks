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
import random
import networkx as nx
import Thief

def initializeGOTGraph(G,noNodes, noVDiamonds):

    #initialize the amount of vdiamonds per node
    for i in range(noNodes):
        G.node[i]['vdiamonds']=noVDiamonds

    # initialize the thieves passes per edge
    for edge in G.edges():
        G.add_edge(edge[0], edge[1], thiefsPasses=0)

    return G


def ComputeCentrality(G, noThiefs, noVDiamonds,noEpochs, untilConvergence=False, noLastEuclidDists = 10):
    # This is the sequential version of GOT
    # Input:
    #   G - network to be analyzed
    #   noThiefs - number of thieves per node
    #   noVDiamonds - number of vdiamonds per node
    #   noEpochs - number of epochs to run the algorithms
    #   untilConvergence - if this parameter is set to True then at each epoch the stopping criteria is checked, otherwise GOT will just run for the given amount of epochs (default False)
    #   noLastEuclidDists - for how many consecutive epochs the stopping criteria is checked (default 10)
    # Output:
    #   meanVDiamonds - the average amount of vdiamonds per node after the algorithm stops
    #   sortedNodes - an array with all nodes sorted according with their centrality (from the most important ones to the least important ones)
    #   vdiamonds - an array with the number of vdiamonds in each nodes at every epoch
    #   meanPassesEdges - the average amount of thieves passes per edge after the algorithm stops
    #   sortedEdges - an array with all edges sorted according with their centrality (from the most important ones to the least important ones)
    #   k - the number of the epoch when GOT was stopped

    random.seed()
    noNodes=nx.number_of_nodes(G)
    noEdges = G.number_of_edges()

    # initialize GOT parameters on the graph
    G = initializeGOTGraph(G, noNodes, noVDiamonds)

    # initialize a list with theives
    thiefsList = []

    edgesList = np.zeros((noEdges,2))
    i=0
    for edge in G.edges(data=True):
        edgesList[i] = np.asarray([edge[0], edge[1]])
        i += 1

    vdiamonds = np.zeros((noNodes, noEpochs))
    passesEdges = np.zeros((noEdges, noEpochs))
    previousNodesRank = np.zeros(noNodes)
    lastEuclidDists = noNodes + np.zeros(noLastEuclidDists)

    # run GOT for a specific number of epochs or until convergence
    k = 0
    while (k < noEpochs):
        k += 1

        # make a move for each thief
        for thief in thiefsList:
            thief.Move(G, k)

        # in the first epoch create the thieves for each node
        if (k == 1):
            for i in range(noNodes):
                if (G.neighbors(i) != []):
                    for j in range(noThiefs):
                        thiefsList.append(Thief.Thief(i))

        # store the amount of vdiamonds from each node at epoch k
        for i in range(noNodes):
            vdiamonds[i, k - 1] = G.node[i]['vdiamonds']

        # store the number of thieves passes on each edge at epoch k
        i = 0
        for edge in G.edges(data=True):
            passesEdges[i, k - 1] = edge[2]['thiefsPasses']
            i += 1

        # if the GOT algorithm runs until convergence than GOT centrality has to be computed at each epoch
        # please pay attention as in this way the algorithm is much slower due to the extra computations needed
        if (untilConvergence):

            meanVDiamonds = np.mean(vdiamonds[:, :k],axis=1)
            sortedNodes = meanVDiamonds.argsort(axis=0)

            nodesRank = np.zeros(noNodes)
            for i in range(noNodes):
                nodesRank[sortedNodes[i]] = i
            euclidDist = np.sqrt(((nodesRank - previousNodesRank) * (nodesRank - previousNodesRank)).sum())
            lastEuclidDists = np.roll(lastEuclidDists, -1)
            lastEuclidDists[noLastEuclidDists - 1] = euclidDist
            previousNodesRank = nodesRank

            # if stoping criteria is fullfiled then stop the algorithm
            if ((np.mean(lastEuclidDists) < 0.02 * noNodes)):
                sortedEdges=np.zeros((noEdges,1,2))
                meanPassesEdges = np.mean(passesEdges[:, :k],axis=1)
                sortedEdgesIndex = meanPassesEdges.argsort(axis=0)[::-1]
                for i in range(noEdges):
                    sortedEdges[i,0]=edgesList[sortedEdgesIndex[i]]
                return [meanVDiamonds, sortedNodes, vdiamonds, meanPassesEdges, sortedEdges, k]

    # compute the rank of nodes and edges
    meanVDiamonds = np.mean(vdiamonds[:, :k], axis=1)
    sortedNodes = meanVDiamonds.argsort(axis=0)

    sortedEdges = np.zeros((noEdges, 1, 2))
    meanPassesEdges = np.mean(passesEdges[:, :k], axis=1)
    sortedEdgesIndex = meanPassesEdges.argsort(axis=0)[::-1]
    for i in range(noEdges):
        sortedEdges[i,0] = edgesList[sortedEdgesIndex[i]]
    return [meanVDiamonds, sortedNodes, vdiamonds,meanPassesEdges, sortedEdges, k]
