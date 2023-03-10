import networkx as nx
import queue
import numpy as np

from stuff import convert_to_nx_simple, create_logger, convert_to_nx
from johnson import simple_cycles_my


LOGGER = create_logger(__file__)


def nx_to_matrix(g: nx.Graph, is_test: bool):
    max_degree = max(len(g[node]) for node in g)
    if max_degree != 3:
        # test
        LOGGER.warning(f"Max degree of g is {max_degree}")
    m = [[-1 for _ in range(max_degree)] for _ in range(g.order())]
    for x, y in g.edges:
        i = 0
        while m[x][i] >= 0:
            i += 1
        m[x][i] = y
        i = 0
        while m[y][i] >= 0:
            i += 1
        m[y][i] = x
    # le za test
    for j, row in enumerate(m):
        for i in range(len(row)):
            if row[i] < 0:
                if is_test:
                    row[i] = j  # samososed: vedno bo prisoten v verigi -> nikoli dodan
                else:
                    raise ValueError("!?")
    return m


def decode(s_code):
    present = []
    i = 0
    while s_code:
        if s_code % 2 == 1:
            present.append(i)
        i += 1
        s_code >>= 1
    return present


def is_regular(graph: nx.Graph, is_test: bool = False, the_node: int = 0):
    matrix = nx_to_matrix(graph, is_test)
    n = len(matrix)
    q = queue.SimpleQueue()
    q.put((the_node, 1 << the_node, 1))     # (node, subset code, length): length odvec, ampak ok ...
    neighbours = sorted(graph[the_node])
    neighbour_to_index = {x: i for i, x in enumerate(neighbours)}
    counts = np.zeros((n + 1, len(neighbours)))  # n x 3
    last_cycle_length = 0
    iterations = 0
    answer = True
    while not q.empty() and iterations < 10**8:
        iterations += 1
        node, subset, length = q.get_nowait()
        if node in neighbours and length > 2:
            if length > last_cycle_length and min(counts[last_cycle_length]) < max(counts[last_cycle_length]):
                # testirano na if False and (pogoj zgoraj)
                answer = False
                break
            i = neighbour_to_index[node]
            counts[length, i] += 1
            last_cycle_length = length
        for neighbour in matrix[node]:
            n_code = 1 << neighbour  # i.e., n_code = 2 ** i
            if n_code & subset:
                continue
            q.put((neighbour, subset | n_code, length + 1))
    return answer, last_cycle_length, counts


def better_test_single(graph: nx.Graph):
    answer, last_cycle_length, counts = is_regular(graph)
    directed_version = graph.to_directed()
    all_cycles = list((length, part) for length, part in simple_cycles_my(directed_version) if length > 2 and part[0] == 0)
    counts_from_johnson = np.zeros((last_cycle_length + 1, 3), dtype=int)
    node_to_index = dict(zip(graph[0], range(3)))
    for length, part in all_cycles:
        if length > last_cycle_length:
            continue
        i = node_to_index[part[1]]
        counts_from_johnson[length, i] += 1
    for i in range(last_cycle_length + 1):
        truth = sorted(counts_from_johnson[i])
        maybe = sorted(counts[i])
        assert len(truth) == len(maybe) == 3, (truth, maybe)
        for x, y in zip(truth, maybe):
            if abs(x - y) > 0.5:
                raise ValueError(f"Length {i}: {truth}, {maybe}")


def better_test():
    graphs = convert_to_nx_simple()
    for graph in graphs:
        better_test_single(graph)


def solve_all():
    graphs = convert_to_nx()
    results_file = "cvt-info-1000-girth-6-7-8-not-mod-3_filtering_level1.csv"
    with open(results_file, "w", encoding="utf-8") as f:
        print("order,cvt_id,is_regular,last_cycle_length")
        for i, ((order, cvt_id), g) in enumerate(graphs):
            LOGGER.info(f"Graph {i}")
            answer, last_cycle_length, _ = is_regular(g, the_node=0)
            print(f"{order},{cvt_id},{answer},{last_cycle_length}", file=f)


if __name__ == '__main__':
    solve_all()
    # better_test()
