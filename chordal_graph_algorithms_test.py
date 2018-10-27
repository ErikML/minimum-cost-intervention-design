import unittest

import networkx as nx

from chordal_graph_algorithms import lex_bfs, color_chordal_graph, mwis_chordal_graph

class ChordalGraphAlgorithmsTest(unittest.TestCase):

  def testLexBFSOn3Tree(self):
    T = nx.Graph()
    # 0 -- 1 -- 2
    T.add_edges_from([(0, 1), (1, 2)])
    peo_actual = lex_bfs(T)
    peo_expected = [0, 1, 2]
    self.assertEqual(peo_actual, peo_expected)

  def testLexBFSOn6Tree(self):
    T = nx.Graph()
    #        6
    #     /    \
    #    4      5
    #  /  \   /  \
    # 0   1  2    3
    T.add_edges_from([(0, 4), (1, 4), (2, 5), (3, 5), (4, 6), (5, 6)])
    peo_actual = lex_bfs(T)
    peo_expected = [0, 4, 1, 6, 5, 2, 3]
    self.assertEqual(peo_actual, peo_expected)

  def testLexBFSOn3Cycle(self):
    #    1
    #  /  \
    # 0 - 2
    C = nx.Graph()
    C.add_edges_from([(0, 1), (0, 2), (1, 2)])
    peo_actual = lex_bfs(C)
    peo_expected = [0, 1, 2]
    self.assertEqual(peo_actual, peo_expected)

  def testLexBFSOnTriforce(self):
    #        0
    #      /  \
    #     1 -  2
    #   /  \ /  \
    #  3 -  4 - 5
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5),
                      (3, 4), (4, 5)])
    peo_actual = lex_bfs(G)
    #peo_expected = [0, 1, 2]
    #self.assertEqual(peo_actual, peo_expected)

  def testColoringOn3Tree(self):
    T = nx.Graph()
    # 0 -- 1 -- 2
    T.add_edges_from([(0, 1), (1, 2)])
    coloring = color_chordal_graph(T)
    self.assertNotEqual(coloring[0], coloring[1])
    self.assertNotEqual(coloring[1], coloring[2])
    self.assertEqual(set(coloring.values()), {0, 1})

  def testColoringOn3Cycle(self):
    #    1
    #  /  \
    # 0 - 2
    C = nx.Graph()
    C.add_edges_from([(0, 1), (0, 2), (1, 2)])
    coloring = color_chordal_graph(C)
    self.assertEqual(set(coloring.keys()), set(range(3)))
    self.assertEqual(set(coloring.values()), set(range(3)))

  def testColoringOnTriforce(self):
    #        0
    #      /  \
    #     1 -  2
    #   /  \ /  \
    #  3 -  4 - 5
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5),
                      (3, 4), (4, 5)])
    coloring = color_chordal_graph(G)
    self.assertEqual(set(coloring.keys()), set(range(6)))
    self.assertEqual(set(coloring.values()), set(range(3)))
    for u,v in G.edges():
      self.assertNotEqual(coloring[u], coloring[v])

  def testMWISOnTriforceUnweighted(self):
    #        0
    #      /  \
    #     1 -  2
    #   /  \ /  \
    #  3 -  4 - 5
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5),
                      (3, 4), (4, 5)])
    for v in range(6):
      G.node[v]['weight'] = 1
    mwis_actual = mwis_chordal_graph(G)
    mwis_expected = [0, 3, 5]
    self.assertEqual(mwis_actual, mwis_expected)

  def testMWISOnTriforceWeighted(self):
    #        0
    #      /  \
    #     1 -  2
    #   /  \ /  \
    #  3 -  4 - 5
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5),
                      (3, 4), (4, 5)])
    for v in range(6):
      G.node[v]['weight'] = 1
    G.node[2]['weight'] = 3
    mwis_actual = mwis_chordal_graph(G)
    mwis_expected = [2, 3]
    self.assertEqual(mwis_actual, mwis_expected)