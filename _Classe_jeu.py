"""
#######################################
#               TIPE                  #
#######################################
"""


"""
#######################################
#          Classe de Jeu              #
#######################################
"""
import numpy as np

class Jeu:
    "Definit l'objet jeu"

    def __init__(self, labyrinthe, pos_joueur, pos_caisses, pos_victoire, case=0):
        self.laby = labyrinthe
        self.pj = pos_joueur
        self.pc = pos_caisses
        self.pv = pos_victoire
        self.case = case

    def __repr__(self):
        res = self.laby.__repr__() + '\n'
        res += 'Position du joueur : ' + str(self.pj) + '\n'
        res += 'Positions des caisses : ' + self.pc.__repr__() + '\n'
        res += 'Positions de victoire : ' + self.pv.__repr__()
        return res

    def go_h (self, check=False, ret=False) :
        "Modifie (si possible) le labyrinthe en faisant monter le joueur"
        if check or self.go_h_bool():
            x, y = self.pj
            if self.laby[x - 1, y] == 2 :
                self.laby[x - 2, y] = 2
                self.laby[x, y], self.case = self.case, 0
                self.laby[x - 1, y] = 5
                self.pj = (x - 1, y)
                i = self.pc.index([x - 1, y])
                self.pc[i] = [x - 2, y]
                if ret :
                    return True, i, [x - 1, y], [x - 2, y]
            else :
                self.laby[x, y], self.case = self.case, self.laby[x - 1, y]
                self.laby[x - 1, y] = 5
                self.pj = (x - 1, y)
                if ret:
                    return False, None, None, None
        if ret:
            return False, None, None, None

    def go_b (self, check=False, ret=False) :
        "Modifie (si possible) le labyrinthe en faisant descendre le joueur"
        if check or self.go_b_bool():
            x, y = self.pj
            if self.laby[x + 1, y] == 2 :
                self.laby[x + 2, y] = 2
                self.laby[x, y], self.case = self.case, 0
                self.laby[x + 1, y] = 5
                self.pj = (x + 1, y)
                i = self.pc.index([x + 1, y])
                self.pc[i] = [x + 2, y]
                if ret :
                    return True, i, [x + 1, y], [x + 2, y]
            else :
                self.laby[x, y], self.case = self.case, self.laby[x + 1, y]
                self.laby[x + 1, y] = 5
                self.pj = (x + 1, y)
                if ret:
                    return False, None, None, None
        if ret:
            return False, None, None, None

    def go_d (self, check=False, ret=False) :
        "Modifie (si possible) le labyrinthe en faisant aller a droite le joueur"
        if check or self.go_d_bool():
            x, y = self.pj
            if self.laby[x, y + 1] == 2 :
                self.laby[x, y + 2] = 2
                self.laby[x, y], self.case = self.case, 0
                self.laby[x, y + 1] = 5
                self.pj = (x, y + 1)
                i = self.pc.index([x, y + 1])
                self.pc[i] = [x, y + 2]
                if ret :
                    return True, i, [x, y + 1], [x, y + 2]
            else :
                self.laby[x, y], self.case = self.case, self.laby[x, y + 1]
                self.laby[x, y + 1] = 5
                self.pj = (x, y + 1)
                if ret:
                    return False, None, None, None
        if ret:
            return False, None, None, None

    def go_g (self, check=False, ret=False) :
        "Modifie (si possible) le labyrinthe en faisant aller a gauche le joueur"
        if check or self.go_g_bool():
            x, y = self.pj
            if self.laby[x, y - 1] == 2 :
                self.laby[x, y - 2] = 2
                self.laby[x, y], self.case = self.case, 0
                self.laby[x, y - 1] = 5
                self.pj = (x, y - 1)
                i = self.pc.index([x, y - 1])
                self.pc[i] = [x, y - 2]
                if ret :
                    return True, i, [x, y - 1], [x, y - 2]
            else :
                self.laby[x, y], self.case = self.case, self.laby[x, y - 1]
                self.laby[x, y - 1] = 5
                self.pj = (x, y - 1)
                if ret:
                    return False, None, None, None
        if ret:
            return False, None, None, None

    def go_h_bool (self) :
        "Renvoie True si on peut monter, False sinon"
        x, y = self.pj
        if self.laby[x - 1, y] in [0, 4]:                                       #Case superieure = vide
            return True
        elif self.laby[x - 1, y] == 2:                                          #Case superieur = caisse
            if self.laby[x - 2, y] in [2, 1, 4]:                                #Caisse non bougeable
                return False
            else :                                                              #Caisse bougeable
                return True
        else :
            return False

    def go_b_bool (self) :
        "Renvoie True si on peut descendre, False sinon"
        x, y = self.pj
        if self.laby[x + 1, y] in [0, 4]:                                       #Case inferieure = vide
            return True
        elif self.laby[x + 1, y] == 2:                                          #Case inferieure = caisse
            if self.laby[x + 2, y] in [2, 1, 4]:                                #Caisse non bougeable
                return False
            else :                                                              #Caisse bougeable
                return True
        else :
            return False

    def go_d_bool (self) :
        "Renvoie True si on peut aller a droite, False sinon"
        x, y = self.pj
        if self.laby[x, y + 1] in [0, 4]:                                       #Case de droite = vide
            return True
        elif self.laby[x, y + 1] == 2:                                          #Case de droite = caisse
            if self.laby[x, y + 2] in [2, 1, 4]:                                #Caisse non bougeable
                return False
            else :                                                              #Caisse bougeable
                return True
        else :
            return False

    def go_g_bool (self) :
        "Renvoie True si on peut aller a gauche, False sinon"
        x, y = self.pj
        if self.laby[x, y - 1] in [0, 4]:                                       #Case de gauche = vide
            return True
        elif self.laby[x, y - 1] == 2:                                          #Case de gauche = caisse
            if self.laby[x, y - 2] in [2, 1, 4]:                                #Caisse non bougeable
                return False
            else :                                                              #Caisse bougeable
                return True
        else :
            return False

    def avancee_bool(self, direction):
        "Renvoie True si on peut aller dans la direction, False sinon"
        D = {"Haut" : Jeu.go_h_bool, "Bas" : Jeu.go_b_bool, "Droite" : Jeu.go_d_bool, "Gauche" : Jeu.go_g_bool}
        return D[direction](self)

    def avancee(self, direction, check=False, ret=False) :
        "Fait avancer le personnage dans la direction donnee (si possible)"
        D = {"Haut" : Jeu.go_h, "Bas" : Jeu.go_b, "Droite" : Jeu.go_d, "Gauche" : Jeu.go_g}
        res = D[direction](self, check, ret)
        if ret:
            return res

    def copy(self):
        "Renvoie une copie du jeu"
        lab = np.array([[self.laby[i, j] for j in range(len(self.laby[0]))] for i in range(len(self.laby))])
        pc = [[self.pc[i][j] for j in range(len(self.pc[0]))] for i in range(len(self.pc))]
        pj = self.pj
        pv = [[self.pv[i][j] for j in range(len(self.pv[0]))] for i in range(len(self.pv))]
        case = self.case
        return Jeu(lab, pj, pc, pv, case)
