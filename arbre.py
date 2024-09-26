import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import pickle 
HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"


l_lgroupes = []
tttgroupe=[]


with open(DATA_FOLDER / "tableau.pkl", "rb") as tf:
    dic_compte = pickle.load(tf)

lcompte = list(dic_compte.keys())
print(lcompte)





def insert_groupe():
    nom_groupe = group_entry.get()
    print(nom_groupe)
    #le nom de groupe ne doit pas exister
    #
    tree.insert('', tk.END, open=True ,text=nom_groupe,
                values = ("","solde compte"),
                tag='groupe')
    #reset les valeur par défaut
    group_entry.delete(0,"end")
    group_entry.insert(0,"Groupe")

def sup_groupe():
    ''' 
    suprimmer un groupe,gardesr les compte , les passer ses comptes en compte-seul
    '''
    row = tree.selection()
    if tree.tag_has('groupe', item =row) == 1:
        children = tree.get_children(row)
        for child in children :
            tree.move(child,'',index="end")
            tree.item(child, tag ='compte_seul')
        tree.delete(row)


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
    parent = tree.parent(row)
    parent_prev = tree.prev(parent)
    
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
        nb_row = tree.get_children(parent_prev)
        tree.move(row, parent_prev,index= len(nb_row)+1)
    #remonter d'un indice
    tree.move(row, tree.parent(row), tree.index(row)-1)


def down():
    rowd = tree.selection()
    rowd_next = tree.next(rowd)
    parentd = tree.parent(rowd)
    parentd_next = tree.next(parentd)
    print(f" indice de la ligne selectionné {rowd}")
    print(f" indice de la ligne selectionné {tree.index(rowd)}")
    print(f" indice de la ligne selectionné {rowd}")
    print(f" indice ligne suivante {rowd_next}")
    print(f" indice parent {parentd}")
    print(f" parent suivant {parentd_next}")

    tree.move(rowd, parentd, tree.index(rowd)+1)
    #un compte passe au groupe du desous si c'est bien un groupe
    if tree.tag_has('compte', item =rowd) == 1 :
        print(" c'est un compte")
        if rowd_next == "" and tree.tag_has('groupe', item =parentd_next) == 1 :
            tree.move(rowd, parentd_next, index= 0)
            print("uuuuuuu")
    #un groupe ne passe pas sous un compte _seul
    if tree.tag_has('groupe', item =rowd) == 1 :
        if tree.tag_has('groupe', item =rowd_next) == 1 :
            tree.move(rowd, rowd_next, tree.index(rowd)+1)

def charger_file():
    select_file = filedialog.askopenfilename(parent=root,
                                             filetypes=[("Fichier SIG",".pkl")],
                                             initialdir=DATA_FOLDER)
    print(select_file)
    with open(select_file, "rb") as tf:
        lgroupes = pickle.load(tf)
    print(lgroupes)
    print("--------")
    remplir_tree(lgroupes)


def sauver_file():
    select_file = filedialog.asksaveasfilename(parent=root,
                                             filetypes=[("Fichier SIG",".pkl")],
                                             initialdir=DATA_FOLDER)
    print(select_file)
    xxx,yyy = get_all_children(tree)
    lgroupes=faire_groupe(yyy)
    with open(select_file, "wb") as tf1:
        pickle.dump(lgroupes,tf1)
    


def get_all_children(tree, item=""):
    '''
    extraire la liste de tout les enfants dans l'ordre
    le l'arbre
    -renvoi "children" la liste de tous les item de l'arbre non classé
    -renvoi "tttgroupe" la liste classé dans l'orde de l'arbre des valeurs "text"
    de chaque item
    '''
    children = tree.get_children(item)
    for child in children:
        children += get_all_children(tree, child)
        print(tree.item(child)["text"])
        tttgroupe.append(child)
    return children , tttgroupe

def faire_groupe(enfants):
    '''
    enfants est la liste des items de l'arbre tree
    génère la liste de groupe avec leur compte pour pouvoire etre traité
    par classeur.py 
    '''
    tgroupe = []
    ttgroupe = [] 
    for enfant in enfants :
       if tree.tag_has('compte', item =enfant) == 1 :
           tgroupe.insert(len(tgroupe),tree.item(enfant)["text"])
       if tree.tag_has('groupe', item =enfant) == 1 :
           tgroupe.insert(0,tree.item(enfant)["text"])
           ttgroupe.append(tgroupe)
           tgroupe = []
       if tree.tag_has('compte_seul', item =enfant) == 1 :
           ttgroupe.insert(len(ttgroupe),tree.item(enfant)["text"])
    return ttgroupe

def remplir_tree(lgroupes):
    '''
    populer l'arbre à partir d'une liste 
    '''
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
        

root = tk.Tk()
root.title(' sigsage ')
#root.geometry('1200x800')

frame = ttk.Frame(root)
frame.pack()
#-------------------------frame1
frame1= ttk.Labelframe(frame, text="modifier les groupes")
frame1.grid(row=1, column=0,sticky="en")

widgets_frame10 = ttk.Labelframe(frame1, text=" Créer un nouveau groupe de compte")
widgets_frame10.grid(row=0, column=0)

group_entry = ttk.Entry(widgets_frame10)
group_entry.grid(row=0, column=0, padx=5, pady=(10,5), sticky="ew")
group_entry.insert(0, "Groupe")
group_entry.bind("<FocusIn>", lambda e: group_entry.delete('0', 'end'))
group_entry.grid(row=0, column=0, sticky="ew")

button = ttk.Button(widgets_frame10, text="Inserer", command=insert_groupe)
button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")


widgets_frame11 = ttk.Labelframe(frame1, text=" supprimer un groupe vide")
widgets_frame11.grid(row=1, column=0, sticky="ew")
button1 = ttk.Button(widgets_frame11, text="suprimer", command=sup_groupe)
button1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")


widgets_frame12 = ttk.Labelframe(frame1, text="deplacer les lignes")
widgets_frame12.grid(row=2, column=0, sticky="ew")
button_select = ttk.Button(widgets_frame12, text="selectionner",
                           command=select_ligne)
button_select.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
button_up = ttk.Button(widgets_frame12 , text="monter", command=up)
button_up.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
button_down = ttk.Button(widgets_frame12 , text="descendre", command=down)
button_down.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
#-------------------------frame2
frame2= ttk.Labelframe(frame, text="utiliser des  fichiers SIG ")
frame2.grid(row=0, column=0,sticky="we")
widgets_frame20 = ttk.Labelframe(frame2,
                                 text=" Charger un fichier existant les comptes seront MAJ")
widgets_frame20.grid(row=0, column=0,sticky="w" )
button_imp = ttk.Button(widgets_frame20,
                        text="Charger",
                        command=charger_file)
button_imp.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

widgets_frame21 = ttk.Labelframe(frame2, text=" sauver un fichier de solde")
widgets_frame21.grid(row=1, column=0, sticky="nsew")
button_imp = ttk.Button(widgets_frame21, text="sauver", command=sauver_file)
button_imp.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")




temp_aff = ttk.Label(frame, text="")
temp_aff.grid(row=1, column=0, padx=10, pady= 20, sticky="sew")


tree_frame = ttk.Frame(frame)
tree_frame.grid(row=0, column=1, pady=10,rowspan=2)
treeScroll = ttk.Scrollbar(tree_frame)
treeScroll.pack(side="right", fill="y")
columns = ('groupe' , 'compte')
tree = ttk.Treeview(tree_frame ,columns=columns ,
                    yscrollcommand=treeScroll.set,
                    show='tree headings',
                    height=40 ,
                    selectmode=tk.BROWSE)
treeScroll.config(command=tree.yview)
tree.heading("#0",  text= 'root')
tree.heading('groupe',  text= 'solde groupe')
tree.heading('compte',  text= 'solde compte')
tree.column("#0", width=400)
#remplir l'arbre
lgroupes = l_lgroupes
tree.pack(expand=True,fill="y")






tree.tag_configure('groupe', background='lightblue')
tree.tag_configure('compte_seul', background='orange red')

tree.bind("<ButtonRelease-1>", clicker)



print("""""""""""""""""""""""""""""")
print("ààààààààààààààààà")
root.mainloop()
