
with open('data/Census3valentVTproperties.csv') as fin:
    with open('data/mod3.csv', 'w') as fout:
        next(fin) # preskoči glavo
        for l in fin:
            info = l.split(',')
            mod = int(info[-1]) % 3
            if mod != 0:
                fout.write(','.join(info[:-1] + [str(mod) + '\n']))
            
