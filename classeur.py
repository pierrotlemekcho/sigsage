from pathlib import Path
import pickle 
from openpyxl import Workbook

HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"

wb = Workbook()
ws = wb.active


with open(DATA_FOLDER / "tableau.pkl", "rb") as tf:
    dic_compte = pickle.load(tf)

lcompte = list(dic_compte.keys())
print(lcompte)


lg1=['Achat Matière', lcompte[1],lcompte[2],lcompte[3]]
lg2=['dummy_group' , lcompte[7],lcompte[10],lcompte[10],lcompte[20]]

lgroupes=[lg1,lg2]
print(lgroupes)

#p#rint('########################')
#print(lg1)
#dg1 = {
#    "titre": lg1[0],
#    lg1[1] : dic_compte.get(lg1[1]),
#    lg1[2] : dic_compte.get(lg1[2]),
#    lg1[3] : dic_compte.get(lg1[3]),
#}
# boucle sur la liste de groupes lgroupes (ii indice ligne , jj indice colonne
# d'excel)
ii=1
for lgroup in lgroupes:
    dgroup = {}
    dgroup = {"titre" : lgroup[0] }
    for i in range(1,len(lgroup)):
        dgroup[lgroup[i]] = dic_compte.get(lgroup[i])

        #print('########################')
        #print(dg1)
        #print('########################')
        #print(dic_compte.get(lg1[1]).items())
        #print(dic_compte.get(lg1[1]).keys())
        #print(dic_compte.get(lg1[1]).values())
        #print('########################')
        #print('########################')
        #print(dic_compte.get(lg1[1]).get("mois4"))


    stotal = {}
    for i in range(1,len(lgroup)):
        if i == 1 :
            for key, value in dic_compte.get(lgroup[i]).items():
                stotal[key] =  value
                print(value)
    #            print('########################')
    #            print(stotal)
    #            print('########################')
        else :
            for key, value in dic_compte.get(lgroup[i]).items():
                stotal[key] = stotal[key] + value
    #            print('########################')
    #            print(stotal)
    #            print('########################')
    print('~~~~~~~~~~~~~~~~~~')
    print(i)
    print('~~~~~~~~~~~~~~~~~~')

    print('#####ws###################')
    print(stotal)
    print('########################')

    dgroup[str("Sous-total"+lgroup[0])] = stotal

    print(dgroup)

    #ii=1
    jj=1

    #ws.cell(row=ii, column=jj, value = lg1[0])

    for key, value in dgroup.items():
        if isinstance(value, str):
            ws.cell(row=ii, column=jj, value =value)
            print(key,value)
        else:
            ii+=1
            jj=1
            ws.cell(row=ii, column=jj, value = key)

            for key1, value1 in value.items():
                jj+=1
                print(key1 ,value1)
                ws.cell(row=ii, column=jj, value =value1)

            print( value)
            print(type(value))
    ii+=2
    




#ws['A1'] = lg1[0]
wb.save('document.xlsx')

