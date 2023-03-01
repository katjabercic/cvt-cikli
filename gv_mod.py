
with open('props.csv') as fin:
    with open('mod3.csv', 'w') as fout:
        for l in fin:
            info = l.split(',')
            mod = int(info[-1]) % 3
            if mod != 0:
                fout.write(','.join(info[:-1] + [str(mod) + '\n']))
            
