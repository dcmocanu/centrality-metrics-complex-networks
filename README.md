# centrality-metrics-complex-networks
Proof of concept implementations of various centrality metrics for complex networks developed by us;
The following implementations are distributed in the hope that they may be useful, but WITHOUT ANY WARRANTIES; Their use is entirely at the user's own risk.

Implementation 1 (game-of-thieves):

Game of Thieves (GoT) is a decentralized algorithm, inspired by swarm intelligence, which computes nodes and links centrality in complex networks or graphs;
This code is a pre-alpha free software and was tested with Python 2.7.12, Matplotlib 2.1.0, Numpy 1.14, NetworkX 2.0;
For an easy understanding of its behavior please read its corresponding article.

If you will use this code in your work please cite the article:
@article{Mocanu2018GOT,
  author =        {Mocanu, Decebal Constantin and Exarchakos, Georgios and Liotta, Antonio},
  journal =       {Scientific Reports},
  title =         {Decentralized dynamic understanding of hidden relations in complex networks},
  volume =        {8},
  year =          {2018},
  doi =           {10.1038/s41598-018-19356-4},
  url =           { https://www.nature.com/articles/s41598-018-19356-4 }
}

GoT examples: 

_ "game-of-thieves/example_GOT_illustration.py" is creating a nice visualization of GOT behavior (similar with Figure 1 from the paper);

_ "game-of-thieves/example_GOT_random_networks.py" is running GOT on a random generated network.
