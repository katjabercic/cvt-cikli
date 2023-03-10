#!/usr/bin/env sage -python

from math import pi
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
import sys

import sage.all
from sage.graphs.graph import Graph
from sage.libs.gap.libgap import libgap

g = Graph(':I`ES@obGkqegW~')

def different_edges(g):
    """Returns a list of representative edges for the edge orbits such that they are
     all from the neighborhood of 0."""

    # edge transitivity part
    if not g.size():
        return False # if there are no edges
    # predpostavimo, da so povezave vse (i, j), i < j
    nbh_edges = list(sorted(g.edges(labels=False)))[:3]
    A = g.automorphism_group()
    assert(all(e[0] == 0 for e in nbh_edges))
    gap_to_domain = { v: k for k, v in A._domain_to_gap.items() if k in g.neighbors(0, closed = True) }
    orbits = {}
    
    for i in range(3):
        # vertices are 1-n in Gap, not 0-(n-1)
        e = nbh_edges[i]
        e = [A._domain_to_gap[e[0]], A._domain_to_gap[e[1]]]
        current_orbit = [e for e in libgap(A).Orbit(e, libgap.OnSets) if A._domain_to_gap[0] in e]
        if i == 0 or all(e not in orbits[j] for j in range(i)):
            # keys are the indices of edges from nbh_edges
            orbits[i] = current_orbit
    return [ (gap_to_domain[int(o[0][0])], gap_to_domain[int(o[0][1])]) for o in orbits.values() ]
