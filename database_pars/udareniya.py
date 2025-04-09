from copy import deepcopy

def ud_pars(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    AllWords = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))
    w=[]
    for i in AllWords:
        counter = 0
        for j in i:
            counter += 1
            if j.istitle():
                break
        k = i.replace('Ё', 'Е')
        w.append((k.upper(), i, str(counter)))
    return w

words = ud_pars('databasetxt/ud_pars.txt')

copywords = deepcopy(words)
