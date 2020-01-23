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


from os import *
chdir(path.dirname(__file__))
import numpy as np
import time
from _Interface_graphique import *
from _Classe_jeu import *
from _Bibliotheque_niveaux import *



"""
#######################################
#          Implementation             #
#######################################
"""




def victoire(jeu):
    "Renvoie True si le jeu est gagne, False sinon"
    for i in jeu.pc:
        if not i in jeu.pv:                                                   #Teste si chaque position de victoire est occupee
            return False
    return True

def jouer(jeu) :
    "Permet de jouer a un niveau"
    cop = jeu.copy()
    #cop = jeu
    L = []
    D = {"z" : "Haut", "s" : "Bas", "q" : "Gauche", "d" : "Droite"}
    while 1:
        if victoire(cop) :
            print("Probleme resolu !")
            print("Resolu en {} coups".format(len(L)))
            return L
        else :
            print(cop.laby)
            direction = input("Entrez la direction : ")
            if direction in D.keys():
                cop.avancee(D[direction])
                L.append(D[direction])
            elif direction == "Quit" :
                print("Abandon")
                break
        print('Deplacements : {}'.format(len(L)))

def complementaire(direc):
    "Renvoie la direction opposee a direc"
    D = {"Haut" : "Bas", "Bas" : "Haut", "Droite" : "Gauche", "Gauche" : "Droite"}
    return D[direc]

def solveur_general(jeu, fonction_aux, pre_aux, nb_coups_restants, args={}):
    "Solveur general sur lequel sont utilises les differents modes de resolution"
    if args["affichage"]:
        print(args["coup"], " ", nb_coups_restants)
        print(jeu)

    if victoire(jeu):
        return True

    elif nb_coups_restants == 0:
        return False

    else:
        if pre_aux(jeu, args, nb_coups_restants) == False:                                                          #Actions preliminaires, renvoyant eventuellement False si la partie est perdue
            return False
        nb_coups_restants -= 1

        for d in ["Haut", "Bas", "Droite", "Gauche"]:                                                               #On teste chaque direction dans cet ordre
            if jeu.avancee_bool(d):                                                                                 #On verifie qu'on puisse avancer
                args["coup"] = d
                if fonction_aux(jeu, nb_coups_restants, args):                                                      #Fonction auxiliaire d'exploration
                    args["sol"].append(d)
                    return True

        return False

def aux_solveur_naif(jeu, nb_coups_restant, args):
    "Fonction auxiliaire pour le solveur naif"
    coup, pos_caisses, affichage = args["coup"], args["pos_caisses"], args["affichage"]
    pos_caisses = [[args["pos_caisses"][i][0], args["pos_caisses"][i][1]] for i in range(len(jeu.pc))]
    jeu.avancee(coup)
    res = solveur_general(jeu, aux_solveur_naif, pre_verif_naif, nb_coups_restant, args)
    jeu.avancee(complementaire(coup))
    reset_caisses(jeu, pos_caisses)
    args["pos_caisses"] = [[jeu.pc[i][0], jeu.pc[i][1]] for i in range(len(jeu.pc))]
    if affichage:
        print(coup)
        print(jeu.pc)
    return res

def pre_verif_naif(jeu, args, nb_coups_restant):
    "Actions preliminaires pour le solveur naif"
    args["pos_caisses"] = [[jeu.pc[i][0], jeu.pc[i][1]] for i in range(len(jeu.pc))]                            #Copie de la position des caisses pour le reset

def solveur_naif(jeu, nb_coups_restants, affichage=False):
    "Solveur naif v1"
    args = {"affichage" : affichage, "sol" : [], "coup" : "Haut"}
    solveur_general(jeu, aux_solveur_naif, pre_verif_naif, nb_coups_restants, args)
    args["sol"].reverse()
    return args["sol"]

def reset_caisses(jeu, pos_caisses):
    "Retablie les positions des caisses du jeu aux positions pos_caisses"
    set_caisses = set((pos_caisses[i][0], pos_caisses[i][1]) for i in range(len(pos_caisses)))                  #Transformation en ensemble pour utiliser l'intersection
    newcaisses = set((jeu.pc[i][0], jeu.pc[i][1]) for i in range(len(jeu.pc)))
    caisses_a_enlever = newcaisses - set_caisses
    caisses_a_rajouter = set_caisses - newcaisses
    for pos in caisses_a_enlever:
        jeu.laby[pos] = 0
    for pos in caisses_a_rajouter:
        jeu.laby[pos] = 2
    jeu.pc = [[pos_caisses[i][0], pos_caisses[i][1]] for i in range(len(pos_caisses))]

"""-------------------------------------------------------------------------"""

def aux_solveur_un_tout_petit_peu_moins_naif(jeu, nb_coups_restants, args):
    "Fonction auxiliaire pour le solveur un tout petit peu moins naif"
    coup, affichage = args["coup"], args["affichage"]
    boole, i, old, new = jeu.avancee(coup, True, True)
    res = solveur_general(jeu, aux_solveur_un_tout_petit_peu_moins_naif, pre_verif_un_tout_petit_peu_moins_naif, nb_coups_restants, args)
    jeu.avancee(complementaire(coup), check = True)
    reset_caisses2(jeu, boole, i, old, new)
    if affichage:
        print(coup)
        print(jeu.pc)
    return res

def pre_verif_un_tout_petit_peu_moins_naif(jeu, args, nb_coups_restant):
    "Actions preliminaires pour le solveur un tout petit peu moins naif"
    pass                                                                                                        #Pas d'actions preliminaires pour ce solveur


def solveur_un_tout_petit_peu_moins_naif(jeu, nb_coups_restants, affichage=False):
    "Solveur naif v2"
    args = {"affichage" : affichage, "sol" : [], "coup" : "Haut"}
    solveur_general(jeu, aux_solveur_un_tout_petit_peu_moins_naif, pre_verif_un_tout_petit_peu_moins_naif, nb_coups_restants, args)
    args["sol"].reverse()
    return args["sol"]

def reset_caisses2(jeu, boole, i, old, new):
    "Retablie les positions des caisses du jeu"
    if boole:
        jeu.pc[i] = old
        [a, b] = old
        jeu.laby[a, b] = 2
        [a, b] = new
        jeu.laby[a, b] = 0




"""
##########################################
#          Tables de hachages            #
##########################################
"""




def table_hachage(n=257) :
    "Cree une table de False"
    return np.array([False for _ in range(n)])

def hachage1(jeu, n=257) :
    "Fonction de hachage"
    liste = []
    for x in jeu.pc :
        liste += x
    a, b = jeu.pj
    liste += [a, b]
    cle = 0
    i = 1
    for x in liste :
        cle += (x * i) ** 5
        i += 1
    return cle % n

def hachage2(jeu, n=257):
    "Autre fonction de hachage"
    liste = []
    for x in jeu.pc :
        liste += x
    a, b = jeu.pj
    liste += [a, b]
    cle = 0
    i = 1
    for x in liste :
        cle += i ** x
        i += 1
    return cle % n

def aux_solveur_hachage(jeu, nb_coups_restants, args):
    "Fonction auxiliaire pour le solveur utilisant les tables de hachage"
    coup, affichage, tab_hash, hachage, n = args["coup"], args["affichage"], args["tab_hash"], args["hachage"], args["n"]
    boole, i, old, new = jeu.avancee(coup, True, True)
    cle = hachage(jeu, n)
    res = False
    if not tab_hash[cle]:                                                                                       #Position pas encore visitee
        tab_hash[cle] = True
        res = solveur_general(jeu, aux_solveur_hachage, pre_verif_hachage, nb_coups_restants, args)
    jeu.avancee(complementaire(coup), check=True)
    reset_caisses2(jeu, boole, i, old, new)
    if affichage:
        print(coup)
        print(jeu.pc)
        print("Hash : ", cle)
    return res

def pre_verif_hachage(jeu, args, nb_coups_restant):
    "Actions preliminaires pour le solveur utilisant les tables de hachage"
    pass                                                                                                        #Pas d'actions preliminaires pour ce solveur

def solveur_hachage(jeu, nb_coups_restants, tab_hash, hachage, affichage=False):
    "Solveur hachage v1"
    n = len(tab_hash)
    args = {"tab_hash" : tab_hash, "hachage" : hachage, "n" : n, "coup" : "Haut", "affichage" : affichage, "sol" : []}
    solveur_general(jeu, aux_solveur_hachage, pre_verif_hachage, nb_coups_restants, args)
    args["sol"].reverse()
    return args["sol"]

"""-------------------------------------------------------------------------"""

def table_hachage_injectif(jeu) :
    "Cree une table de False pour le hachage injectif"
    n = max(len(jeu.laby), len(jeu.laby[0]))
    p = len(str(n))
    taille = n ** (p * 2 * (len(jeu.pc) + 1))                                                                   #Nombre d'etats possibles : n ** ((nb_caisse + pj) * p)
    return np.array([False for _ in range(int(taille))]), np.array([0 for _ in range(int(taille))])

def to_str_len_p(x,p):
    "Renvoie x convertie en str sur p caracteres"
    x = str(x)
    xlen = len(x)
    if xlen < p:
        x = "0" * (p - xlen) + x                                                                                #Ajout d'eventuels 0 pour obtenir une chaine de la bonne taille
    return x

def hachage_injectif(jeu) :
    "Fonction de hachage injective"
    n, p = max(len(jeu.laby), len(jeu.laby[0])), len(jeu.pc)
    cle = 0
    for i in range(p):
        cle += jeu.pc[i][0] * (n ** (2 * i)) + jeu.pc[i][1] * (n **  (2 * i + 1))                                         #Ecriture en "base n"
    x, y = jeu.pj
    cle += x * (n ** (2 * p)) + y * (n **  (2 * p + 1))
    return cle

def aux_solveur_hachage_injectif(jeu, nb_coups_restants, args):
    "Fonction auxiliaire pour le solveur utilisant la fonction de hachage injective"
    tab_coups, tab_cle, coup, affichage = args["tab_coups"], args["tab_cle"], args["coup"], args["affichage"]
    boole, i, old, new = jeu.avancee(coup, True, True)
    cle = hachage_injectif(jeu)
    res = False
    if not tab_cle[cle] or (nb_coups_restants > tab_coups[cle]):                                                #Position non deja visitee ou visitee avec un nombre de coups plus petit
        tab_cle[cle] = True
        tab_coups[cle] = nb_coups_restants
        res = solveur_general(jeu, aux_solveur_hachage_injectif, pre_verif_hachage_injectif, nb_coups_restants, args)
    jeu.avancee(complementaire(coup), check = True)
    reset_caisses2(jeu, boole, i, old, new)
    if affichage:
        print(coup)
        print(jeu.pc)
        print("Hash : ", cle)
    return res

def pre_verif_hachage_injectif(jeu, args, nb_coups_restant):
    "Actions preliminaires pour le solveur utilisant la fonction de hachage injective"
    pass                                                                                                        #Pas d'actions preliminaires pour ce solveur

def solveur_hachage_injectif(jeu, nb_coups_restants, affichage=False):
    "Solveur hachage v2"
    tab_cle, tab_coups = table_hachage_injectif(jeu)
    args = {"sol" : [], "coup" : "Haut", "tab_coups" : tab_coups, "tab_cle" : tab_cle, "affichage" : affichage}
    solveur_general(jeu, aux_solveur_hachage_injectif, pre_verif_hachage_injectif, nb_coups_restants, args)
    args["sol"].reverse()
    return args["sol"]




"""
##########################################
#          Version dictionnaire          #
##########################################
"""




def hachage_tuple(jeu):
    "Fonction de hachage avec les tuples pour le solveur version dictionnaire"
    L = sorted(jeu.pc)
    #L = jeu.pc
    pc_tuple = tuple(tuple(L[i]) for i in range(len(jeu.pc)))                                       #Transformation en tuple
    key = jeu.pj, pc_tuple
    return key

def hachage_str(jeu):
    "Fonction de hachage avec les chaines de caracteres pour le solveur version dictionnaire"
    L = sorted(jeu.pc)
    #L = jeu.pc
    x, y = jeu.pj
    LL = [str(x), str(y)]
    LL += [str(L[i][j]) for i in range(len(L)) for j in range(2)]
    key = " ".join(LL)                                                                              #Transformation en string
    return key

def lprem():
    "Liste des nombres premiers inferieurs a 1000"
    return [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]

nbprem = lprem()

def hachage_nbprem(jeu):
    x, y = jeu.pj
    L = [[x, y]] + sorted(jeu.pc)
    key = 1
    for k in range(len(L)):
        key *= nbprem[2 * k] ** L[k][0]
        key *= nbprem[2 * k + 1] ** L[k][1]
    return key

def aux_solveur_dico(jeu, nb_coups_restant, args):
    "Fonction auxiliaire pour le solveur utilisant les dictionnaires"
    dic, coup, affichage = args["dic"], args["coup"], args["affichage"]
    boole, i, old, new = jeu.avancee(coup, True, True)                                              #Mouvement
    cle = hachage_str(jeu)
    res = False
    try:                                                                                            #Position deja vue
        nb_coup = dic[cle]
        if nb_coups_restant > nb_coup:
            dic[cle] = nb_coups_restant
            res = solveur_general(jeu, aux_solveur_dico, pre_verif_dico, nb_coups_restant, args)    #On ne reessaie que si il nous reste plus de coups que la fois precedente
    except KeyError:                                                                                #Si la position n'a pas ete vue (Exception KeyError declenchee)
        dic[cle] = nb_coups_restant
        res = solveur_general(jeu, aux_solveur_dico, pre_verif_dico, nb_coups_restant, args)
    jeu.avancee(complementaire(coup), check=True)                                                   #Annulation du coup
    reset_caisses2(jeu, boole, i, old, new)
    if affichage:                                                                                   #Pour le debug
        print(coup)
        print(jeu.pc)
        print("Hash : ", cle)
    return res

def pre_verif_dico(jeu, args, nb_coups_restant):
    "Actions preliminaires pour le solveur utilisant les dictionnaires"
    if args["dead"] and nb_coups_restant % 7 == 1:                                                  #On verifie les deadlocks tous les 7 coups
            stop = check_deadlock(jeu)
            if not stop:
                return False

def solveur_dico(jeu, nb_coups_restants, dic=None, dead=True, aff=False):
    "Solveur dico v1"
    if dic is None:
        dic = {}
    args = {"sol" : [], "coup" : "Haut", "affichage" : aff, "dic" : dic, "dead" : dead}
    if dead :
        reperage(jeu)                                                                               #On repere les case menant a coup sur a une defaite
    solveur_general(jeu, aux_solveur_dico, pre_verif_dico, nb_coups_restants, args)
    args["sol"].reverse()
    if dead:
        remove_deads(jeu)
    return args["sol"]

def test_sol(jeu, sol):
    "Verefie si sol est bien solution du jeu"
    cop = jeu.copy()
    for x in sol:
        cop.avancee(x)
    if victoire(cop) :
        print(cop.laby)
        return "Probleme resolu !"
    else :
        print(cop.laby)
        return "Ce n'est pas une solution"




"""
##########################################
#               Deadlocks                #
##########################################
"""



def est_deadlock1(jeu, x, y):
    "Verifie si la case x, y est un coin dans le labyrinthe (case supposee non position de victoire)"
    L = [((1, 0), (0, 1)), ((1, 0), (0, -1)), ((-1, 0), (0, 1)), ((-1, 0), (0, -1))]                # Coin bas - droite / bas - gauche / haut - droite / haut - gauche
    for ((a, b), (c, d)) in L:
        if jeu.laby[x + a, y + b] == 1 == jeu.laby[x + c, y + d]:
            return True
    return False

def deadlock2(jeu):
    "Deadlocks des carres"
    if len(jeu.pc) < 4:
        return True
    else:
        for [x, y] in jeu.pc:
            if jeu.laby[x + 1, y] == jeu.laby[x, y + 1] == jeu.laby[x + 1, y + 1] == 2 or \
                jeu.laby[x + 1, y] == jeu.laby[x, y - 1] == jeu.laby[x + 1, y - 1] == 2 or \
                jeu.laby[x - 1, y] == jeu.laby[x, y + 1] == jeu.laby[x - 1, y + 1] == 2 or \
                jeu.laby[x - 1, y] == jeu.laby[x, y - 1] == jeu.laby[x - 1, y - 1] == 2:            #la case est le coin haut - gauche / haut - droite / bas - gauche / bas - droite du carre
                    if not [x, y] in jeu.pv:
                        return False
        return True

def est_deadlock3(jeu, x, y) :
    "Teste si une position est contre un mur et qu'on ne peut pas en retirer une caisse eventuelle ne peut pas partir (case supposee non position de victoire)"
                                                                                                    #Chaque boucle fais le meme teste, en changeant le cote longe
    if jeu.laby[x, y + 1] == 1:                                                                     #Mur vertical droit
        i = x + 1                                                                                   #On avance vers le bas
        test_pv_i = False                                                                           #True si on a rencontre une p_v, False sinon
        rencontre_mur_i = False                                                                     #True si on est arrive en face d'un mur, False sinon
        while not test_pv_i and not rencontre_mur_i and jeu.laby[i, y + 1] == 1:                    #Verifie qu'on est toujours contre un mur et qu'on a pas encore rencontre de p_v ou de mur
            if [i, y] in jeu.pv:
                test_pv_i = True
            elif jeu.laby[i, y] in [1, 4]:
                rencontre_mur_i = True
            i += 1
        if rencontre_mur_i :                                                                        #Si on a rencontre un mur mais pas de p_v, on essaie en descendant
            j = x - 1
            test_pv_j = False
            rencontre_mur_j = False
            while not test_pv_j and not rencontre_mur_j and jeu.laby[j, y + 1] == 1:
                if [j, y] in jeu.pv:
                    test_pv_j = True
                elif jeu.laby[j, y] in [1, 4]:
                    rencontre_mur_j = True
                j -= 1
            if rencontre_mur_j:                                                                     #Si on a rencontre un mur dans les deux sens, c'est perdu
                return False
    if jeu.laby[x, y - 1] == 1:                                                                     #Mur vertical gauche
        i = x + 1
        test_pv_i = False
        rencontre_mur_i = False
        while not test_pv_i and not rencontre_mur_i and jeu.laby[i, y - 1] == 1:
            if [i, y] in jeu.pv:
                test_pv_i = True
            elif jeu.laby[i, y] in [1, 4]:
                rencontre_mur_i = True
            i += 1
        if rencontre_mur_i:
            j = x - 1
            test_pv_j = False
            rencontre_mur_j = False
            while not test_pv_j and not rencontre_mur_j and jeu.laby[j, y - 1] == 1:
                if [j, y] in jeu.pv:
                    test_pv_j = True
                elif jeu.laby[j, y] in [1, 4]:
                    rencontre_mur_j = True
                j -= 1
            if rencontre_mur_j:
                return False
    if jeu.laby[x - 1, y] == 1:                                                                     #Mur horizontal haut
        i = y + 1                                                                                   #On avance vers la droite
        test_pv_i = False
        rencontre_mur_i = False
        while not test_pv_i and not rencontre_mur_i and jeu.laby[x - 1, i] == 1:
            if [x, i] in jeu.pv:
                test_pv_i = True
            elif jeu.laby[x, i] in [1, 4]:
                rencontre_mur_i = True
            i += 1
        if rencontre_mur_i:                                                                         #On avance vers la gauche
            j = y - 1
            test_pv_j = False
            rencontre_mur_j = False
            while not test_pv_j and not rencontre_mur_j and jeu.laby[x - 1, j] == 1:
                if [x, j] in jeu.pv:
                    test_pv_j = True
                elif jeu.laby[x, j] in [1, 4]:
                    rencontre_mur_j = True
                j -= 1
            if rencontre_mur_j :
                return False
    if jeu.laby[x + 1, y] == 1:                                                                     #Mur horizontal bas
        i = y + 1
        test_pv_i = False
        rencontre_mur_i = False
        while not test_pv_i and not rencontre_mur_i and jeu.laby[x + 1, i] == 1:
            if [x, i] in jeu.pv:
                test_pv_i = True
            elif jeu.laby[x, i] in [1, 4]:
                rencontre_mur_i = True
            i += 1
        if rencontre_mur_i :
            j = y - 1
            test_pv_j = False
            rencontre_mur_j = False
            while not test_pv_j and not rencontre_mur_j and jeu.laby[x + 1, j] == 1:
                if [x, j] in jeu.pv:
                    test_pv_j = True
                elif jeu.laby[x, j] in [1, 4]:
                    rencontre_mur_j = True
                j -= 1
            if rencontre_mur_j:
                return False
    return True

def deadlock4(jeu) :
    "Test si on a 2 caisses l'une contre l'autre contre un mur"
    for [x,y] in jeu.pc :
        if not([x, y] in jeu.pv) :
            if (jeu.laby[x, y + 1] == 2 and (jeu.laby[x - 1, y] == jeu.laby[x - 1, y + 1] == 1 or jeu.laby[x + 1, y] == jeu.laby[x + 1, y + 1] == 1)) or\
            (jeu.laby[x, y - 1] == 2 and (jeu.laby[x - 1, y] == jeu.laby[x - 1, y - 1] == 1  or jeu.laby[x + 1, y] == jeu.laby[x + 1, y - 1] == 1)) or\
            (jeu.laby[x - 1, y] == 2 and (jeu.laby[x, y + 1] == jeu.laby[x - 1, y + 1] == 1 or jeu.laby[x, y - 1] == jeu.laby[x - 1, y - 1] == 1)) or\
            (jeu.laby[x + 1, y] == 2 and (jeu.laby[x, y + 1] == jeu.laby[x + 1, y + 1] == 1 or jeu.laby[x, y - 1] == jeu.laby[x + 1, y - 1] == 1)): #Caisse a droite / a gauche / en haut / en bas
                return False
    return True

def deadlock5(jeu):
    "Deadlock des trois caisses dans un angle"
    if len(jeu.pc) < 3:
        return True
    for [x, y] in jeu.pc:
        if (jeu.laby[x + 1, y - 1] == 1 and (jeu.laby[x, y - 1] == 2 == jeu.laby[x + 1, y])) \
            or (jeu.laby[x + 1, y + 1] == 1 and (jeu.laby[x, y + 1] == 2 == jeu.laby[x + 1, y])) \
            or (jeu.laby[x - 1, y - 1] == 1 and (jeu.laby[x, y - 1] == 2 == jeu.laby[x - 1, y])) \
            or (jeu.laby[x - 1, y + 1] == 1 and (jeu.laby[x, y + 1] == 2 == jeu.laby[x - 1, y])):   #Angle bas - gauche / bas - droite / haut - gauche / haut - droite
                return False
    return True

def remove_deads(jeu):
    "Enleve les 4 du jeu"
    nx, ny = len(jeu.laby), len(jeu.laby[0])
    for x in range(1, nx - 1):
        for y in range(1, ny - 1):
            if jeu.laby[x, y] == 4:
                jeu.laby[x, y] = 0
    jeu.case = 0

def check_deadlock(jeu):
    "Verifie si le jeu est bloque pour l'un des deadlocks implemente"
    L = [deadlock2, deadlock4, deadlock5]                                                           #Fonctions de deadlocks a verifier
    res = True
    for f in L:
        res = res and f(jeu)
    return res

def reperage(jeu) :
    "Mise en place des 4 (deadlocks previsibles)"
    for x in range(len(jeu.laby)):
        for y in range(len(jeu.laby[0])):
            if jeu.laby[x, y] == 0 and not [x, y] in jeu.pv:
                if est_deadlock1(jeu, x, y) or not est_deadlock3(jeu, x, y):
                    jeu.laby[x, y] = 4
    x, y = jeu.pj
    if not [x, y] in jeu.pv and (est_deadlock1(jeu, x, y) or not est_deadlock3(jeu, x, y)):
        jeu.case = 4




"""
##########################################
#          Exploration guidee            #
##########################################
"""




def dir_caisse(x, y, xc, yc):
    "Rnvoie l'ordre des directions dans lesquelles aller pour atteindre la caisse (xc, yc) depuis (x, y)"
    dx, dy = x - xc, y - yc
    L = []
    if dx > 0:
        if dy > 0:
            return ["Haut", "Gauche", "Bas", "Droite"]
        else:
            return ["Haut", "Droite", "Bas", "Gauche"]
    elif dx < 0:
        if dy > 0:
            return ["Bas", "Gauche", "Haut", "Droite"]
        else:
            return ["Bas", "Droite", "Haut", "Gauche"]
    elif dy > 0:
        return ["Gauche", "Haut", "Bas", "Droite"]
    return ["Droite", "Haut", "Bas", "Gauche"]

def order_dir(jeu):
    "Renvoie l'ordre dans lequel doivent etre effectus les mouvements pour se rapprocher des caisses"
    x, y = jeu.pj
    Ld = [abs(x - jeu.pc[i][0] + y - jeu.pc[i][1]) for i in range(len(jeu.pc))]
    i = 0
    for k in range(len(Ld)):
        if Ld[k] < Ld[i]:
            i = k
    return dir_caisse(x, y, jeu.pc[i][0], jeu.pc[i][1])

def solveur_general2(jeu, fonction_aux, pre_aux, nb_coups_restants, args={}):
    "Solveur ou l'ordre d'exploration est determine par la distance a la caisse la plus proche"
    if args["affichage"]:
        print(args["coup"], " ", nb_coups_restants)
        print(jeu)

    if victoire(jeu):
        return True

    elif nb_coups_restants == 0:
        return False

    else:
        if pre_aux(jeu, args, nb_coups_restants) == False:                                                          #Actions preliminaires, renvoyant eventuellement False si la partie est perdue
            return False
        nb_coups_restants -= 1
        bh, bb, bd, bg = jeu.go_h_bool(), jeu.go_b_bool(), jeu.go_d_bool(), jeu.go_g_bool()
        Ldir = order_dir(jeu)

        for d in Ldir:
            if jeu.avancee_bool(d):
                args["coup"] = d
                if fonction_aux(jeu, nb_coups_restants, args):
                    args["sol"].append(d)
                    return True

        return False

def aux_solveur_dico2(jeu, nb_coups_restant, args):
    "Fonction auxiliaire pour le second solveur utilisant les dictionnaires"
    dic, coup, affichage = args["dic"], args["coup"], args["affichage"]
    boole, i, old, new = jeu.avancee(coup, True, True)                                              #Mouvement
    cle = hachage_str(jeu)
    res = False
    try:                                                                                            #Position deja vue
        nb_coup = dic[cle]
        if nb_coups_restant > nb_coup:
            dic[cle] = nb_coups_restant
            res = solveur_general2(jeu, aux_solveur_dico2, pre_verif_dico, nb_coups_restant, args)  #On ne reessaie que si il nous reste plus de coups que la fois precedente
    except KeyError:                                                                                #Si la position n'a pas ete vue (Exception KeyError declenchee)
        dic[cle] = nb_coups_restant
        res = solveur_general2(jeu, aux_solveur_dico2, pre_verif_dico, nb_coups_restant, args)
    jeu.avancee(complementaire(coup), check=True)                                                   #Annulation du coup
    reset_caisses2(jeu, boole, i, old, new)
    if affichage:                                                                                   #Pour le debug
        print(coup)
        print(jeu.pc)
        print("Hash : ", cle)
    return res

def solveur_dico2(jeu, nb_coups_restants, dic=None, dead=True, aff=False):
    "Solveur dico pour le second solveur"
    if dic is None:
        dic = {}
    args = {"sol" : [], "coup" : "Haut", "affichage" : aff, "dic" : dic, "dead" : dead}
    if dead :
        reperage(jeu)                                                                               #On repere les case menant a coup sur a une defaite
    solveur_general2(jeu, aux_solveur_dico2, pre_verif_dico, nb_coups_restants, args)
    args["sol"].reverse()
    if dead:
        remove_deads(jeu)
    return args["sol"]

"""
D = {}
t1 = time.time()
L = solveur_dico(jeu1, 100, D)
t2 = time.time()
print(L)
print(t2 - t1)
print(len(D.keys()))
"""


"""
70 coups : 1135s, 3.334.855 etats -> 734s (portable) / 800s (fixe), 2.495.948 etats
90 coups : 2.325s, 4.230.695 etats                  (portable, en arriere plan)
137 coups : 6.137s, 5.312.655 etats                 (fixe)
136 coups : 5.968s, 5.310.618 etats                 (fixe)
132 coups : 6264s, 5.327.153 etats                  (portablen en arriere plan)
130 coups : 6332s, 5.321.506 etats                  (portablen en arriere plan)
"""

"""
D = {}
t1 = time.time()
L = solveur_dico(jeu_cosmos1, 48, D)
t2 = time.time()
print(t2 - t1)
print(len(D.keys()))
"""
"""
L1 = [jeu_test2, jeu_micro1, jeu_micro16]
L2 = [5,10,15,16,17,20,10,20,32,33,34,40,20,50,99,100,101,120]

for i in range(18):
    t1 = time.time()
    solveur_dico(L1[i//6],L2[i], dead = False)
    t2 = time.time()
    print(t2 - t1)
    print("___________")
"""

