import random

def random_int_list(n, bound):
    """ renvoie une liste de taille n contenant des chiffres générés aléatoirement
    entre 0 et bound inclus """
    return [random.randrange(0, bound+1) for i in range(n)]

def random_int_matrix(n, bound, null_diag = True):
    """ renvoie une matrice de taille n*n qui a comme éléments des int tirés aléatoirement entre 0 et bound inclus et si null_diag = True alors la diagonale sera nulle"""
    return [[0 if (i == j and null_diag) else random.randrange(0, bound+1) for j in range(n)] for i in range(n)]

def random_symetric_int_matrix(n, bound, null_diag = True):
    """ renvoie une matrice symetrique de taille n*n qui a comme éléments des int tirés aléatoirement entre 0 et bound inclus et si null_diag = True alors la diagonale sera nulle """
    tab = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i,n):   # on remplit juste la partie en haut a droite de la matrice et on copie les valeurs dans tab[j][i]
            if i == j and null_diag:
                tab[i][j] = 0
            else:
                val = random.randrange(0, bound+1)
                tab[i][j] = val
                tab[j][i] = val
    return tab

def random_oriented_int_matrix(n, bound, null_diag = True):
    """ renvoie une matrice de taille n*n remplie avec des chiffres aléatoires entre 0 et bound inclus telle si A[i][j] != 0 alors A[j][i] == 0 et la fonction dispose du param null_diag """
    tab = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i,n):
            if (i == j ): #diagonale
                if null_diag:    
                    tab[i][j] = 0
                else:
                    tab[i][j] = random.randrange(0, bound+1)
            else:
                if random.random() < 0.5: #1 chance sur 2 de remplir en haut, sinon en bas
                    tab[i][j] = random.randrange(0, bound+1)
                    tab[j][i] = 0
                else:
                    tab[j][i] = random.randrange(0, bound +1)
                    tab[i][j] = 0
    return tab
   
    """Autre version qui augmente la chance d'avoir aucune arête entre 2 noeuds (1 chance sur 2)
    def random_oriented_int_matrix(n, bound, null_diag = True):
    tab = [n * [0] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if (i == j and null_diag) or tab[j][i] != 0:   # tab[j][i] != 0 veut dire que il y a deja des arretes qui vont dans un sens entre les noeuds donc si c'est le cas il faut pas rajoutter plus d'arretes
                tab[i][j] = 0
            else:
                if random.random() < 0.5:    #est ce que c'est bon? parcque on augmente les chances que tab[i][j] == 0 ??             # on remplit la valeur avec une chance de 50% comme ça on evite que toutes les valeurs en haut à gauche aient des valeurs et pas les autres
                    tab[i][j] = random.randrange(0, bound+1)
    return tab
    """

def random_triangular_int_matrix(n, bound, null_diag = True):
    """ renvoie une matrice triangulaire supérieure de taille n*n remplie avec des chiffres aléatoires entre 0 et bound inclu et la fonction dispose du param null_diag """
    tab = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i,n):   # on remplit juste la partie en haut a droite de la matrice
            if i == j and null_diag:
                tab[i][j] = 0
            else:
                tab[i][j] = random.randrange(0, bound+1)
    return tab

def afficher_matrice(matrice):
    """Affiche une matrice"""
    for ligne in matrice:
        print(ligne)
    print()