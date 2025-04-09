from copy import deepcopy

def is_pars(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    AllWords = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))
    w=[]
    for i in AllWords:
        for j in range(len(i)):
            if i[j].isupper():
                wo = i.upper()
                wo = f'{wo[:j]}...{wo[j+1:]}'
                w.append((wo, i, str(i[j])))
    return w

words = is_pars('databasetxt/is_pars.txt')
copywords = deepcopy(words)
