from copy import deepcopy

def n__pars(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    AllWords = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))
    w=[]
    for i in AllWords:
        flag = False
        for j in i:
            if j == 'Н':
                if flag == False:
                    flag = True
                    continue
                if flag == True:
                    flag == False
                    w.append((i.replace('НН', '...').upper(),i,'НН'))
                    break
            if flag == True:
                flag == False
                w.append((i.replace('Н', '...').upper(),i,'Н'))
                break
            
    return w

words = n__pars('databasetxt/n__pars.txt')

copywords = deepcopy(words)
    