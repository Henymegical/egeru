from random import choice
import ast
from copy import deepcopy

def fo_pars(file_path):
    w = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    try:
        AllWords = list(dict.fromkeys([ast.literal_eval(line.strip()) for line in lines if line.strip()]))
    except:
        AllWords = list(dict.fromkeys([tuple(line.strip().split('#')) for line in lines if line.strip()]))
    for i in AllWords:
        i=(i[0].upper(), i[1].upper())
        c=choice([0,1])
        ch = i[c]
        if ch == i[0]:
            w.append((ch, i[0].lower(), str(ch == i[0]), i[c-1]))
        else:
            w.append((ch, i[0].lower(), str(ch == i[0]), 'False'))
    return w

words = fo_pars('databasetxt/fo_pars.txt')
copywords = deepcopy(words)

