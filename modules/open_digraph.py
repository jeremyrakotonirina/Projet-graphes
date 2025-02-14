import random

class node:

    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity, multiplicite: nb arrête entre 2 noeuds
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children
    
    def __str__(self):
        """Affichage dans la console"""
        return f"node(id={self.id}, label='{self.label}', parents={list(self.parents.keys())}, children={list(self.children.keys())})"
    
    def __repr__(self):
        """Affichage inductive du noeud"""
        return f"node({self.id}, '{self.label}', {self.parents}, {self.children})"
    
    def copy(self):
        """Retourne une copie du noeud"""
        return node(self.id, self.label, self.parents.copy(), self.children.copy())
    
    #-------------------Getters------------
    def get_id(self):
        return self.id
    
    def get_label(self):
        return self.label
    
    def get_parents(self):
        return self.parents
    
    def get_children(self):
        return self.children
    
    #------------------Setters---------------------------
    def set_id(self, new_id):
        """Remplace l'identifiant du noeud"""
        self.id = new_id

    def set_label(self, new_label):
        """Remplace le label du noeud."""
        self.label = new_label

    def set_parents(self, new_parents):
        """Remplace la liste des parents"""
        self.parents = new_parents

    def set_children(self, new_children):
        """Remplace la liste des enfants"""
        self.children = new_children
    
    def add_parent_id(self, idparent, multiplicite):
        """Ajoute un parent avec sa multiplicité"""
        self.parents[idparent]=multiplicite
        
    def add_child_id(self, idchildren, multiplicite):
        """Ajoute un enfant avec sa multiplicité"""
        self.children[idchildren] = multiplicite
            

class open_digraph:

    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes}
    
    #----------Méthodes d'affichage-----------------
    
    def __str__(self):
        "Affichage dans la console"
        nodes_str = "\n  ".join(str(node) for node in self.nodes.values()) #affichage des noeuds
        return f"open_digraph(\nInputs: {self.inputs}, \nOutputs: {self.outputs}, \nNodes:\n  {nodes_str}\n)"
    
    def __repr__(self):
        """Affichage inductive du graphe"""
        return f"open_digraph({self.inputs}, {self.outputs}, {list(self.nodes.values())})"
    
    #--------------------------------------------------
    
    @classmethod
    def empty(cls):
        """Crée et retourne un graphe vide"""
        return cls([],[],[])
    
    def copy(self):
        """Retourne une copie du graphe"""
        return open_digraph( self.inputs.copy(), self.outputs.copy(),
            [noeud.copy() for noeud in self.nodes.values()] 
        )
    
     #-------------Getters---------------------------
    def get_input_ids(self):
        return self.inputs
    
    def get_output_ids(self):
        return self.outputs
    
    def get_id_node_map(self):
        """renvoie un dictionnaire id:node"""
        return self.nodes
    
    def get_nodes(self):
        """renvoie une liste de tous les noeuds"""
        return [self.nodes[cle] for cle in self.nodes]
    
    def get_node_ids(self, n):
        """renvoie l'ID du noeud n"""
        return [ID for ID,noeud in self.nodes.items() if n==noeud][0] #premier élément
    
    def get_node_by_id(self, ID):
        """renvoie le noeud d'id ID"""
        return self.nodes[ID]
    
    def get_nodes_by_ids(self, IDS):
        """renvoie une liste de noeuds à partir d'une liste d'ids"""
        return [self.nodes[cle] for cle in self.nodes if cle in IDS]
    
    #-------------Setters---------------------------   
    def set_inputs(self, new_inputs):
        """Remplace la liste des entrées"""
        self.inputs = new_inputs

    def set_outputs(self, new_outputs):
        """Remplace la liste des sorties"""
        self.outputs = new_outputs
    
    def add_input_id(self, ID):
        """Ajoute un nouvel id dans la liste des entrées"""
        if ID not in self.inputs:
            self.inputs.append(ID)
    
    def add_output_id(self, ID):
        """Ajoute un nouvel id dans la liste des sorties"""
        if ID not in self.outputs:
            self.outputs.append(ID)
    
    #----------Méthodes d'ajout -------------------------------
    
    def new_id(self):
        """Renvoie un id non utilisé jusquà ce moment pour un nouveau noeud"""
        new_id = 0 
        while new_id in self.get_id_node_map():
            new_id += 1 
        return new_id
    
    def add_edge(self, src, tgt):
        """Ajoute une arête du noeud src au noeud tgt, prend les id des noeuds en paramètre"""
        if (src in self.get_id_node_map() and tgt in self.get_id_node_map()):  #vérifier qu'ils existent
            self.nodes[src].add_child_id(tgt, 1)
            self.nodes[tgt].add_parent_id(src, 1)
        else :
            raise ValueError ("Vous avez donné des noeuds qui n'existent pas")
        
    def add_edges(self, edges):
        """edges prend une liste de paires d'ids de noeuds, et la méthode rajoute une arête entre chacune de ces paires"""
        for src, tgt in edges:
            self.add_edge(src, tgt)
    
    """def add_node(self, label='', parents=None, children=None):
        rajoute un noeud au graphe
        nouveau_id= self.new_id()
        if parents==None:
            parents={}
        if children==None:
            children={}
        self.get_id_node_map[nouveau_id]= node(nouveau_id, label, {parents:})
        """

    
    def add_input_node(self, tgt):
        """Ajoute un nouveau noeud d'entrée qui pointe vers tgt"""
        if tgt not in self.get_id_node_map():
            raise ValueError("le noeud tgt n'existe pas")
    
        new_id = self.new_id()
        new_node = node(new_id, "", {}, {tgt: 1})  #  1 arête vers tgt
    
        self.nodes[new_id] = new_node  # Ajout du nouveau noeud dans le graphe
        self.nodes[tgt].add_parent_id(new_id, 1)  # ajout du nouveau parent de tgt
        self.add_input_id(new_id)  # Ajout à la liste des entrées
        
        return new_id 
    
    def add_output_node(self, tgt):
        """Ajoute un nouveau noeud de sortie qui pointe vers tgt"""
        if tgt not in self.get_id_node_map():
            raise ValueError("le noeud tgt n'existe pas")
    
        new_id = self.new_id()
        new_node = node(new_id, "", {tgt:1}, {})  #  1 arête vers tgt
    
        self.nodes[new_id] = new_node  # Ajout du nouveau noeud dans le graphe
        self.nodes[tgt].add_child_id(new_id, 1)  # ajout du nouvel enfant de tgt
        self.add_output_id(new_id)  # Ajout à la liste des sorties
        
        return new_id 
    

    #---------Méthodes de suppression---------------

    def remove_parent_once(self, id_noeud, id_parent):
        """Retire 1 occurence (1 multiplicité) d'un parent dans un noeud"""
       
        noeud = self.get_node_by_id(id_noeud) #cherche le noeud
        noeud.get_parents()[id_parent] -= 1
        if noeud.get_parents()[id_parent] == 0:
            del noeud.get_parents()[id_parent] #enlève l'arête si c'est égal à 0
   
    def remove_child_once(self, id_noeud, id_children):
        """Retire 1 occurence (1 multiplicité) d'un enfant dans un noeud"""

        noeud = self.get_node_by_id(id_noeud)#cherche le noeud
        noeud.get_children()[id_children] -= 1
        if noeud.get_children()[id_children] == 0:
            del noeud.get_children()[id_children] #enlève l'arête si c'est égal à 0
   
    def remove_parent_id(self, id_noeud, id_parent):
        """Retire toutes les occurences d'un parent dans un noeud"""
        noeud = self.get_node_by_id(id_noeud) #cherche le noeud
        del noeud.get_parents()[id_parent]

    def remove_child_id(self, id_noeud, id_children):
        """Retire toutes les occurences d'un enfant dans un noeud"""
        noeud = self.get_node_by_id(id_noeud) #cherche le noeud
        del noeud.get_children()[id_children]
   
    def remove_edge(self, src, tgt):
        """Retire 1 multiplicté de l'arête qui va de l'id src vers l'id tgt"""
        self.remove_parent_once(tgt, src)#supprime dans l'instance de chacun des deux noeuds
        self.remove_child_once(src, tgt)
   
    def remove_parallel_edges(self, src, tgt):
        """Retire toutes les multiplicités de l'arête qui va de l'id src vers l'id tgt"""
        self.remove_parent_id(tgt,src) #supprime dans l'instance de chacun des deux noeuds
        self.remove_child_id(src,tgt)
    
    def remove_node_by_id(self, id_noeud):
        """Retire les arêtes associées à un noeud"""
        noeud = self.get_node_by_id(id_noeud)
        
        for id_parent in noeud.get_parents(): #supprime arête des parents
            self.remove_child_id(id_parent, id_noeud)
        
        for id_child in noeud.get_children(): #supprime arête des enfants
            self.remove_parent_id(id_child, id_noeud)
    
    def remove_edges(self, *args):
        """Retire une multiplicité des arêtes dans les arguments
        Les arguments doivent être des listes de paires de l'id source et l'id 
        destination"""
        for src, tgt in args:
            self.remove_edge(src, tgt)
    
    def remove_several_parallel_edges(self, *args):
        """Retire toutes les multiplicités des arêtes dans les arguments
        Les arguments doivent être des listes de paires de l'id source et l'id 
        destination"""
        for src, tgt in args:
            self.remove_parallel_edges(src, tgt)
    
    def remove_nodes_by_id(self, *args):
        """Retire toutes les arêtes associées à un noeud"""
        for id_noeud in args:
            self.remove_node_by_id(id_noeud)
    
    #----------------------------------

    def is_well_formed(self):
        """Vérifie qu'un graphe est toujours bien formé"""
        for noeud in self.get_input_ids()+self.get_output_ids(): #chaque noeud d'input et output doit être dans le graphe
            if noeud.get_id() not in self.get_id_node_map():
                return False
        
        for noeud in self.get_input_ids():
            if len(noeud.get_children()) != 1 or len(noeud.get_parents()) != 0: #vérifie que les noeuds d'entrée ont un unique enfant et aucun parent
                return False
            for cle in noeud.get_children(): #vérifie que l'unique enfant est de multiplicité 1
                if noeud.get_children()[cle] != 1:
                    return False
        
        for noeud in self.get_output_ids():
            if len(noeud.get_parents()) != 1 or len(noeud.get_children()) != 0: #vérifie que les noeuds de sortie ont un unique parent et aucun enfant
                return False
            for cle in noeud.get_parents(): #vérifie que l'unique parent est de multiplicité 1
                if noeud.get_parents()[cle] != 1:
                    return False
        
        for noeud_id in noeud.get_id_node_map(): #chaque clé de nodes pointe vers un noeud d'id la clé
            noeud=noeud.get_id_node_map()[noeud_id]
            if noeud.get_id() != noeud_id : 
                return False
        
        for noeud_id in self.get_id_node_map():
            noeud=noeud.get_id_node_map()[noeud_id]
            for fils in noeud.get_children():
                multiplicite=noeud.get_children()[fils]
                
    @classmethod    # ça sert a quoi cette ligne de code ?
    def random(self, n, bound, inputs = 0, outputs = 0, form = "free"):   # a tester
        """ génère un graphe formé de n noeuds ou le nb d'arretes est aleatoire avec des valeurs entre 0 et bound inclus, on peut décider le graphe que l'on veut avec le parametre form
            valeurs possibles pour form :   free       -- 
                                            DAG        --  
                                            oriented   -- 
                                            undirected -- 
                                            loop-free  --   
        """
        if form == "free":
            return graph_from_adjacency_matrix(random_int_matrix(n, bound, False))
        elif form == "DAG":
            return graph_from_adjacency_matrix(random_triangular_int_matrix(n, bound, False))
        elif form == "oriented":
            return graph_from_adjacency_matrix(random_oriented_int_matrix(n, bound, False))
        elif form == "undirected":
            return graph_from_adjacency_matrix(random_symetric_int_matrix(n, bound, False))
        elif form == "loop-free":
            return graph_from_adjacency_matrix(random_int_matrix(n, bound, True))
        elif form == "loop-free DAG":
            return graph_from_adjacency_matrix(random_triangular_int_matrix(n, bound, True))
        elif form == "loop-free oriented":
            return graph_from_adjacency_matrix(random_oriented_int_matrix(n, bound, True))
        elif form == "loop-free undirected":
            return graph_from_adjacency_matrix(random_symetric_int_matrix(n, bound, True))
        else:
            raise ValueError(" Le paramètre form est mal donné, regarder la documentation pour plus d'info sur le paramètre ")
        
        


    """  A retraivailler, pas clair"""

    def association_ID(self):    # je sais pas a quoi elle sert la fonction on me la demandait dans le tp3
        dic = {}
        i = 0
        for id in self.get_id_node_map().keys():
            dic[id] = i
            i = i + 1
        return dic
    
    def adjacency_matrix(self):  #on soit la logique selon laquelle id du noeud = 0,1,2,3,4,5,etc. et que les noeuds sont gardés en ordre? car c'est un dictionnaire?
        """ renvoi la matrice d'adjacence du graphe, on ignore inputs et outputs """
        tab = []
        for id,noeud in self.get_id_node_map().items():
            petit_tab = [0] * len(id)   # on place dans la matrice les enfants
            for i in noeud.get_children().keys():                   # relation directe entre id et place dans le tableau
                petit_tab[i] += 1 
            tab.append(petit_tab)
        return tab

    """    """






def random_int_list(n, bound):
    """ renvoi une liste de taille n contenant des chiffres générés aléatoirement entre 0 et bound inclus """
    [random.randrange(0, bound+1) for i in range(n)]

def random_int_matrix(n, bound, null_diag = True):
    """ renvoi une matrice de taille n*n qui a comme éléments des int tirés aléatoirement entre 0 et bound inclus et si null_diag = True alors la diagonale sera nulle"""
    return [[0 if i == j and null_diag else random.randrange(0, bound+1) for j in range(n)] for i in range(n)]

def random_symetric_int_matrix(n, bound, null_diag = True):
    """ renvoi une matrice symetrique de taille n*n qui a comme éléments des int tirés aléatoirement entre 0 et bound inclus et si null_diag = True alors la diagonale sera nulle """
    tab = [n * [0] for i in range(n)]
    for i in range(n):
        for j in range(i,n):   # on remplit juste la partie en haut a droite de la matrice et on copie les valeurs dans tab[j][i]
            if i == j and null_diag:
                tab[i][j] = 0
            else:
                val = random.randrange(0, bound+1)
                tab[i][j] = val
                tab[j][i] = val
    return tab

def est_symetrique(tab, n):
    """ renvoi si le tableau double passé en paramètres est symetrique (n est la longueur du tableau)"""
    for i in range(n):
        for j in range(n):
            if(tab[i][j] != tab[j][i]):
                return False
    return True

def random_oriented_int_matrix(n, bound, null_diag = True):
    """ renvoi une matrice de taille n*n remplie avec des chiffres aléatoires entre 0 et bound inclus telle si A[i][j] != 0 alors A[j][i] == 0 et la fonction dispose du param null_diag """
    tab = [n * [0] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if (i == j and null_diag) or tab[j][i] != 0:   # tab[j][i] != 0 veut dire que il y a deja des arretes qui vont dans un sens entre les noeuds donc si c'est le cas il faut pas rajoutter plus d'arretes
                tab[i][j] = 0
            else:
                if random.random() < 0.5:    #est ce que c'est bon? parcque on augmente les chances que tab[i][j] == 0 ??             # on remplit la valeur avec une chance de 50% comme ça on evite que toutes les valeurs en haut à gauche aient des valeurs et pas les autres 
                    tab[i][j] = random.randrange(0, bound+1)
    return tab

# attention, dans le tp ils disent que graphe oriente implique que si un noeud pointe vers un autre alors l'autre ne peut pas pointer vers celui ci, c'est la bonne def de oriente??
def est_oriente(tab, n):
    """ renvoi si le tableau double passé en paramètres est orienté (n est la longueur du tableau)"""
    for i in range(n):
        for j in range(n):
            if(i != j and tab[i][j] == tab[j][i] and tab[i][j] != 0):
                return False
    return True

def random_triangular_int_matrix(n, bound, null_diag = True):
    """ renvoi une matrice triangulaire supérieure de taille n*n remplie avec des chiffres aléatoires entre 0 et bound inclu et la fonction dispose du param null_diag """
    tab = [n * [0] for i in range(n)]
    for i in range(n):
        for j in range(i,n):   # on remplit juste la partie en haut a droite de la matrice
            if i == j and null_diag:
                tab[i][j] = 0
            else:
                tab[i][j] = random.randrange(0, bound+1)
    return tab

def est_triangulaire_sup(tab, n):
    """ renvoi si le tableau double passé en paramètres est triangulaire sup (n est la longueur du tableau)"""
    for i in range(n):
        for j in range(i):
            if tab[i][j] != 0:
                return False
    return True

def graph_from_adjacency_matrix(matrice): # a tester
    """ renvoi le multigraph represente par la matrice donnee en parametres, on laisse les attributs input et output vides"""
    G = open_digraph([], [], [])
    for i in range(len(matrice)):
        G.add_node(node(i, str(i), [], []))    # ne marche que si new_id donne les id 0,1,2,3,4 en ordre sinon la suite n'a pas de sens #label = id??
    for i in range(len(matrice)):
        for j in range(len(matrice[1])):
            while matrice[i][j] != 0:         # on fait un while car il peu y avoir plusieurs arretes a placer
                G.add_edge(i, j)
    return G



    
    

    



