
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
        """retourne l'id du noeud"""
        return self.id
   
    def get_label(self):
        """retourne le label du noeud"""
        return self.label
   
    def get_parents(self):
        """retourne un dictionnaire avec clé id des parents et valeur multiplicité"""
        return self.parents
   
    def get_children(self):
        """retourne un dictionnaire avec clé id des enfants et valeur multiplicité"""
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
    
    def indegree(self):
        "renvoie le degré entrant du noeud"
        res=0
        for i in self.get_parents():
            res += self.get_parents()[i]
        return res
    
    def outdegree(self):
        "renvoie le degré sortant du noeud"
        res=0
        for i in self.get_children():
            res += self.get_children()[i]
        return res
    
    def degree(self):
        "renvoie le degré total du noeud"
        return self.indegree() + self.outdegree()