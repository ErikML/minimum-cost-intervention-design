from __future__ import division
from __future__ import print_function
from six.moves import range

import numpy as np
from chordal_graph_generators import generate_chordal_graph
import mcid

import time

d = 1.0
m = 5
b = 10
chi_coloring_cost = []
greedy_coloring_cost = []
ip_coloring_cost = []
trials = 5
t_greedy = []
t_ip = []
avg_degree = []
for n in [10000]:
  chi_c = []
  greedy_c = []
  ip_c = []
  avg_degree_n = []
  for _ in range(trials):
      G = generate_chordal_graph(n, d, b)
      avg_degree_n.append(G.number_of_edges() * 2 / len(G))
      for v in G:
        G.node[v]['weight'] = np.random.pareto(2.0)
      t = time.time()
      I_greedy = mcid.mcid(G, m)
      t_greedy.append(time.time() - t)
      I_chi = mcid.create_interventions_from_coloring(G, mcid.baseline(G), m)
      greedy_c.append(mcid.cost(G, I_greedy))
      chi_c.append(mcid.cost(G, I_chi))
      t = time.time()
      ip_c.append(mcid.ip_coloring(G, m))
      t_ip.append(time.time() - t)
  avg_degree.append(np.mean(avg_degree_n))
  chi_coloring_cost.append(
    (n, np.mean(chi_c), 2 * np.std(chi_c, ddof=1) / np.sqrt(trials)))
  greedy_coloring_cost.append(
    (n, np.mean(greedy_c), 2 * np.std(greedy_c, ddof=1) / np.sqrt(trials)))
  ip_coloring_cost.append(
    (n, np.mean(ip_c), 2 * np.std(ip_c, ddof=1) / np.sqrt(trials)))
print(avg_degree)
for D in [greedy_coloring_cost, chi_coloring_cost, ip_coloring_cost]:
  for a, b, c in D:
    print('{} {} {}'.format(a, b, c))
  print()

print()
print('t greedy: {}'.format(np.mean(t_greedy)))
print('t ip: {}'.format(np.mean(t_ip)))