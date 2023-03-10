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

