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
import random as rd

class Thief:
    # this is the basic implementation of a thief behaviour
    def __init__(self, origin):
        self.origin = origin
        self.position = origin
        self.diamond=0
        self.path=[]
        
    def Move(self,G,k):
        if (self.diamond==0):
            self.Search(G)
            if (self.position!=self.origin):
                self.TakeDiamond(G)
        else:
            self.Back(G,k)
            
    def Search(self,G):
        neighboursList = G[self.position]
        moveProb=np.zeros(len(neighboursList))
        sumWeights=0
        for neighbour in neighboursList:
            sumWeights+=G.edges[self.position,neighbour]['value']

        i=0
        for neighbour in neighboursList:
            moveProb[i]=(float)(G.edges[self.position,neighbour]['value'])/sumWeights
            i+=1

        rdProb=rd.random()
        sumProb=0
        i = 0
        for neighbour in neighboursList:
            sumProb+=moveProb[i]
            if (sumProb>=rdProb):
                moveTo=neighbour
                break
            i += 1
        try: 
            index=self.path.index(moveTo)
        except ValueError:
            index=-1

        if (index>-1):
            for i in range(index+1,len(self.path)):
                del self.path[-1]

        self.path.append(self.position)
        self.position=moveTo
        if (self.origin==self.position):  
            self.path=[]   

    def TakeDiamond(self,G):
        if (G.node[self.position]['vdiamonds']>0):
            G.node[self.position]['vdiamonds']-=1
            self.diamond=1
        
    def Back(self,G,epo):
        currentEdge=G.get_edge_data(self.position,self.path[-1])
        thiefsPasses=currentEdge['thiefsPasses']+1
        G.add_edge(self.position,self.path[-1],thiefsPasses=thiefsPasses)

        self.position=self.path[-1]
        del self.path[-1]
        if (self.position==self.origin):
            self.path=[]
            self.diamond=0
            self.position=self.origin
            G.node[self.position]['vdiamonds']+=1

