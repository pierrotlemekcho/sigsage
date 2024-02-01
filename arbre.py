import tkinter as tk
from tkinter import ttk
from pathlib import Path
import pickle 
HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"



with open(DATA_FOLDER / "tableau.pkl", "rb") as tf:
    dic_compte = pickle.load(tf)

lcompte = list(dic_compte.keys())
print(lcompte)




with open(DATA_FOLDER / "groupes.pkl", "rb") as tf:
    lgroupes = pickle.load(tf)
print(lgroupes)
"""
def montre_selection():
    try:
        # 1er id de la selection
        item =tree.selection()[0]
    execpt IndexError:
        messagebox.showwarning(
            message="Selectionnez un élément"

"""








window =tk.Tk()
window.title(' sigsage ')
window.geometry('1800x1800')
columns = ('groupe' , 'compte')
tree = ttk.Treeview(window ,columns=columns , show='tree headings', height=20)
tree.heading("#0",  text= 'root')
tree.heading('groupe',  text= 'solde groupe')
tree.heading('compte',  text= 'solde compte')






for value in lgroupes:
    if isinstance (value, list):
        item = tree.insert("",
                           tk.END,
                           text= value[0],
                           values = ("Montant groupe","")
                          )
        print(item)
        print(value[0])
        for value1 in value[1:]:
            item1=tree.insert(item,
                              tk.END,
                              text=value1,
                              values = ("","solde compte")
                             )
            print(item1 + '-----------' + value1)
    else:
        tree.insert('', 'end', text = value, values = ("","solde compte"))





window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
tree.grid(row=1, column=0,sticky='nsew' ) 

scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=1, column=0, sticky='nse')

window.mainloop()


