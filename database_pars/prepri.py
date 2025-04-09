from copy import deepcopy

def pr_pars(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    AllWords = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))
    w=[]
    for i in AllWords:
        if 'пре' in i:
            w.append((i.replace('пре', 'пр...').upper(), i.replace('пре', 'прЕ'), 'е'))
        elif 'при' in i:
            w.append((i.replace('при', 'пр...').upper(), i.replace('при', 'прИ'), 'и'))

    return w

words = pr_pars('databasetxt/pr_pars.txt')

copywords = deepcopy(words)