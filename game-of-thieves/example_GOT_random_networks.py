# Author: Decebal Constantin Mocanu;
# Proof of concept implementation of the Game of Thieves (GoT) - a metric to compute nodes and links centrality in complex networks or graphs;
# This is a pre-alpha free software and was tested with Python 2.7.12, Matplotlib 2.1.0, Numpy 1.14, NetworkX 2.0;
# The software is distributed in the hope that it may be useful, but WITHOUT ANY WARRANTIES; The use of this software is entirely at the user's own risk;
# For an easy understanding of the software functionality please read the following article.

# If you use this software please cite its corresponding article:
#@article{Mocanu2018GOT,
#  author =        {Mocanu, Decebal Constantin and Exarchakos, Georgios and Liotta, Antonio},
#  journal =       {Scientific Reports},
#  title =         {Decentralized dynamic understanding of hidden relations in complex networks},
#  volume =        {8},
#  year =          {2018},
#  doi =           {10.1038/s41598-018-19356-4},
#  url =           {https://www.nature.com/articles/s41598-018-19356-4}
#}

import networkx as nx
import numpy as np
import library, GOT
import datetime

# set GOT parameters
N=1000 #number of nodes
noThieves=1 #number of thieves per node (setting it to 1 shall give acceptable results)
noVDiamonds=N # number of vdiamonds per node (setting it to the number of nodes shall give acceptable results)
noEpochs=int(np.power(np.log(N),3)) #number of epochs (acceptable results shall be between np.power(np.log(N),2) and np.power(np.log(N),3))

# set the type of the generated network
networkType=["scale-free","small-world","Erdos-Renyi"]
cnType= networkType[0] #choose one of the above three network types
weighted=False #set this to True if you would like to generate an weighted network

# generate a random network (here in you can create or use your own network)
G= library.generateNetwork(N, cnType, weighted)
print "Generated a ",cnType," network."

# compute nodes and edges centrality with GOT
t1=datetime.datetime.now()
[centralityNodesGOT, nodesSortedGOT, vdiamonds,centralityEdgesGOT, edgesSortedGOT, stopedEpoch]= GOT.ComputeCentrality(G, noThieves, noVDiamonds, noEpochs=noEpochs, untilConvergence=False)
t2=datetime.datetime.now()

# Nodes removal procedure on nodes centrality given by GOT to compute the size of the Giant Component and the number of Connected Components
t3=datetime.datetime.now()
[nodesRemovalSizeGiantComponentGOT, nodesRemovalNoConnectedComponentsGOT] = library.nodesRemovalProcedure(G, nodesSortedGOT)
[edgesRemovalSizeGiantComponentGOT, edgesRemovalNoConnectedComponentsGOT] = library.edgesRemovalProcedure(G, edgesSortedGOT)
t4=datetime.datetime.now()
print "GOT stopped after ",stopedEpoch," epochs and run in ",t2-t1," seconds, while nodes and edges removal procedures in ",t4-t3," seconds."

# compute nodes centrality with Betweenness centrality
t1=datetime.datetime.now()
nodesBetweenessCentrality=nx.betweenness_centrality(G)
edgesBetweenessCentrality=nx.edge_betweenness_centrality(G,weight="value")
t2=datetime.datetime.now()

#process Betweenness centrality results
centralityNodesBetweeness=np.zeros(N)
for i in range(N):
    centralityNodesBetweeness[i] = nodesBetweenessCentrality[i]
nodesSortedBetweenness=centralityNodesBetweeness.argsort(axis=0)[::-1]
edgesSortedBetweenness = [x for x in edgesBetweenessCentrality.iteritems()]
edgesSortedBetweenness.sort(key=lambda x: x[1]) # sort by value
edgesSortedBetweenness.reverse()

# Nodes and edges removal procedure on nodes and edges centrality given by Betweenness centrality to compute the size of the Giant Component and the number of Connected Components
t3=datetime.datetime.now()
[nodesRemovalSizeGiantComponentBetweenness, nodesRemovalNoConnectedComponentsBetweenness]= library.nodesRemovalProcedure(G, nodesSortedBetweenness)
[edgesRemovalSizeGiantComponentBetweenness, edgesRemovalNoConnectedComponentsBetweenness] = library.edgesRemovalProcedure(G, edgesSortedBetweenness)
t4=datetime.datetime.now()
print "Betweenness centrality for nodes and edges run in ",t2-t1," seconds, while nodes and edges removal procedures in ",t4-t3," seconds."

print "\nResults:\n"
print "Area under the curve (AUC) for NODES removal procedure: "
print "AUC giant component (smaller value is better) with GOT centrality: ",np.sum(nodesRemovalSizeGiantComponentGOT)
print "AUC giant component (smaller value is better) with Betweenness centrality: ",np.sum(nodesRemovalSizeGiantComponentBetweenness)
print "AUC number of connected components (higher value is better) with GOT centrality: ",np.sum(nodesRemovalNoConnectedComponentsGOT)
print "AUC number of connected components (higher value is better) with Betweenness centrality: ",np.sum(nodesRemovalNoConnectedComponentsBetweenness)

print "\n"
print "Area under the curve (AUC) for EDGES removal procedure: "
print "AUC giant component (smaller value is better) with GOT centrality: ",np.sum(edgesRemovalSizeGiantComponentGOT)
print "AUC giant component (smaller value is better) with Betweenness centrality: ",np.sum(edgesRemovalSizeGiantComponentBetweenness)
print "AUC number of connected components (higher value is better) with GOT centrality: ",np.sum(edgesRemovalNoConnectedComponentsGOT)
print "AUC number of connected components (higher value is better) with Betweenness centrality: ",np.sum(edgesRemovalNoConnectedComponentsBetweenness)



