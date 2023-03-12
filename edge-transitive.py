#!/usr/bin/env sage -python

from math import pi
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
import sys

import sage.all
from sage.graphs.graph import Graph
from sage.libs.gap.libgap import libgap

def different_edges(graph):
    """Takes a sparse6 string and returns a list of representative edges 
     for the edge orbits such that they are all from the neighborhood of 0."""

    # edge transitivity part
    g = Graph(graph)
    if not g.size():
        return False # if there are no edges
    # predpostavimo, da so povezave vse (i, j), i < j
    nbh_edges = list(sorted(g.edges(labels=False)))[:3]
    A = g.automorphism_group()
    assert(all(e[0] == 0 for e in nbh_edges))
    gap_to_domain = { v: k for k, v in A._domain_to_gap.items() if k in g.neighbors(0, closed = True) }
    orbits = []
    
    for i in range(3):
        # vertices are 1-n in Gap, not 0-(n-1)
        e = nbh_edges[i]
        e = [A._domain_to_gap[e[0]], A._domain_to_gap[e[1]]]
        current_orbit = [e for e in libgap(A).Orbit(e, libgap.OnSets) if A._domain_to_gap[0] in e]
        if i == 0 or all(e not in o for o in orbits):
            orbits.append(current_orbit)

    return [ (gap_to_domain[int(o[0][0])], gap_to_domain[int(o[0][1])]) for o in orbits ]


if __name__ == '__main__':
    with open('first_pass.csv') as fin:
        next(fin)
        with open('data/cvt-info-1000-girth-6-7-8-not-mod-3.csv') as finfo:
            next(finfo)
            with open('orbite.csv', 'w') as fh:
                last_order = 0
                fh.write('order,cvt_id,girth,mod3,zadnja_dolžina,orbite\n')
                for cycles_line in fin:
                    cycle_data = cycles_line.strip().split(',')
                    order = int(cycle_data[0])
                    cvt_id = int(cycle_data[1])
                    kandidat = bool(cycle_data[2]) # True, če do zadnje dolžine vse isto
                    zadnja_dolzina = int(cycle_data[3]) # zadnja dolžina cikla, ki smo jo do konca preiskali
                    if not kandidat: # prekinemo, če ni kandidat
                        continue
                    cvt_line = finfo.readline().strip()
                    while not cvt_line.startswith(cycle_data[0] + ',' + cycle_data[1]):
                        cvt_line = finfo.readline().strip()
                    cvt_data = cvt_line.split(',')
                    girth = int(cvt_data[2])
                    mod3 = int(cvt_data[3])
                    sparse6 = cvt_data[4]
                    orbite = different_edges(sparse6)
                    fh.write(';'.join(map(str, [order, cvt_id, girth, mod3, zadnja_dolzina, orbite])) + '\n')
