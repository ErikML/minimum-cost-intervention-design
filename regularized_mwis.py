from chordal_graph_generators import generate_chordal_graph
from chordal_graph_algorithms import mwis_chordal_graph, color_chordal_graph
import networkx as nx
import numpy as np

def k_sparse_mcid(G, k, lambd):
  G = G.copy()
  for v in G:
    G.node[v]['weight'] += lambd
  S = mwis_chordal_graph(G)
  G.remove_nodes_from(S)
  coloring = color_chordal_graph(G)
  color_classes = {}
  for v in G:
    c = coloring[v]
    if c in color_classes:
      color_classes[c].append(v)
    else:
      color_classes[c] = [v]
  splits = []
  for S in color_classes.values():
    splits.extend(split_into_size_k(S, k))
  return splits

def split_into_size_k(S, k):
  splits = []
  curr_split = []
  for v in S:
    curr_split.append(v)
    if len(curr_split) == k:
      splits.append(curr_split)
      curr_split = []
  if curr_split:
    splits.append(curr_split)
  return splits

def get_vc(G):
  G = G.copy()
  for v in G:
    G.node[v]['weight'] = 1
  S = mwis_chordal_graph(G)
  return len(G) - len(S)

lambdas = [0, 1, 2, 5, 10, 20, 50, 100]


costs = {}
sizes = {}
for lambd in lambdas:
  costs[lambd] = []
  sizes[lambd] = []

TRIALS = 20
n = 10000
k = 10
d = 0.1
block_size = 10
avg_degree = 0.0
avg_size = 0.0
avg_cost = 0.0
avg_vc = 0.0
for _ in range(TRIALS):
  G = generate_chordal_graph(n, d, block_size)
  for v in G:
    G.node[v]['weight'] = 10.0 * np.random.pareto(2.0)
  avg_degree += len(G.edges) * 2 / len(G)
  for lambd in lambdas:
    splits = k_sparse_mcid(G, k, lambd)
    cost = 0.0
    for s in splits:
      for v in s:
        cost += G.node[v]['weight']
    costs[lambd].append(cost)
    sizes[lambd].append(len(splits))
  vc = get_vc(G)
  avg_vc += vc
  avg_size += len(splits)
  for s in splits:
    for v in s:
      avg_cost += G.node[v]['weight']

max_cost = 0.0
for lambd in lambdas:
  avg_cost = sum(costs[lambd]) / float(TRIALS)
  if avg_cost > max_cost:
    max_cost = avg_cost

for lambd in lambdas:
  avg_size = sum(sizes[lambd]) / float(TRIALS)
  avg_cost = sum(costs[lambd]) / float(TRIALS) / max_cost
  print('{} {}'.format(avg_size, avg_cost))
print(avg_degree / float(TRIALS))
print(avg_vc / k / float(TRIALS))

