import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from node import *

class MethodesAjout:
    def new_id(self):
        """Renvoie un id non utilisé jusquà ce moment pour un nouveau noeud"""
        new_id = 0
        # Assurez-vous que get_id_node_map est disponible via MethodesGettersSetters
        while new_id in self.get_id_node_map(): 
            new_id += 1
        return new_id
   
    def add_edge(self, src, tgt):
        """Ajoute une arête du noeud src au noeud tgt"""
        # Assurez-vous que get_id_node_map et get_node_by_id sont disponibles
        if src in self.get_id_node_map() and tgt in self.get_id_node_map():
            src_node = self.get_node_by_id(src)
            tgt_node = self.get_node_by_id(tgt)
           
            if tgt in src_node.get_children():
                src_node.add_child_id(tgt, src_node.get_children()[tgt] + 1)
                tgt_node.add_parent_id(src, tgt_node.get_parents()[src] + 1)
            else:
                src_node.add_child_id(tgt, 1)
                tgt_node.add_parent_id(src, 1)
        else:
            raise ValueError("Vous avez donné des noeuds qui n existent pas")
       
    def add_edges(self, edges):
        """edges prend une liste de paires d ids de noeuds, et la méthode rajoute une arête entre chacune de ces paires"""
        for src, tgt in edges:
            self.add_edge(src, tgt)
    def add_node(self, label="", parents=None, children=None):
        """rajoute un noeud au graphe et le lie avec les noeuds d ids parent et children
        entrée: parents et children des listes """ 
        nouveau_id= self.new_id()
        # Assurez-vous que get_id_node_map est disponible
        self.get_id_node_map()[nouveau_id]= node(nouveau_id, label, {},{}) 
        if parents != None:
            for parent in parents:
                self.get_id_node_map()[nouveau_id].add_parent_id(parent, 1)
                self.get_id_node_map()[parent].add_child_id(nouveau_id, 1)

        if children != None:
            for child in children:
                self.get_id_node_map()[nouveau_id].add_child_id(child, 1)
                self.get_id_node_map()[child].add_parent_id(nouveau_id, 1)

        return nouveau_id

   
    def add_input_node(self, tgt):
        """Ajoute un nouveau noeud d entrée qui pointe vers tgt"""
        # Assurez-vous que get_id_node_map et add_input_id sont disponibles
        if tgt not in self.get_id_node_map():
            raise ValueError("le noeud tgt n existe pas")
   
        new_id = self.new_id()
        new_node = node(new_id, "", {}, {tgt: 1})
   
        self.get_id_node_map()[new_id] = new_node
        self.get_id_node_map()[tgt].add_parent_id(new_id, 1)
        self.add_input_id(new_id)
       
        return new_id
   
    def add_output_node(self, tgt):
        """Ajoute un nouveau noeud de sortie qui pointe vers tgt"""
        # Assurez-vous que get_id_node_map et add_output_id sont disponibles
        if tgt not in self.get_id_node_map():
            raise ValueError("le noeud tgt n existe pas")
   
        new_id = self.new_id()
        new_node = node(new_id, "", {tgt:1}, {})
   
        self.nodes[new_id] = new_node # self.nodes est get_id_node_map()
        self.nodes[tgt].add_child_id(new_id, 1)
        self.add_output_id(new_id)
       
        return new_id
