import networkx as nx
import queue
import numpy as np

from stuff import convert_to_nx, create_logger
from prvi_poskus import find_spurious_edge


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


def is_regular(graph: nx.Graph, is_test: bool = False):
    matrix = nx_to_matrix(graph, is_test)
    n = len(matrix)
    q = queue.SimpleQueue()
    q.put((0, 1, 1))     # (node, subset code, length): length odvec, ampak ok ...
    neighbours = sorted(graph[0])
    neighbour_to_index = {x: i for i, x in enumerate(neighbours)}
    counts = np.zeros((n + 1, len(neighbours)))  # n x 3
    last_cycle_length = 0
    iterations = 0
    answer = True
    max_q_size = 1
    while not q.empty():
        q_s = q.qsize()
        if q_s > max_q_size:
            LOGGER.debug(f"   Max q_size: {q_s}")
            max_q_size *= 2
        iterations += 1
        node, subset, length = q.get_nowait()
        # print("Processing", node, decode(subset))
        if node in neighbours and length > 2:
            if length > last_cycle_length and min(counts[last_cycle_length]) < max(counts[last_cycle_length]):
                answer = False
                break
            i = neighbour_to_index[node]
            counts[length, i] += 1
            last_cycle_length = length
            # print("    Found cycle: ", decode(subset))
        for neighbour in matrix[node]:
            n_code = 1 << neighbour  # neighbour code: 2 ** i
            if n_code & subset:
                continue
            # print("    Adding ", neighbour)
            q.put((neighbour, subset | n_code, length + 1))
        if iterations % 10 ** 6 == 0:
            LOGGER.info(f"        iterations: {iterations}, length: {length}")
        if iterations > 10**8:
            LOGGER.info("BREAKING AFTER MANY ...")
            break
    LOGGER.info(f"   After {iterations} iterations: {answer} (last length: {last_cycle_length})")
    return answer


def simple_test():
    """
                  5     ------------
               /     \\            |
              0  ...  1            |
              .       .            |
              .   /   .            |
              2  ...  3            |
               \\    /             |
                  4 ---------------|


    :return:
    """
    g = nx.Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 5)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 5)
    g.add_edge(2, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 4)
    g.add_edge(4, 5)

    assert not is_regular(g, True)
    g = nx.icosahedral_graph()
    assert is_regular(g, True)


def solve_all():
    graphs = convert_to_nx("cvt-nekaj_velikih.csv")  # "cvt-100.csv"
    for i, g in enumerate(graphs):
        LOGGER.info(f"Graph {i}")
        # LOGGER.info(f"Spurious edge: {find_spurious_edge(g)}")
        is_regular(g)


if __name__ == '__main__':
    # simple_test()
    solve_all()
