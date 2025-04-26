class MethodesSuppression:
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