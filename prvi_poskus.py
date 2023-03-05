"""
Ideja: če graf ni ET, potem obstaja kritičen par povezav (ki nista "enaki"),
se pravi nimata iste (upajmo, da majhne) okolice.

Poskusimo najti dve "majhni" okolici, za kateri to ne velja ...
Ena od povezav v njih je kriva za nesorazmernost ciklov
"""

import networkx as nx
# import tqdm
from stuff import convert_to_nx, create_logger
from typing import Tuple
from johnson import simple_cycles_my

"""

0  ----- 1 ----- 2 ----3 ----- 4
         |                     |
         -----------------------



"""


LOGGER = create_logger(__file__)


def find_spurious_edge_r(line_graph: nx.Graph, radius: int):
    edges = [(a, b) for a, b in sorted(line_graph.nodes) if a == 0]  # only those that start in 0
    g1 = nx.ego_graph(line_graph, edges[0], radius=radius, undirected=True)  # can always take this one
    # maybe this would be even faster (when finding cycles):
    # - find a pair (e1, e2, radius)
    # - find a pair with a smaller radius
    for j in range(1, len(edges)):
        g2 = nx.ego_graph(line_graph, edges[j], radius)
        if not nx.is_isomorphic(g1, g2):
            return edges[0][1], edges[j][1]
    return None, None


def find_spurious_edge(graph: nx.Graph):
    line_graph = nx.line_graph(graph)
    for r in range(2, graph.order()):
        # Useless: r = 1
        v1, v2 = find_spurious_edge_r(line_graph, r)
        if v1 is not None:
            return r, v1, v2
    raise ValueError(f"Did not find two different edges for {graph}")


def swap_dict(n, v1, v2):
    if v1 > v2:
        raise ValueError("v1 < v2")
    mapping = dict(zip(range(n), range(n)))
    if v2 < n - 2:
        # no match
        mapping[v1], mapping[n - 2] = n - 2, v1
        mapping[v2], mapping[n - 1] = n - 1, v2
    elif v2 == n - 2:
        # one match: case1
        mapping[v1], mapping[n - 1] = n - 1, v1
    elif v1 < n - 2 and v2 == n - 1:
        # one match: case2
        mapping[v1], mapping[n - 2] = n - 2, v1
    # else: two matches
    if mapping[v1] > mapping[v2]:
        mapping[v1], mapping[v2] = mapping[v2], mapping[v1]
    return mapping


def test():
    n = 100
    for i in range(n):
        for j in range(i + 1, n):
            d = swap_dict(n, i, j)
            if d[i] != n - 2 or d[j] != n - 1:
                raise ValueError(f"{i} {j}: {d[i]} != {n - 2} or {d[j]} != {n - 1}")


test()


def relabel_graph(graph, v1, v2):
    n = graph.order()
    # min(v1, v2) --> n - 2
    # max(v1, v2) --> n - 1
    # So that they are the last to be put on the stack
    mapping = swap_dict(n, min(v1, v2), max(v1, v2))
    return nx.relabel_nodes(graph, mapping, copy=True), mapping[v1], mapping[v2]


def solve(graph: nx.Graph):
    r, v1, v2 = find_spurious_edge(graph)
    LOGGER.info(f"nodes: {graph.order()}; r = {r} ({v1} and {v2})")
    graph_relabeled, v1, v2 = relabel_graph(graph, v1, v2)
    counts = {}  # {k: {v: count, ...}, ...}  for cycles starting at 0 and continuing at v
    other_counts = {}
    total_count = 0
    checked_once = False
    for k, c in simple_cycles_my(graph_relabeled.to_directed(as_view=False)):
        used = counts
        if not (c[1] == v1 or c[1] == v2):
            if c[0] != 0:
                break
            if not checked_once:
                checked_once = True
                LOGGER.info(f"Total count and lengths: TOT = {total_count}, ks = {sorted(counts)}")
                if total_count == 0:
                    raise ValueError("!?")
                if not report(counts):
                    return
                LOGGER.info("All are equal. Lol")
            used = other_counts
        else:
            total_count += 1
        if k == 2:
            continue
        v = c[1]
        update_counts(used, k, v)
    if not report(other_counts):
        raise ValueError(f"counts = {counts}\ntotal = {other_counts}")


def update_counts(counts, k, v):
    if k not in counts:
        counts[k] = {}
    cs = counts[k]
    if v not in cs:
        cs[v] = 1
    else:
        cs[v] += 1


def report(counts):
    for k, pairs in sorted(counts.items()):
        s = set(pairs.values())
        if len(s) != 1 or len(pairs) == 1:
            LOGGER.info(f"Not all equal: {k} --> {pairs}")
            return False
        else:
            LOGGER.info(f"all equal: {k} --> {pairs}")
    LOGGER.info("All are equal. Lol")
    return True


def solve_all():
    graphs = convert_to_nx("cvt-100.csv")
    for i, g in enumerate(graphs):
        LOGGER.info(f"Graph {i}")
        solve(g)
        print("")


if __name__ == '__main__':
    solve_all()
