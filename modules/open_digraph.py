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
        """Ajoute une arête du noeud src au noeud tgt"""
        if (src in self.get_id_node_map() and tgt in self.get_id_node_map()):  #vérifier qu'ils existent
            self.nodes[src].add_child_id(tgt, 1)
            self.nodes[tgt].add_parent_id(src, 1)
        else :
            raise ValueError ("Vous avez donné des noeuds qui n'existent pas")
        
    def add_edges(self, edges):
        """edges prend une liste de paires d'ids de noeuds, et la méthode rajoute une arête entre chacune de ces paires"""
        for src, tgt in edges:
            self.add_edge(src, tgt)
    
    def add_node(self, label='', parents=None, children=None):
        """rajoute un noeud au graphe"""
        nouveau_id= self.new_id()
        if parents==None:
            parents={}
        if children==None:
            children={}
        self.get_id_node_map[nouveau_id]= node(nouveau_id, label, {parents:})

    
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
                return false
        
        for noeud in self.get_input_ids():
            if len(noeud.get_children()) != 1 or len(noeud.get_parents()) != 0: #vérifie que les noeuds d'entrée ont un unique enfant et aucun parent
                return false
            for cle in noeud.get_children(): #vérifie que l'unique enfant est de multiplicité 1
                if noeud.get_children()[cle] != 1:
                    return false
        
        for noeud in self.get_output_ids():
            if len(noeud.get_parents()) != 1 or len(noeud.get_children()) != 0: #vérifie que les noeuds de sortie ont un unique parent et aucun enfant
                return false
            for cle in noeud.get_parents(): #vérifie que l'unique parent est de multiplicité 1
                if noeud.get_parents()[cle] != 1:
                    return false
        
        for noeud_id in noeud.get_id_node_map(): #chaque clé de nodes pointe vers un noeud d'id la clé
            noeud=noeud.get_id_node_map()[noeud_id]
            if noeud.get_id() != noeud_id : 
                return false
        
        for noeud_id in self.get_id_node_map():
            noeud=noeud.get_id_node_map()[noeud_id]
            for fils in noeud.get_children():
                multiplicite=noeud.get_children()[fils]


        


        
            

        
            
    
    
    
        
    
        

    

    



