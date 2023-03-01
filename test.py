import networkx as nx
import time

# g = nx.from_sparse6_bytes(b':MiGc`pHC[qPD@IgDP?p~') # Heawood graph

with open('cvt-1000-girth-6-7-8-not-mod-3.csv') as fin:
    with open('time.txt', 'w') as fh:
        last_order = 0
        for line in fin:
            split = line.find(',')
            n = int(line[:split])
            if n == last_order: continue
            last_order = n
            g = nx.from_sparse6_bytes(bytes(line[split+1:], 'utf8'))
            t0 = time.time()
            for c in nx.simple_cycles(g.to_directed(as_view=False)):
                if c[0] > 0: break
            report = str(n) + ', ' + str(time.time()-t0) + '\n'
            print(report)
            fh.write(report)


    # select graph.'order', graph_cvt.cvt_index, graph.data
# from
# 	graph inner join graph_cvt 
# 	on graph.zooid = graph_cvt.zooid
# where
# 	graph.'order' <= 1000 and
# 	graph.is_vertex_transitive and
# 	not graph.is_edge_transitive and
# 	graph_cvt.cvt_index is not null and
# 	graph.girth >= 6 and
# 	graph.girth <=8

# TODO: red stabilizatorja vozlišča NI deljiv s 3
# Za 6 domnevam, da jih ni, pri 7 ali 8 pa bi po mojem morali najti kake primere.
# Skratka, program, ki tole pregleda do, recimo, 1.000 vozlišč v enem tednu, 
# prejme nagrado (ne samo simbolično). Če je 1.000 preveč, potem bom zadovoljen do 
#  manj (sam znam narediti do 400). Skratka, čim dlje.
