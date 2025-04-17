import random
import sys
import os
sys.path.append(os.path.dirname(__file__))  
from matrices import *
from node import *

import matplotlib.colors as mcolors

# Liste de toutes les couleurs X11 depuis matplotlib
x11_colors = list(mcolors.CSS4_COLORS.keys())
x11_colors_taille = len(x11_colors)


#liste couleures spécifiques
couleurs_specifiques = [
    "red", "blue", "green","orange", "purple", "brown", "gray", "white","yellow", "cyan", "magenta",
]
couleurs_specifiques_taille = len(couleurs_specifiques)
        

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
        """renvoie les id des inputs nodes"""
        return self.inputs
   
    def get_output_ids(self):
        """renvoie les id des outputs nodes"""
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
        """Retire les arêtes associées à un noeud, ainsi que le noeud"""
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
   
    #----------------------------------Prédicats-----------

    def is_well_formed(self):
        """Vérifie qu'un graphe est toujours bien formé"""
        for noeud_id in self.get_input_ids()+self.get_output_ids(): #chaque noeud d'input et output doit être dans le graphe
            noeud=self.get_node_by_id(noeud_id)
            if noeud.get_id() not in self.get_id_node_map():
                raise Exception("un noeud input ou output n'est pas dans le graphe")
       
        for noeud_id in self.get_input_ids():
            noeud=self.get_node_by_id(noeud_id)
           
            if len(noeud.get_children()) != 1 or len(noeud.get_parents()) != 0: #vérifie que les noeuds d'entrée ont un unique enfant et aucun parent
                raise Exception("noeud d'entrée n'ont pas un unique enfant et/ou aucun parent")
            for cle in noeud.get_children(): #vérifie que l'unique enfant est de multiplicité 1
                if noeud.get_children()[cle] != 1:
                   raise Exception("l'unique enfant n'est pas de multiplicité 1")
       
        for noeud_id in self.get_output_ids():
            noeud=self.get_node_by_id(noeud_id)
            if len(noeud.get_parents()) != 1 or len(noeud.get_children()) != 0: #vérifie que les noeuds de sortie ont un unique parent et aucun enfant
                raise Exception("noeud de sortie n'ont pas un unique parent et/ou aucun enfant")
            for cle in noeud.get_parents(): #vérifie que l'unique parent est de multiplicité 1
                if noeud.get_parents()[cle] != 1:
                    raise Exception("l'unique parent n'est pas de multiplicité 1")
       
        for noeud_id in self.get_id_node_map(): #chaque clé de nodes pointe vers un noeud d'id la clé
            noeud=self.get_node_by_id(noeud_id)
            if noeud.get_id() != noeud_id :
                raise Exception("clé de nodes ne pointe pas vers un noeud d'id la clé")
       
        for noeud_id in self.get_id_node_map(): #si j a pour fils i avec multiplicité m,  alors i  doit avoir pour parent j avec même multiplicité
            noeud=self.get_node_by_id(noeud_id)
            for fils_id in noeud.get_children():
                multiplicite=noeud.get_children()[fils_id] #regarde la multiplicité vers le fils
                fils=self.get_node_by_id(fils_id)
                if fils.get_parents()[noeud_id] != multiplicite: #regarde la multiplicité vers le parent
                    raise Exception("un noeud n'a pas la même multiplicité vers son parent, que son parent n'a vers ce noeud")
            for parent_id in noeud.get_parents(): #si j a pour parent i avec multiplicité m, alors i doit avoir pour enfant j avec même multiplicité
                multiplicite=noeud.get_parents()[parent_id]
                parent=self.get_node_by_id(parent_id)
                if parent.get_children()[noeud_id] != multiplicite:
                    raise Exception("un noeud n'a pas la même multiplicité vers son enfant, que son enfant n'a vers ce noeud")
        return True

   #-------------------------------------------------------

    def random(self, n, bound, inputs = 0, outputs = 0, form = "free"):
        """ génère un graphe formé de n noeuds internes, inputs désigne le nb
        de inputs et outputs le nombre de outputs
        le nb d'arretes est aleatoire avec des valeurs entre 0 et bound inclus,  on peut décider le graphe que l'on veut avec le parametre form
            valeurs possibles pour form :   free       --
                                            DAG        --  
                                            oriented   --
                                            undirected --
                                            loop-free  --  
        """
       
        if form == "free":
            graphe = graph_from_adjacency_matrix(random_int_matrix(n, bound, False))
        elif form == "DAG":
            graphe = graph_from_adjacency_matrix(random_triangular_int_matrix(n, bound, False))
        elif form == "oriented":
            graphe = graph_from_adjacency_matrix(random_oriented_int_matrix(n, bound, False))
        elif form == "undirected":
            graphe = graph_from_adjacency_matrix(random_symetric_int_matrix(n, bound, False))
        elif form == "loop-free":
            graphe = graph_from_adjacency_matrix(random_int_matrix(n, bound, True))
        elif form == "loop-free DAG":
            graphe = graph_from_adjacency_matrix(random_triangular_int_matrix(n, bound, True))
        elif form == "loop-free oriented":
            graphe = graph_from_adjacency_matrix(random_oriented_int_matrix(n, bound, True))
        elif form == "loop-free undirected":
            graphe = graph_from_adjacency_matrix(random_symetric_int_matrix(n, bound, True))
        else:
            raise ValueError(" Le paramètre form est mal donné, regarder la documentation pour plus d'info sur le paramètre ")
       
        id_noeuds=graphe.get_id_node_map().keys() #liste d'id de tous les noeuds
        id_entrees=random.sample(list(id_noeuds), k=inputs) #séléctionne k éléments de id_noeuds sans répétition
        id_sorties=random.sample(list(id_noeuds), k=outputs)

        for i in id_entrees:
            graphe.add_input_node(i)
       
        for i in id_sorties:
            graphe.add_output_node(i)
           
        graphe.is_well_formed() #vérifie que graphe bien formé
        return graphe
           

    def adjacency_matrix(self):
        N=len(self.get_nodes()) #nb noeuds
        matrice = [[0] * N for i in range(N)]
       
        for noeud_id in self.get_id_node_map():
            noeud=self.get_node_by_id(noeud_id)
            for enfant in noeud.get_children(): #un enfant est une arête
                multiplicite=noeud.get_children()[enfant]
                matrice[noeud_id][enfant]=multiplicite
       
        return matrice
       
    #----------------Conversion en image------------------------------------

    def save_as_dot_file(self, path:str, verbose=False):
        with open(path, "w") as file:
            file.write("digraph G {\n")
            for node in self.nodes.values():
                if(verbose):
                    file.write(f'\t{node.get_id()} [label="{node.get_label()}, {node.get_id()}"];\n')
                else:
                    file.write(f'\t{node.get_id()};\n')
            index_couleur = 0
            for node in self.nodes.values():
                col = couleurs_specifiques[index_couleur]
                for children,multiplicite in node.get_children().items():
                    for i in range(multiplicite):
                        #col = ["red", "blue", "green", "aqua", "brown", "darkmagenta"][i % 3]
                        #col = x11_colors[i%x11_colors_taille]
                        file.write(f"\t{node.get_id()} -> {children} [color={col} minlen={i+1}];\n") #afin de differencier les arretes on leur atribue une couleur dependant de leur parent
                index_couleur +=1
            file.write("}")

        
    @classmethod
    def from_dot_file(self, path:str):
        graph = self.empty()
        dic = {}
        with open(path, "r") as file:
            lines = lignes_sans_v = [ligne.strip() for ligne in file]  #recupère toutes les lignes
        i = 1
        fin = len(lines)-1
        print(fin)
        while i < fin:
            print("i=",i)
            words = lines[i].split()
            if len(words) == 1:
                n = node(int(words[0].strip(';')), "", {}, {})
                dic[int(words[0].strip(';'))] = n
            elif words[1] != "->":
                n = node(int(words[0].strip(';')), "label",{},{})
                dic[int(words[0].strip(';'))] = n
            else:
                multiplicite = 1
                words_S = lines[i+1].split()
                #while(i + 1 < len(lines) and lines[i + 1].split()[0] == words[0] and lines[i + 1].split()[2] == words[2]):
                #while(words_S[0] == words[0] and words_S[2] == words[2]):
                while(i + 1 < len(lines) and lines[i+1].split()[0] == words[0] and lines[i+1].split()[2] == words[2]):
                    multiplicite += 1
                    words_S = lines[i+1].split()
                    i += 1
                for i in range(multiplicite):
                    print(multiplicite)
                    dic[int(words[0].strip(';'))].add_child_id(int(words[2].strip(';')), multiplicite)
                    print(dic[int(words[0].strip(';'))])
                    dic[int(words[2].strip(';'))].add_parent_id(int(words[0].strip(';')), multiplicite)
            i+=1
        """
        i = 1
        while i < len(lines)-1:
            words = lines[i].split()
            if words[1] != "->":
                n = node(int(words[0]), words[1].split('"')[1],{},{})
                dic[int(words[0])] = n
                i += 1
            else:
                multiplicite = 1
                words_S = lines[i+1].split()
                while(i + 1 < len(lines) and lines[i + 1].split()[0] == words[0] and lines[i + 1].split()[2] == words[2]):
                    multiplicite += 1
                    i += 1
                dic[int(words[0])].add_child_id(int(words[2]), multiplicite)
                dic[int(words[2])].add_parent_id(int(words[0]), multiplicite)
                i += 1
        """
        graph.nodes = dic
        print(dic)
        """for n in dic.values():
            for p in n.get_parents().keys():
                graph.add_edge(n.get_id(), p)
            for c in n.get_children().keys():
                graph.add_edge(n.get_id(), c)"""
        # faut coder la partie du input et output
        #graph.inputs = 
        #graph.outputs = 
        return graph

    
    def display(self, verbose=False):
        import os #pour le display du noeud
        self.save_as_dot_file("temp.dot",verbose)
        process = f"dot -Tpng temp.dot -o temp.png && open temp.png" #remplacer open par start sur windows
        os.system(process)


def graph_from_adjacency_matrix(matrice):
    """ renvoi le graphe represente par la matrice donnee en parametres"""
    G = open_digraph([], [], [])
    N=len(matrice)
    for i in range(N):
        G.add_node(label="v"+str(i)) #une matrice de taille N a N noeuds
    for i in range(N):
        for j in range(N):
            if matrice[i][j] != 0:
                for _ in range (matrice[i][j]): #la multiplicité peut être >1
                    G.add_edge(i,j) #on a supposé que le noeud de ligne[i] a pour id i
    for i in range(N):
        ligne = matrice[i]
        colonne = [matrice[j][i] for j in range(N)]
        if all(x == 0 for x in ligne) and colonne.count(1) == 1 and sum(colonne) == 1:
            # Aucun enfant mais 1 parent => output node
            G.add_output_id(i)
        elif all(x == 0 for x in colonne) and ligne.count(1) == 1 and sum(ligne) == 1:
            # Aucun parent mais 1 enfants => input node
            G.add_input_id(i)
    return G

