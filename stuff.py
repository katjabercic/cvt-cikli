import networkx as nx
import logging


def convert_to_nx(file: str = "cvt-100.csv", to_directed=False):
    gs = []
    with open(file, encoding="utf-8") as f:
        for line in f:
            i = line.find(',')  # maybe more than ','
            n_nodes = int(line[:i])
            sprase6 = line[i + 1:].strip()
            graph: nx.Graph = nx.from_sparse6_bytes(bytes(sprase6, 'utf8'))
            if n_nodes != graph.order():
                raise ValueError(f"{sprase6}: {n_nodes} != {graph.order()}")
            elif list(range(n_nodes)) != sorted(graph.nodes):
                raise ValueError(f"Nodes are not labelled as integers 0, 1, ..., order - 1")
            gs.append(graph)
        return gs


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
