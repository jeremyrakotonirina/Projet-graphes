import random
import os #pour le display du noeud
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
        """Affichage détaillé du graphe dans la console, incluant les multiplicités des parents et enfants."""
        nodes_str = "\n  ".join(
            f"Node {node.id} ({node.label}):\n"
            f"    Parents: {dict(node.get_parents())}\n"
            f"    Children: {dict(node.get_children())}"
            for node in self.nodes.values()
        )
        return (
            f"open_digraph(\n"
            f"  Inputs: {self.inputs},\n"
            f"  Outputs: {self.outputs},\n"
            f"  Nodes:\n  {nodes_str}\n)"
        )
    
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
        """Ajoute une arête du noeud src au noeud tgt"""
        if src in self.get_id_node_map() and tgt in self.get_id_node_map():  # Vérifier qu'ils existent
            src_node = self.get_node_by_id(src)
            tgt_node = self.get_node_by_id(tgt)
            
            # Vérifier si l'arête existe déjà
            if tgt in src_node.get_children():
                src_node.add_child_id(tgt, src_node.get_children()[tgt] + 1)
                tgt_node.add_parent_id(src, tgt_node.get_parents()[src] + 1)
            else:
                src_node.add_child_id(tgt, 1)
                tgt_node.add_parent_id(src, 1)
        else:
            raise ValueError("Vous avez donné des noeuds qui n'existent pas")
        
    def add_edges(self, edges):
        """edges prend une liste de paires d'ids de noeuds, et la méthode rajoute une arête entre chacune de ces paires"""
        for src, tgt in edges:
            self.add_edge(src, tgt)
    
    def add_node(self, label='', parents=None, children=None):
        """rajoute un noeud au graphe et le lie avec les noeuds d'ids parent et children
        entrée: parents et children des listes """
        nouveau_id= self.new_id()
        self.get_id_node_map()[nouveau_id]= node(nouveau_id, label, {},{}) #nouveau noeud
        if parents != None:
            for parent in parents: #parcourir les parents à ajouter
                self.get_id_node_map()[nouveau_id].add_parent_id(parent, 1) #ajoute son parent avec multiplicité 1
                self.get_id_node_map()[parent].add_child_id(nouveau_id, 1)  # Mise à jour du parent

        if children != None:
            for child in children:#parcourir les enfants à ajouter
                self.get_id_node_map()[nouveau_id].add_child_id(child, 1) #ajoute son enfant avec multiplicité 1
                self.get_id_node_map()[child].add_parent_id(nouveau_id, 1)  # Mise à jour de l'enfant

        return nouveau_id

    
    def add_input_node(self, tgt):
        """Ajoute un nouveau noeud d'entrée qui pointe vers tgt"""
        if tgt not in self.get_id_node_map():
            raise ValueError("le noeud tgt n'existe pas")
    
        new_id = self.new_id()
        new_node = node(new_id, "", {}, {tgt: 1})  #  1 arête vers tgt
    
        self.get_id_node_map()[new_id] = new_node  # Ajout du nouveau noeud dans le graphe
        self.get_id_node_map()[tgt].add_parent_id(new_id, 1)  # ajout du nouveau parent de tgt
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
        parents = list(noeud.get_parents().keys())  # liste des parents
        for id_parent in parents: #supprime arête des parents des deux côtés
            self.remove_child_id(id_parent, id_noeud)
            self.remove_parent_id(id_noeud, id_parent)
        
        children = list(noeud.get_children().keys())  # liste des enfants
        for id_child in children: #supprime arête des enfants des deux côtés
            self.remove_parent_id(id_child, id_noeud)
            self.remove_child_id(id_noeud, id_child)
    
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
        for noeud_id in self.get_input_ids()+self.get_output_ids(): #chaque noeud d'input et output doit être dans le graphe
            noeud=self.get_node_by_id(noeud_id)
            if noeud.get_id() not in self.get_id_node_map():
                return False
        
        for noeud_id in self.get_input_ids():
            noeud=self.get_node_by_id(noeud_id)
            if len(noeud.get_children()) != 1 or len(noeud.get_parents()) != 0: #vérifie que les noeuds d'entrée ont un unique enfant et aucun parent
                return False
            for cle in noeud.get_children(): #vérifie que l'unique enfant est de multiplicité 1
                if noeud.get_children()[cle] != 1:
                    print(3)
                    return False
        
        for noeud_id in self.get_output_ids():
            noeud=self.get_node_by_id(noeud_id)
            if len(noeud.get_parents()) != 1 or len(noeud.get_children()) != 0: #vérifie que les noeuds de sortie ont un unique parent et aucun enfant
                return False
            for cle in noeud.get_parents(): #vérifie que l'unique parent est de multiplicité 1
                if noeud.get_parents()[cle] != 1:
                    return False
        
        for noeud_id in self.get_id_node_map(): #chaque clé de nodes pointe vers un noeud d'id la clé
            noeud=self.get_node_by_id(noeud_id)
            if noeud.get_id() != noeud_id : 
                return False
        
        for noeud_id in self.get_id_node_map(): #si j a pour fils i avec multiplicité m,  alors i  doit avoir pour parent j avec même multiplicité
            noeud=self.get_node_by_id(noeud_id)
            for fils_id in noeud.get_children():
                multiplicite=noeud.get_children()[fils_id] #regarde la multiplicité vers le fils
                fils=self.get_node_by_id(fils_id)
                if fils.get_parents()[noeud_id] != multiplicite: #regarde la multiplicité vers le parent
                    return False
            for parent_id in noeud.get_parents(): #si j a pour parent i avec multiplicité m, alors i doit avoir pour enfant j avec même multiplicité
                multiplicite=noeud.get_parents()[parent_id]
                parent=self.get_node_by_id(parent_id)
                if parent.get_children()[noeud_id] != multiplicite:
                    return False
        return True
    
    def random(self, n, bound, inputs = 0, outputs = 0, form = "free"):
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
           
    def association_ID(self): #inutile vu la manière dont on a codé new_id() (indices 0,1,2,3)
        dic = {}
        i = 0
        for id in self.get_id_node_map():
            dic[id] = i
            i = i + 1
        return dic
    
    def adjacency_matrix(self):
        N=len(self.get_nodes()) #nb noeuds
        matrice = [[0] * N for i in range(N)]
        
        for noeud_id in self.get_id_node_map():
            noeud=self.get_node_by_id(noeud_id)
            for enfant in noeud.get_children(): #un enfant est une arête
                multiplicite=noeud.get_children()[enfant]
                matrice[noeud_id][enfant]=multiplicite
        
        return matrice
        
        """version avec association_ID()
        id_map = self.association_ID()  # Associe les IDs des nœuds à des indices
        N = len(id_map)  
        matrice = [[0] * N for _ in range(N)]  # Initialise une matrice N x N remplie de 0
     
        for node_id, index in id_map.items():
            node = self.get_node_by_id(node_id)
            for child_id, multiplicity in node.get_children().items():
                matrice[index][id_map[child_id]] = multiplicity  # Remplit avec les multiplicités d'arêtes
     
        return matrice
        """

    def save_as_dot_file(self, path:str, verbose=False):
        with open(path, "w") as file:
            file.write("digraph G {\n")
            for node in self.nodes.values():
                file.write(f'\t{node.get_id()} [label="{node.get_label()}"{f", xlabel={node.get_id()}"*verbose}];\n')
            for node in self.nodes.values():
                for parent in node.get_parents():
                    file.write(f"\t{parent} -> {node.get_id()} ;\n")
            file.write("}")
        
    @classmethod
    def from_dot_file(cls, path:str):
        graph = cls.empty()
        dic = {}
        with open(path, "r") as file:
            lines = file.readlines()
        for line in lines[1:-1]:
            words = line.split()
            if words[1] != "->":
                n = node(int(words[0]), words[1].split('"')[1])
                dic[int(words[0])] = n
            else:
                dic[int(words[0])].add_child_id(int(words[2]), 1)
                dic[int(words[2])].add_parent_id(int(words[0]), 1)
        graph.nodes = {v.get_id(): v for v in dic.values()}
        graph.inputs = [node.get_id() for node in graph.nodes.values() if node.is_input]
        graph.outputs = [node.get_id() for node in graph.nodes.values() if node.is_output]
        return graph

    
    def display(self, verbose=False):
        self.save_as_dot_file("temp.dot",verbose)
        process = f"dot -Tpng temp.dot -o temp.png && open temp.png"
        os.system(process)


#---------------Matrices------------------------------------------

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

def graph_from_adjacency_matrix(matrice): 
    """ renvoi le multigraph represente par la matrice donnee en parametres, on laisse les attributs input et output vides"""
    G = open_digraph([], [], [])
    N=len(matrice)
    for i in range(N): 
        G.add_node(label="v"+str(i)) #une matrice de taille N a N noeuds
    for i in range(N):
        for j in range(N):
            if matrice[i][j] != 0:
                for _ in range (matrice[i][j]): #la multiplicité peut être >1
                    G.add_edge(i,j) #on a supposé que le noeud de ligne[i] a pour id i
    return G

def afficher_matrice(matrice):
    """Affiche une matrice"""
    for ligne in matrice:
        print(ligne)
    print()







        


        
            

        
            
    
    
    
        
    
        

    

    



