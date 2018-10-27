from __future__ import division
from __future__ import print_function
from six.moves import range

import random
import itertools

import networkx as nx


def generate_chordal_graph(n, d, block_size):
  G = nx.Graph()
  G.add_nodes_from(range(n))
  for v in range(n-1, 0, -1):
    clique = {v}
    clique.update(u for u in G.neighbors(v) if u < v)
    min_val = max(0, v - block_size)
    clique.add(random.choice(range(min_val, v)))
    for u in range(min_val, v):
      if random.random() <= d / block_size:
        clique.add(u)
    clique_edges = itertools.combinations(clique, r=2)
    G.add_edges_from(clique_edges)
  return G
