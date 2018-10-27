from __future__ import division
from __future__ import print_function
from six.moves import range

import numpy as np
from chordal_graph_generators import generate_chordal_graph
import mcid

n = 500
m = 5
b = 10
chi_coloring_cost = []
greedy_coloring_cost = []
ip_coloring_cost = []
trials = 20
for d in [0.1, 0.3, 0.5, 1.0, 1.5, 2.0]:
  avg_degree = []
  chi_c = []
  greedy_c = []
  ip_c = []
  for _ in range(trials):
      G = generate_chordal_graph(n, d, b)
      avg_degree.append(G.number_of_edges() * 2 / len(G))
      for v in G:
        G.node[v]['weight'] = np.random.pareto(2.0)
      I_greedy = mcid.mcid(G, m)
      I_chi = mcid.create_interventions_from_coloring(G, mcid.baseline(G), m)
      greedy_c.append(mcid.cost(G, I_greedy))
      chi_c.append(mcid.cost(G, I_chi))
      ip_c.append(mcid.ip_coloring(G, m))
  avg_degree = np.mean(avg_degree)
  chi_coloring_cost.append(
    (avg_degree, np.mean(chi_c), 2 * np.std(chi_c, ddof=1) / np.sqrt(trials)))
  greedy_coloring_cost.append(
    (avg_degree, np.mean(greedy_c), 2 * np.std(greedy_c, ddof=1) / np.sqrt(trials)))
  ip_coloring_cost.append(
    (avg_degree, np.mean(ip_c), 2 * np.std(ip_c, ddof=1) / np.sqrt(trials)))
for D in [greedy_coloring_cost, chi_coloring_cost, ip_coloring_cost]:
  for a, b, c in D:
    print('{} {} {}'.format(a, b, c))
  print()