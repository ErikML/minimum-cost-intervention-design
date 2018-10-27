from __future__ import division
from __future__ import print_function
from six.moves import range

import heapq


def mwis_chordal_graph(G):
  G = G.copy()
  peo = perfect_elimination_ordering(G)
  position = {}
  for i, v in enumerate(peo):
    position[v] = i
  red_nodes = set()
  for v in reversed(peo):
    if G.node[v]['weight'] > 0:
      red_nodes.add(v)
      for u in G[v]:
        if position[u] < position[v]:
          new_weight = max(0, G.node[u]['weight'] - G.node[v]['weight'])
          G.node[u]['weight'] = new_weight
      G.node[v]['weight'] = 0
  blue_nodes = set()
  for v in peo:
    if v in red_nodes:
      if set(G[v]).isdisjoint(blue_nodes):
        blue_nodes.add(v)
  return sorted(list(blue_nodes))


def color_chordal_graph(G):
  peo = perfect_elimination_ordering(G)
  coloring = {}
  current_max_color = -1
  current_colors = set()
  for v in peo:
    neighbor_colors = set(coloring.get(u, -1) for u in G[v])
    free_colors = current_colors - neighbor_colors
    if free_colors:
      coloring[v] = min(free_colors)
    else:
      coloring[v] = current_max_color + 1
      current_max_color += 1
      current_colors.add(current_max_color)
  return coloring


def perfect_elimination_ordering(G):
  return lex_bfs(G)


def lex_bfs(G):
  G = G.copy()
  peo = []
  top_block = _LexBFSDoublyLinkedListNode(label=())
  for v in G:
    top_block.add_vertex(v)
  node_block_dict = {v: top_block for v in G}
  for i in range(len(G)-1, -1, -1):
    while top_block.parent is not None:
      top_block = top_block.parent
    while top_block.is_empty:
      top_block = top_block.child
      top_block.parent = None
    v = top_block.pop_min_vertex()
    peo.append(v)
    for u in G[v]:
      block = node_block_dict[u]
      new_label = block.label + (i,)
      if block.parent is None or block.parent.label != new_label:
        new_block = _LexBFSDoublyLinkedListNode(new_label)
        block.insert_parent(new_block)
        if block.label == top_block.label:
          top_block = new_block
      else:
        new_block = block.parent
      new_block.add_vertex(u)
      block.remove_vertex(u)
      node_block_dict[u] = new_block
    G.remove_node(v)
  return peo


class _LexBFSDoublyLinkedListNode(object):

  def __init__(self, label):
    self.label = label
    self.parent = None
    self.child = None
    self._vertex_heap = []
    self._removed_vertices = set()

  def add_vertex(self, v):
    heapq.heappush(self._vertex_heap, v)

  def pop_min_vertex(self):
    v = heapq.heappop(self._vertex_heap)
    while v in self._removed_vertices:
      self._removed_vertices.remove(v)
      v = heapq.heappop(self._vertex_heap)
    return v

  def remove_vertex(self, v):
    self._removed_vertices.add(v)

  @property
  def is_empty(self):
      return len(self._vertex_heap) - len(self._removed_vertices) == 0

  def insert_parent(self, new_parent):
    if self.parent is not None:
      new_parent.parent = self.parent
      self.parent.child = new_parent
    self.parent = new_parent
    new_parent.child = self

  def insert_child(self, new_child):
    if self.child is not None:
      new_child.child = self.child
      self.child.parent = new_child
    self.child = new_child
    new_child.parent = self

  def remove(self):
    if self.parent is not None:
      self.parent.child = self.child
    if self.child is not None:
      self.child.parent = self.parent




