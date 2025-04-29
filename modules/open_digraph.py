import random
import sys
import os
import matplotlib.colors as mcolors

sys.path.append(os.path.dirname(__file__))  
from FonctionsMatrices import *
from node import *

#Mixing
from open_digraph_mixin.GettersSetters import MethodesGettersSetters
from open_digraph_mixin.Ajout import MethodesAjout
from open_digraph_mixin.Suppression import MethodesSuppression
from open_digraph_mixin.Image import MethodesImage
from open_digraph_mixin.CircuitsBooleens import MethodesCircuitsBooleens
from open_digraph_mixin.Chemins import MethodesChemins





# Liste de toutes les couleurs X11 depuis matplotlib
x11_colors = list(mcolors.CSS4_COLORS.keys())
x11_colors_taille = len(x11_colors)
        

class open_digraph(MethodesGettersSetters, MethodesAjout, MethodesSuppression, 
                   MethodesImage, MethodesCircuitsBooleens, MethodesChemins ):

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
    

    #-------------------Génération de graphes----------------------
    @classmethod
    def empty(cls):
        """Crée et retourne un graphe vide"""
        return cls([],[],[])
    
    @classmethod
    def identity(cls, n):
        """crée un open_digraph représentant l'identité sur n fils"""
        nodes = []
        input_ids = []
        output_ids = []

        for i in range(n):
        # chaque lien est juste : i (entrée) → i+n (sortie)
            in_id = i
            out_id = i + n
            input_ids.append(in_id)
            output_ids.append(out_id)
            nodes.append(node(in_id, "", {}, {out_id: 1}))
            nodes.append(node(out_id, "", {in_id: 1}, {}))

        return open_digraph(input_ids, output_ids, nodes)
   
    def copy(self):
        """Retourne une copie du graphe"""
        return open_digraph( self.inputs.copy(), self.outputs.copy(),
            [noeud.copy() for noeud in self.nodes.values()]
        )
    
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
    
    #-----------------------------------------------------------
    
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

    
    def adjacency_matrix(self):
        N=len(self.get_nodes()) #nb noeuds
        matrice = [[0] * N for i in range(N)]
    
        for noeud_id in self.get_id_node_map():
            noeud=self.get_node_by_id(noeud_id)
            for enfant in noeud.get_children(): #un enfant est une arête
                multiplicite=noeud.get_children()[enfant]
                matrice[noeud_id][enfant]=multiplicite
    
        return matrice
    
    def fusion_nodes(self, id1, id2, label_mode="id1"):
        node1=self.get_node_by_id(id1)
        node2=self.get_node_by_id(id2)

        if label_mode == "id1": #choix du label
            label=node1.get_label()
        else:
            label=node2.get_label()
        
        #on relie les éléments de node 2 vers node 1
        parents_copy = dict(node2.get_parents())
        for pid, mult in parents_copy.items():
            self.get_node_by_id(pid).add_child_id(id1, mult)
            node1.add_parent_id(pid, mult)

        children_copy = dict(node2.get_children())
        for cid, mult in children_copy.items():
            self.get_node_by_id(cid).add_parent_id(id1, mult)
            node1.add_child_id(cid, mult)
        
        #supprimer node 2
        self.remove_node_by_id(id2) #enlève juste les arêtes
        del self.nodes[id2]
        if id2 in self.inputs:
            self.inputs.remove(id2)
        elif id2 in self.outputs:
            self.outputs.remove(id2)
        
        node1.set_label(label) #mise à jour label

    
    
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



