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
def insert_groupe():
    nom_groupe = group_entry.get()
    print(nom_groupe)
    #le nom de groupe ne doit pas exister
    #
    tree.insert('', tk.END, text=nom_groupe) 







root = tk.Tk()
root.title(' sigsage ')
#root.geometry('1200x800')

frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.Labelframe(frame, text=" Insere un groupe de compte")
widgets_frame.grid(row=0, column=0)

group_entry = ttk.Entry(widgets_frame)
group_entry.grid(row=0, column=0, padx=5, pady=(10,5), sticky="ew")
group_entry.insert(0, "Groupe")
group_entry.bind("<FocusIn>", lambda e: group_entry.delete('0', 'end'))
group_entry.grid(row=0, column=0, sticky="ew")

button = ttk.Button(widgets_frame, text="Inserer", command=insert_groupe)
button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")






tree_frame = ttk.Frame(frame)
tree_frame.grid(row=0, column=1, pady=10)
treeScroll = ttk.Scrollbar(tree_frame)
treeScroll.pack(side="right", fill="y")
columns = ('groupe' , 'compte')
tree = ttk.Treeview(tree_frame ,columns=columns ,
                    yscrollcommand=treeScroll.set,show='tree headings', height=20)
treeScroll.config(command=tree.yview)
tree.heading("#0",  text= 'root')
tree.heading('groupe',  text= 'solde groupe')
tree.heading('compte',  text= 'solde compte')
tree.column("#0", width=400)
tree.column("groupe", width=150)
tree.column("compte", width=150)

tree.pack()




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





#root.columnconfigure(0, weight=1)
#root.columnconfigure(1, weight=1)
#tree.grid(row=1, column=0,sticky='nsew' ) 
#scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
#tree.configure(yscroll=scrollbar.set)
#scrollbar.grid(row=1, column=0, sticky='nse')

root.mainloop()


