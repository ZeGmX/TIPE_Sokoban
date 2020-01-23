"""
#######################################
#               TIPE                  #
#######################################
"""


"""
#######################################
#           Importations              #
#######################################
"""


from tkinter import *
from os import *
chdir(path.dirname(__file__))
from _Classe_jeu import *
from _Bibliotheque_niveaux import *
from _Resolution import *


"""
#######################################
#         Interface graphique         #
#######################################
"""

def jouer_tkinter(niveau):
    "Interface graphique pour jouer a un niveau"
    def clavier(event):
        "Interaction clavier - interface"
        touche = event.keysym
        old_coord = canvas.coords(player)
        nb_coups = int(canvas.itemcget(texte,'text')[18:])

        if touche in ["Up", "z"]:
            move, i, _, new = jeu.go_h(ret=True)
        elif touche in ["Down", "s"]:
            move, i, _, new = jeu.go_b(ret=True)
        elif touche in ["Right", "d"]:
            move, i, _, new = jeu.go_d(ret=True)
        elif touche in ["Left", "q"]:
            move, i, _, new = jeu.go_g(ret=True)
        else:                                                                                           #Mauvaise touche
            return None

        if move:
            xx, yy = new[0], new[1]
            canvas.coords(Lc[i], 25 * yy, 25 * xx, 25 * (yy + 1), 25 * (xx + 1))                        #Deplacement de la caisse
        x, y = jeu.pj
        canvas.coords(player, 25 * y, 25 * x, 25 * (y + 1), 25 * (x + 1))                               #Deplacement du joueur

        if old_coord != canvas.coords(player):
            nb_coups += 1
            canvas.itemconfigure(texte, text="Nombre de coups : {}".format(nb_coups))                   #Modification du nombre de coups dans le texte

        if victoire(jeu):
            n, p = len(jeu.laby), len(jeu.laby[0])
            canvas.create_text(max(25 * p, 180) / 2, 25 * n / 2, text="Vous avez gagne !\nScore: {} coups".format(nb_coups), fill="red", font=('Helvetica', '16', 'bold italic'))


    jeu = niveau.copy()
    sokoban = Tk()                                                                                      #Fenetre
    n, p = len(jeu.laby), len(jeu.laby[0])
    canvas = Canvas(sokoban, width=max(25 * p, 180), height=25 * n, background="gray")                  #Canvas, murs gris
    for i in range(n) :
        for j in  range(p):
            if jeu.laby[i,j] != 1:
                canvas.create_rectangle(25 * j, 25 * i, 25 * (j + 1), 25 * (i + 1), fill="white", outline="white")  #Espace libre blancs
            if [i,j] in jeu.pv:
                canvas.create_rectangle(25 * j, 25 * i, 25 * (j + 1), 25 * (i + 1), fill="purple")      #Positions de victoires violettes
    Lc = []                                                                                             #Liste des objets caisses
    for [i, j] in jeu.pc:
        Lc.append(canvas.create_rectangle(25 * j, 25 * i, 25 * (j + 1), 25 * (i + 1), fill="brown"))    #Caisses marrons
    i, j = jeu.pj
    player = canvas.create_oval(25 * j, 25 * i, 25 * (j + 1), 25 * (i + 1), fill="blue")                #Joueur bleu
    texte = canvas.create_text(0, 25*(n-1/2), text="Nombre de coups : 0", anchor="w")

    canvas.focus_set()
    canvas.bind("<Key>", clavier)
    canvas.pack()
    sokoban.mainloop()

def show_sol(jeu, sol):
    "Applique la solution sol au jeu"
    def clavier(event):
        "Appuyer sur la fleche montante pour avancer"
        touche = event.keysym
        old_coord = canvas.coords(player)

        if touche == "Up" and sol != []:
            direction = sol.pop()
            move, i, _, new = jeu.avancee(direction, ret=True)
        else:
            return None

        if move:
            xx, yy = new[0], new[1]
            canvas.coords(Lc[i], 25 * yy, 25 * xx, 25 * (yy + 1), 25 * (xx + 1))
        x, y = jeu.pj
        canvas.coords(player, 25 * y, 25 * x, 25 * (y + 1), 25 * (x + 1))

        if victoire(jeu):
            n, p = len(jeu.laby), len(jeu.laby[0])
            canvas.create_text(max(25 * p, 180) / 2, 25 * n / 2, text="Tada !", fill="red",font=('Helvetica', '16', 'bold italic'))

    sol = sol[::-1]
    jeu = jeu.copy()
    sokoban = Tk()                                                                                      #Fenetre
    n, p = len(jeu.laby), len(jeu.laby[0])
    canvas = Canvas(sokoban, width=max(25 * p, 180), height=25 * n, background="gray")                  #Canvas, mur gris
    for i in range(n) :
        for j in  range(p):
            if jeu.laby[i,j] != 1:
                canvas.create_rectangle(25 * j, 25 * i, 25 * (j + 1), 25 * (i + 1), fill="white", outline="white")  #Espace libre blancs
            if [i,j] in jeu.pv:
                canvas.create_rectangle(25 * j, 25 * i, 25 * (j + 1), 25 * (i + 1), fill="purple")      #Positions de victoires violettes
    Lc = []                                                                                             #Liste des objets caisses
    for [i, j] in jeu.pc:
        Lc.append(canvas.create_rectangle(25 * j, 25 * i, 25 * (j + 1), 25 * (i + 1), fill="brown"))    #Caisses marrons
    i, j = jeu.pj
    player = canvas.create_oval(25 * j, 25 * i, 25 * (j + 1), 25 * (i + 1), fill="blue")                #Joueur bleu

    canvas.focus_set()
    canvas.bind("<Key>", clavier)
    canvas.pack()
    sokoban.mainloop()
