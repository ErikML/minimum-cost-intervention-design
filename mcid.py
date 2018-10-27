from __future__ import division
from __future__ import print_function
from six.moves import range

import itertools
from collections import defaultdict

try:
  import gurobipy as grb
except ImportError:
  grb = None

from chordal_graph_algorithms import mwis_chordal_graph, color_chordal_graph


def ip_coloring(G, m):
  colors = []
  color_vector_gen = _color_vector_gen(m)
  while len(colors) < len(G):
    try:
      colors.append(next(color_vector_gen))
    except StopIteration:
      break
  m = grb.Model('min_coloring')
  vertex_color_cost_dict = {}
  for v, data in G.nodes(data=True):
    weight = data['weight']
    for k in range(len(colors)):
      vertex_color_cost_dict[(v, k)] = weight * sum(colors[k])
  vertex_color_id, vertex_color_cost = grb.multidict(vertex_color_cost_dict)
  vertex_color_state = m.addVars(vertex_color_id, lb=0, ub=1, name='vertex_colors', vtype=grb.GRB.BINARY)
  for v in G:
    variables = [vertex_color_state[(v, k)] for k in range(len(colors))]
    expr = grb.quicksum(variables)
    m.addConstr(expr, grb.GRB.EQUAL, 1)
  for u, v in G.edges():
    for k in range(len(colors)):
      m.addConstr(vertex_color_state[(u, k)] + vertex_color_state[(v, k)] <= 1)
  m.setObjective(vertex_color_state.prod(vertex_color_cost), grb.GRB.MINIMIZE)
  m.optimize()
  if m.status == grb.GRB.Status.OPTIMAL:
    print(m.getAttr('x', vertex_color_state))
    print('cost: {}'.format(m.objVal))
    return m.objVal
  else:
    print('No Solution Found')
    return None


def mcid(G, m):
  coloring = greedy_coloring(G)
  return create_interventions_from_coloring(G, coloring, m)


def create_interventions_from_coloring(G, coloring, m):
  colors = sorted(list(set(coloring.values())))
  colors_to_vector = {}
  color_vector_gen = _color_vector_gen(m)
  color_weights = defaultdict(int)
  for v in coloring:
    c = coloring[v]
    color_weights[c] += G.node[v]['weight']
  for c in sorted(colors, key=lambda x: color_weights[x], reverse=True):
    colors_to_vector[c] = next(color_vector_gen)
  interventions = {}
  for v in G:
    color = coloring[v]
    interventions[v] = colors_to_vector[color]
  return interventions


def cost(G, I):
  cost = 0
  for v, interventions in I.items():
    cost += G.node[v]['weight'] * sum(interventions)
  return cost

def baseline(G):
  G = G.copy()
  S = mwis_chordal_graph(G)
  G.remove_nodes_from(S)
  coloring = color_chordal_graph(G)
  for v in S:
    coloring[v] = -1
  return coloring


def greedy_coloring(G):
  G = G.copy()
  coloring = {}
  color_gen = itertools.count()
  while G:
    w = mwis_chordal_graph(G)
    G.remove_nodes_from(w)
    next_color = next(color_gen)
    for v in w:
      coloring[v] = next_color
  return coloring

def _weight_k_vectors(m, k):
  for x in itertools.combinations(range(m), k):
    y = [0] * m
    for i in x:
      y[i] = 1
    yield y

def _color_vector_gen(m):
  iterables = [_weight_k_vectors(m, k) for k in range(m+1)]
  return itertools.chain(*iterables)
