import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #permet d'importer node.py

from node import *


class MethodesGettersSetters:
    #---------------------------getter--------------------------
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
        return list(self.nodes.values())
   
    def get_node_by_id(self, id):
        """renvoie le noeud d'id ID"""
        return self.nodes[id]
   
    def get_nodes_by_ids(self, ids):
        """renvoie une liste de noeuds à partir d'une liste d'ids"""
        return [self.nodes[id] for id in ids]
   
    def get_node_ids(self):
        """renvoie l'ID du noeud n"""
        return list(self.nodes.keys())
   #-----------------------------setter-----------------------------------
    def set_input_ids(self, inputs):
        """Remplace la liste des entrées"""
        self.inputs = inputs
   
    def set_output_ids(self, outputs):
        """Remplace la liste des sorties"""
        self.outputs = outputs
   
    def add_input_id(self, id):
        """Ajoute un nouvel id dans la liste des entrées"""
        self.inputs.append(id)
   
    def add_output_id(self, id):
        """Ajoute un nouvel id dans la liste des sorties"""
        self.outputs.append(id)
