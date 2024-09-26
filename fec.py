from pathlib import Path
import pandas as pd
from openpyxl import Workbook
import pickle 



HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"


fec = pd.read_table(
    DATA_FOLDER / "2024_EXPORTFEC_20240101_20241231_1.txt",
    usecols = [ "EcritureDate","CompteNum","CompteLib","Debit","Credit"])


fec['EcritureDate']=fec['EcritureDate'].astype('string')
fec['EcritureDate']=pd.to_datetime(fec['EcritureDate'])
fec['Debit']=fec['Debit'].astype('string')
fec['CompteNum']=fec['CompteNum'].astype('string')
fec['CompteLib']=fec['CompteLib'].astype('string')
fec['Credit']=fec['Credit'].astype('string')
fec['Debit']=fec['Debit'].str.replace(',', '.').astype(float)
fec['Credit']=fec['Credit'].str.replace(',', '.').astype(float)


fec['compte'] = fec['CompteNum']+"-->"+fec['CompteLib']
fectrie= fec[fec.compte.str.startswith(('6','7'))]
fectrie['solde'] = fectrie['Debit'] - fectrie['Credit']
fectrie = fectrie.drop(['CompteNum','CompteLib','Debit','Credit'],axis=1)

compte_date = fectrie.groupby(fectrie.EcritureDate.dt.month)['solde'].sum()
fectriegr = fectrie.groupby(fectrie.EcritureDate.dt.month) #['solde']
compte_date


for nom, group in fectriegr:
    indice= str(nom)
    mois = f"mois{indice}"
    groupnet= group.drop(['EcritureDate'],axis=1)
    groupsum=groupnet.groupby(['compte'], as_index=False).sum()
    groupsum=groupsum.rename(columns={'solde': str(mois)})

    if indice  == "1" :
        tableau = groupsum


    else:
        tableau = pd.merge(tableau,groupsum, on= 'compte',how='outer') 
tableau.fillna(0, inplace=True)




solde_compte = fectrie[["compte","solde"]].groupby("compte").sum()


with pd.ExcelWriter(DATA_FOLDER / "pd7_to_ods_1.xlsx", engine="openpyxl") as writer:
    tableau.to_excel(writer)



tableau1 = tableau.set_index('compte')
dic_compte = tableau1.to_dict('index')
sorted_dic_compte = dict(sorted(dic_compte.items()))




with open(DATA_FOLDER / "tableau.pkl", "wb") as tf:
    pickle.dump(sorted_dic_compte , tf)


