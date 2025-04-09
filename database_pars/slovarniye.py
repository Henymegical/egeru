from copy import deepcopy

def sl_pars(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    AllWords = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))
    w=[]
    for i in AllWords:
        counter = -1
        for j in range(len(i)):
            counter += 1
            if i[j] == "(":
                break
            elif i[j] == 'у':
                continue
            elif i[j:] in 'ать,ент' and j >= len(i)-3:
                continue
            elif i[j:] in 'ый,ий,ой,ея,ия,ие' and j >= len(i)-2:
                continue
            elif i[j:] in 'я,о,а,е,и,ы' and j >= len(i)-1:
                continue
            elif i[j] in ['а', 'е', 'я', 'э', 'ё', 'о', 'и', 'ю', 'у', 'ы']:
                wo = i.upper()
                wo = f'{wo[:counter]}...{wo[counter+1:]}'
                w.append((wo, f'{i[:counter]}{i[j].upper()}{i[counter+1:]}', str(i[j])))
    return w

words = sl_pars('databasetxt/sl_pars.txt')

copywords = deepcopy(words)
