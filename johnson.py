from collections import defaultdict
import networkx as nx

# Copied from nx, adjusted as remarked in the comments


def simple_cycles_my(G):
    """Find simple cycles (elementary circuits) of a directed graph.

    A `simple cycle`, or `elementary circuit`, is a closed path where
    no node appears twice. Two elementary circuits are distinct if they
    are not cyclic permutations of each other.

    This is a nonrecursive, iterator/generator version of Johnson's
    algorithm [1]_.  There may be better algorithms for some cases [2]_ [3]_.

    Parameters
    ----------
    G : NetworkX DiGraph
       A directed graph

    Yields
    ------
    list of nodes
       Each cycle is represented by a list of nodes along the cycle.

    Examples
    --------
    >>> edges = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)]
    >>> G = nx.DiGraph(edges)
    >>> sorted(nx.simple_cycles(G))
    [[0], [0, 1, 2], [0, 2], [1, 2], [2]]

    To filter the cycles so that they don't include certain nodes or edges,
    copy your graph and eliminate those nodes or edges before calling.
    For example, to exclude self-loops from the above example:

    >>> H = G.copy()
    >>> H.remove_edges_from(nx.selfloop_edges(G))
    >>> sorted(nx.simple_cycles(H))
    [[0, 1, 2], [0, 2], [1, 2]]

    Notes
    -----
    The implementation follows pp. 79-80 in [1]_.

    The time complexity is $O((n+e)(c+1))$ for $n$ nodes, $e$ edges and $c$
    elementary circuits.

    References
    ----------
    .. [1] Finding all the elementary circuits of a directed graph.
       D. B. Johnson, SIAM Journal on Computing 4, no. 1, 77-84, 1975.
       https://doi.org/10.1137/0204007
    .. [2] Enumerating the cycles of a digraph: a new preprocessing strategy.
       G. Loizou and P. Thanish, Information Sciences, v. 27, 163-182, 1982.
    .. [3] A search strategy for the elementary cycles of a directed graph.
       J.L. Szwarcfiter and P.E. Lauer, BIT NUMERICAL MATHEMATICS,
       v. 16, no. 2, 192-204, 1976.

    See Also
    --------
    cycle_basis
    """

    def _unblock(thisnode, blocked, B):
        stack = {thisnode}
        while stack:
            node = stack.pop()
            if node in blocked:
                blocked.remove(node)
                stack.update(B[node])
                B[node].clear()

    # Johnson's algorithm requires some ordering of the nodes.
    # We assign the arbitrary ordering given by the strongly connected comps
    # There is no need to track the ordering as each node removed as processed.
    # Also we save the actual graph so we can mutate it. We only take the
    # edges because we do not want to copy edge and node attributes here.
    subG = type(G)(G.edges())
    sccs = [scc for scc in nx.strongly_connected_components(subG) if len(scc) > 1]

    # Johnson's algorithm exclude self cycle edges like (v, v)
    # To be backward compatible, we record those cycles in advance
    # and then remove from subG
    for v in subG:
        if subG.has_edge(v, v):
            yield [v]
            subG.remove_edge(v, v)

    while sccs:
        scc = sccs.pop()
        sccG = subG.subgraph(scc)
        # order of scc determines ordering of nodes
        startnode = scc.pop()
        # Processing node runs "circuit" routine from recursive version
        path = [startnode]
        blocked = set()  # vertex: blocked from search?
        closed = set()  # nodes involved in a cycle
        blocked.add(startnode)
        B = defaultdict(set)  # graph portions that yield no elementary circuit
        stack = [(startnode, sorted(sccG[startnode]))]  # sccG gives comp nbrs   # matejp: list --> sorted
        while stack:
            thisnode, nbrs = stack[-1]
            if nbrs:
                nextnode = nbrs.pop()
                if nextnode == startnode:
                    yield len(path), path[:2]  # matejp: path[:] --> ...
                    closed.update(path)
                #                        print "Found a cycle", path, closed
                elif nextnode not in blocked:
                    path.append(nextnode)
                    stack.append((nextnode, sorted(sccG[nextnode])))  # list --> sorted
                    closed.discard(nextnode)
                    blocked.add(nextnode)
                    continue
            # done with nextnode... look for more neighbors
            if not nbrs:  # no more nbrs
                if thisnode in closed:
                    _unblock(thisnode, blocked, B)
                else:
                    for nbr in sccG[thisnode]:
                        if thisnode not in B[nbr]:
                            B[nbr].add(thisnode)
                stack.pop()
                #                assert path[-1] == thisnode
                path.pop()
        # done processing this node
        H = subG.subgraph(scc)  # make smaller to avoid work in SCC routine
        sccs.extend(scc for scc in nx.strongly_connected_components(H) if len(scc) > 1)
