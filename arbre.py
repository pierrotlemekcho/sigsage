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
    tree.insert('', tk.END, open=True ,text=nom_groupe, tag='groupe')
    #reset les valeur par défaut
    group_entry.delete(0,"end")
    group_entry.insert(0,"Groupe")

def sup_groupe():
    pass
def select_ligne():

    selection = tree.focus()
    values = tree.item(selection , 'text')
    temp_aff.config(text=selection)
    print(values)

def clicker(e):
    select_ligne()

def up():

    '''
    faire monter un compte dans un groupe de compte
    changer un compte de groupe de compte
    remonter un groupe de compte
    '''
    row = tree.selection()
    row_prev = tree.prev(row)
    parent=tree.parent(row)
    parent_prev=tree.prev(parent)
    
    # incorporer un compte_seul dans le 1er groupe dispo
    if tree.tag_has('compte_seul',item=row) == 1:
        if tree.tag_has('groupe', item =row_prev) == 1:
            nb_row = tree.get_children(row_prev)
            tree.move(row, row_prev ,index=len(nb_row)+1)
            # impossible de prendre le dernier indice bug ttk?
            tree.item(row, tag ='compte')

    # si enhaut de l'arbre redescendre d'un parent
    if parent_prev == "":
        parent_prev = parent
    #passer au parent du dessus si en haut d'un parent
    if tree.index(row) == 0:
        tree.move(row, parent_prev, tree.index(row)-1)
    #remonter d'un indice
    tree.move(row, tree.parent(row), tree.index(row)-1)


def down():
    row = tree.selection()
    tree.move(row, tree.parent(row), tree.index(row)+1)


root = tk.Tk()
root.title(' sigsage ')
#root.geometry('1200x800')

frame = ttk.Frame(root)
frame.pack()
frame1= ttk.Labelframe(frame, text="modifier les groupes")
frame1.grid(row=0, column=0,sticky="en")
widgets_frame0 = ttk.Labelframe(frame1, text=" Créer un nouveau groupe de compte")
widgets_frame0.grid(row=0, column=0)
widgets_frame1 = ttk.Labelframe(frame1, text=" supprimer un groupe vide")
widgets_frame1.grid(row=1, column=0, sticky="ew")
widgets_frame2 = ttk.Labelframe(frame1, text="deplacer les lignes")
widgets_frame2.grid(row=2, column=0, sticky="ew")

group_entry = ttk.Entry(widgets_frame0)
group_entry.grid(row=0, column=0, padx=5, pady=(10,5), sticky="ew")
group_entry.insert(0, "Groupe")
group_entry.bind("<FocusIn>", lambda e: group_entry.delete('0', 'end'))
group_entry.grid(row=0, column=0, sticky="ew")

button = ttk.Button(widgets_frame0, text="Inserer", command=insert_groupe)
button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

button1 = ttk.Button(widgets_frame1, text="suprimer", command=sup_groupe)
button1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

button_select = ttk.Button(widgets_frame2, text="selectionner",
                           command=select_ligne)
button_select.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

button_up = ttk.Button(widgets_frame2 , text="monter", command=up)
button_up.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

button_down = ttk.Button(widgets_frame2 , text="descendre", command=down)
button_down.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")






temp_aff = ttk.Label(frame, text="")
temp_aff.grid(row=1, column=0, padx=10, pady= 20, sticky="sew")


tree_frame = ttk.Frame(frame)
tree_frame.grid(row=0, column=1, pady=10)
treeScroll = ttk.Scrollbar(tree_frame)
treeScroll.pack(side="right", fill="y")
columns = ('groupe' , 'compte')
tree = ttk.Treeview(tree_frame ,columns=columns ,
                    yscrollcommand=treeScroll.set,
                    show='tree headings',
                    height=20 ,
                    selectmode=tk.BROWSE)
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
                           open = True,
                           values = ("Montant groupe",""),
                           tag='groupe'
                          )
        print(item)
        print(value[0])
        for value1 in value[1:]:
            item1=tree.insert(item,
                              tk.END,
                              text=value1,
                              open=True,
                              values = ("","solde compte"),
                              tag='compte'
                             )
            print(item1 + '-----------' + value1)
    else:
        tree.insert('', 'end', text = value,
                    open=True,
                    values = ("","solde compte"),
                   tag='compte_seul'
                   )



tree.tag_configure('groupe', background='lightblue')
tree.tag_configure('compte_seul', background='orange red')

# Bindings
#tree.bind("<Double-1>", clicker)
tree.bind("<ButtonRelease-1>", clicker)



root.mainloop()



