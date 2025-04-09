from copy import deepcopy

def na_pars(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    AllWords = list(dict.fromkeys([line.strip().replace('/', '0').replace('_', '1')\
                                    for line in lines if line.strip()]))
    w=[]
    for i in AllWords:
        for j in i:
            if j in '0,1':
                break
              
        wordq = i.replace('0', '...').replace('1', '...')
        worda = i.replace('0', '').replace('1', ' ')
        w.append((wordq.upper(), worda, str(j)))
    return w

words = na_pars('databasetxt/na_pars.txt')

copywords = deepcopy(words)
