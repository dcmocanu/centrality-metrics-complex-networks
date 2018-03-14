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

import networkx as nx
import numpy as np
import library, GOT
import matplotlib.pyplot as plt
import matplotlib

def getRank(resources,col):
    ranks={}
    meanVDiamonds=np.mean(resources[:,:col],axis=1)
    got=meanVDiamonds.argsort(axis=0)
    for i in range(N):
        ranks[got[i]]=i+1
    return ranks

def createGraph():
    G = nx.Graph()
    labels = {}
    for i in range(0, 10):
        G.add_node(i)
        labels[i] = str(i)
    G.add_edge(0, 1)
    G.add_edge(0, 3)
    G.add_edge(1, 2)
    G.add_edge(1, 4)
    G.add_edge(2, 3)
    G.add_edge(2, 4)
    G.add_edge(2, 5)
    G.add_edge(3, 0)
    G.add_edge(3, 4)
    G.add_edge(5, 6)
    G.add_edge(5, 7)
    G.add_edge(7, 8)
    G.add_edge(7, 9)
    G.add_edge(8, 9)
    G.add_edge(8, 1)
    G = library.generateUnweightedNetwork(G)

    posNodes = nx.spring_layout(G)
    posNodes[0] = np.asarray([0.95, 0.05])
    posNodes[1] = np.asarray([0.95, 0.35])
    posNodes[2] = np.asarray([0.50, 0.5])
    posNodes[3] = np.asarray([0.05, 0.35])
    posNodes[4] = np.asarray([0.05, 0.05])
    posNodes[5] = np.asarray([0.50, 0.8])
    posNodes[6] = np.asarray([0.05, 0.8])
    posNodes[7] = np.asarray([0.75, 1])
    posNodes[8] = np.asarray([0.95, 1.3])
    posNodes[9] = np.asarray([0.50, 1.3])
    nodeNames = {}
    nodeNames[0] = "A"
    nodeNames[1] = "B"
    nodeNames[2] = "C"
    nodeNames[3] = "D"
    nodeNames[4] = "E"
    nodeNames[5] = "F"
    nodeNames[6] = "G"
    nodeNames[7] = "H"
    nodeNames[8] = "I"
    nodeNames[9] = "J"
    posNodesOut = posNodes.copy()
    posNodesOut[0] = np.asarray([0.95 - 0.1, 0.05 - 0.02])
    posNodesOut[1] = np.asarray([0.95 - 0.05, 0.35 + 0.08])
    posNodesOut[2] = np.asarray([0.50 + 0.1, 0.5])
    posNodesOut[3] = np.asarray([0.05, 0.35 + 0.1])
    posNodesOut[4] = np.asarray([0.05 + 0.1, 0.05])
    posNodesOut[5] = np.asarray([0.50 + 0.1, 0.8])
    posNodesOut[6] = np.asarray([0.05, 0.8 + 0.11])
    posNodesOut[7] = np.asarray([0.75 - 0.1, 1])
    posNodesOut[8] = np.asarray([0.95 - 0.08, 1.3 - 0.07])
    posNodesOut[9] = np.asarray([0.50 - 0.1, 1.3])

    return [G,posNodes,nodeNames,posNodesOut]


# set GOT parameters
N=10 #number of nodes
noThieves=3 #number of thieves per node
noVDiamonds=10 # number of vdiamonds per node
noEpochs=1000 #number of epochs

# create munually an unweighted graph for vizualization purposes
[G,posNodes,nodeNames,posNodesOut]=createGraph()

# compute nodes and edges centrality with GOT
[centralityNodesGOT, nodesSortedGOT, vdiamonds,centralityEdgesGOT, edgesSortedGOT, stopedEpoch]= GOT.ComputeCentrality(G, noThieves, noVDiamonds, noEpochs=noEpochs, untilConvergence=False)

# make GOT illustration
font = { 'size'   : 7}
fig = plt.figure(figsize=(8.3,4.5))
matplotlib.rc('font', **font)
fig.subplots_adjust(wspace=0.07,hspace=0.14)

fs=7
ns=120

plt.subplot(241)
plt.title("a) Epoch 1 (initialization)",fontsize=8)
nx.draw(G,posNodes,node_size=ns,width=1,with_labels=False,font_size=fs,cmap=plt.get_cmap('nipy_spectral'), node_color=np.mean(vdiamonds[:,:1],axis=1),vmin=0,vmax=N*noVDiamonds)
nx.draw_networkx_labels(G,posNodes,nodeNames,font_color="white",font_weight="bold",font_size=fs)


plt.subplot(242)
plt.title("b) After 2 epochs",fontsize=8)
nx.draw(G,posNodes,node_size=ns,width=1,with_labels=False,font_size=fs,cmap=plt.get_cmap('nipy_spectral'), node_color=np.mean(vdiamonds[:,:2],axis=1),vmin=0,vmax=N*noVDiamonds)
nx.draw_networkx_labels(G,posNodes,nodeNames,font_color="white",font_weight="bold",font_size=fs)
nx.draw_networkx_labels(G,posNodesOut,labels=getRank(vdiamonds,2),font_size=fs)

plt.subplot(243)
plt.title("c) After 3 epochs",fontsize=8)
nx.draw(G,posNodes,node_size=ns,width=1,with_labels=False,font_size=fs,cmap=plt.get_cmap('nipy_spectral'), node_color=np.mean(vdiamonds[:,:3],axis=1),vmin=0,vmax=N*noVDiamonds)
nx.draw_networkx_labels(G,posNodes,nodeNames,font_color="white",font_weight="bold",font_size=fs)
nx.draw_networkx_labels(G,posNodesOut,labels=getRank(vdiamonds,3),font_size=fs)

plt.subplot(244)
plt.title("d) After 4 epochs",fontsize=8)
nx.draw(G,posNodes,node_size=ns,width=1,with_labels=False,font_size=fs,cmap=plt.get_cmap('nipy_spectral'), node_color=np.mean(vdiamonds[:,:4],axis=1),vmin=0,vmax=N*noVDiamonds)
nx.draw_networkx_labels(G,posNodes,nodeNames,font_color="white",font_weight="bold",font_size=fs)
nx.draw_networkx_labels(G,posNodesOut,labels=getRank(vdiamonds,4),font_size=fs)

plt.subplot(245)
plt.title("e) After 5 epochs",fontsize=8)
nx.draw(G,posNodes,node_size=ns,width=1,with_labels=False,font_size=fs,cmap=plt.get_cmap('nipy_spectral'), node_color=np.mean(vdiamonds[:,:5],axis=1),vmin=0,vmax=N*noVDiamonds)
nx.draw_networkx_labels(G,posNodes,nodeNames,font_color="white",font_weight="bold",font_size=fs)
nx.draw_networkx_labels(G,posNodesOut,labels=getRank(vdiamonds,5),font_size=fs)

plt.subplot(246)
plt.title("f) After 100 epochs",fontsize=8)
nx.draw(G,posNodes,node_size=ns,width=1,with_labels=False,font_size=fs,cmap=plt.get_cmap('nipy_spectral'), node_color=np.mean(vdiamonds[:,:100],axis=1),vmin=0,vmax=N*noVDiamonds)
nx.draw_networkx_labels(G,posNodes,nodeNames,font_color="white",font_weight="bold",font_size=fs)
nx.draw_networkx_labels(G,posNodesOut,labels=getRank(vdiamonds,100),font_size=fs)

plt.subplot(247)
plt.title("g) After 500 epochs",fontsize=8)
nx.draw(G,posNodes,node_size=ns,width=1,with_labels=False,font_size=fs,cmap=plt.get_cmap('nipy_spectral'), node_color=np.mean(vdiamonds[:,:500],axis=1),vmin=0,vmax=N*noVDiamonds)
nx.draw_networkx_labels(G,posNodes,nodeNames,font_color="white",font_weight="bold",font_size=fs)
nx.draw_networkx_labels(G,posNodesOut,labels=getRank(vdiamonds,500),font_size=fs)

plt.subplot(248)
plt.title("h) After 1000 epochs",fontsize=8)
nx.draw(G,posNodes,node_size=ns,width=1,with_labels=False,font_size=fs,cmap=plt.get_cmap('nipy_spectral'), node_color=np.mean(vdiamonds[:,:1000],axis=1),vmin=0,vmax=N*noVDiamonds)
nx.draw_networkx_labels(G,posNodes,nodeNames,font_color="white",font_weight="bold",font_size=fs)
nx.draw_networkx_labels(G,posNodesOut,labels=getRank(vdiamonds,1000),font_size=fs)

plt.savefig("GOT_illustration.pdf", bbox_inches='tight')
plt.close()

print "GOT illustration figure was made"

