from math import floor

import networkx as nx


def glock_graph(n: int, r: int):
    """
    @see riis2006information Information flows, graphs and their guessing numbers (2006)
    """
    assert n > 1
    assert r <= floor((n - 1) / 2)

    def has_edge(u, v):
        return 0 < (u - v) % n <= r

    G = nx.empty_graph(0, nx.DiGraph)
    G.add_nodes_from(i for i in range(n))
    G.add_edges_from((u, v) for u in range(n) for v in range(n) if has_edge(u, v))

    return G
