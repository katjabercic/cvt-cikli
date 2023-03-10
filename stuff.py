import networkx as nx
import logging
import tqdm


def create_logger(name):
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(filename)s:%(funcName)s:%(lineno)d]:  %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


LOGGER = create_logger(__file__)


def check_graph(order, sparse6, graph):
    if order != graph.order():
        raise ValueError(f"{sparse6}: {order} != {graph.order()}")
    elif list(range(order)) != sorted(graph.nodes):
        raise ValueError(f"Nodes are not labelled as integers 0, 1, ..., order - 1")


def convert_to_nx_simple(file: str = "cvt-100.csv", to_directed=False):
    gs = []
    with open(file, encoding="utf-8") as f:
        f.readline()
        for line in f:
            i = line.find(',')  # maybe more than ','
            n_nodes = int(line[:i])
            sparse6 = line[i + 1:].strip()
            graph: nx.Graph = nx.from_sparse6_bytes(bytes(sparse6, 'utf8'))
            check_graph(n_nodes, sparse6, graph)
            gs.append(graph)
        return gs


def convert_to_nx(file: str = "cvt-info-1000-girth-6-7-8-not-mod-3.csv"):
    gs = []
    with open(file, encoding="utf-8") as f:
        LOGGER.info(f"Loading {file} with header {f.readline().strip()}")
        for line in tqdm.tqdm(f):
            order, id_part, _, _, sparse6 = line.strip().split(",")
            graph: nx.Graph = nx.from_sparse6_bytes(bytes(sparse6, 'utf8'))
            check_graph(int(order), sparse6, graph)
            gs.append(((order, id_part), graph))
        return gs
