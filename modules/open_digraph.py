class node:
    def __init__(self, identity, label, parents, children):
        '''
identity: int; its unique id in the graph
label: string;
parents: int->int dict; maps a parent node's id to its multiplicity, multiplicite: nb arrête entre 2 noeuds
children: int->int dict; maps a child node's id to its multiplicity
'''
        self.id= identity
        self.label=label
        self.parents=parents
        self.children=children
    
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
        self.inputs=inputs
        self.outputs=outputs
        self.nodes={node.id:node for node in nodes}
    
    def __str__(self):
        "Affichage dans la console"
        nodes_str = "\n  ".join(str(node) for node in self.nodes.values()) #affichage des noeuds
        return f"open_digraph(\nInputs: {self.inputs}, \nOutputs: {self.outputs}, \nNodes:\n  {nodes_str}\n)"
    
    def __repr__(self):
        """Affichage inductive du graphe"""
        return f"open_digraph({self.inputs}, {self.outputs}, {list(self.nodes.values())})"
    
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
    
    
        
    
        

    

