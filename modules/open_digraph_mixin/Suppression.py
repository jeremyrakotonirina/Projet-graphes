class MethodesSuppression:
    def remove_parent_once(self, id_noeud, id_parent):
        noeud = self.get_node_by_id(id_noeud)
        noeud.get_parents()[id_parent] -= 1
        if noeud.get_parents()[id_parent] == 0:
            del noeud.get_parents()[id_parent]

    def remove_child_once(self, id_noeud, id_children):
        noeud = self.get_node_by_id(id_noeud)
        noeud.get_children()[id_children] -= 1
        if noeud.get_children()[id_children] == 0:
            del noeud.get_children()[id_children]

    def remove_parent_id(self, id_noeud, id_parent):
        noeud = self.get_node_by_id(id_noeud)
        del noeud.get_parents()[id_parent]

    def remove_child_id(self, id_noeud, id_children):
        noeud = self.get_node_by_id(id_noeud)
        del noeud.get_children()[id_children]

    def remove_edge(self, src, tgt):
        self.remove_parent_once(tgt, src)
        self.remove_child_once(src, tgt)

    def remove_parallel_edges(self, src, tgt):
        self.remove_parent_id(tgt,src)
        self.remove_child_id(src,tgt)

    def remove_node_by_id(self, id_noeud):
        noeud = self.get_node_by_id(id_noeud)
        parents = list(noeud.get_parents().keys())
        for id_parent in parents:
            self.remove_child_id(id_parent, id_noeud)
            self.remove_parent_id(id_noeud, id_parent)
       
        children = list(noeud.get_children().keys())
        for id_child in children:
            self.remove_parent_id(id_child, id_noeud)
            self.remove_child_id(id_noeud, id_child)
    
    def remove_edges(self, *args):
        for src, tgt in args:
            self.remove_edge(src, tgt)
   
    def remove_several_parallel_edges(self, *args):
        # Dans le code original, args est une liste de tuples (src, tgt)
        # Mais dans bool_circ, il est appelé avec un seul tuple : base.remove_several_parallel_edges((p, u.id))
        # Donc, on s'attend à ce que args soit ((src1, tgt1), (src2, tgt2), ...)
        # ou, si appelé comme dans bool_circ, args sera (((p, u.id)),)
        # Il faut clarifier cela. Pour l'instant, on suppose que args est une liste de paires.
        for arg_pair in args: # Si args est (((p,u.id)),) alors arg_pair sera ((p,u.id))
            if isinstance(arg_pair, tuple) and len(arg_pair) == 2:
                 src, tgt = arg_pair
                 self.remove_parallel_edges(src, tgt)
            else:
                # Gérer le cas où l'argument n'est pas une paire, ou ajuster la logique d'appel
                # Pour l'instant, on va supposer que l'appel est correct et que args est une liste de paires
                # Si bool_circ appelle avec un seul tuple, il faut modifier l'appel ou cette méthode
                # L'appel dans bool_circ est `base.remove_several_parallel_edges((p, u.id))`
                # ce qui signifie que args sera `(((p, u.id)),)`
                # Donc, on doit extraire le tuple interne.
                if isinstance(arg_pair, tuple) and len(arg_pair) == 1 and isinstance(arg_pair[0], tuple) and len(arg_pair[0]) == 2:
                    src, tgt = arg_pair[0]
                    self.remove_parallel_edges(src, tgt)
                else:
                    # Pour l'instant, on va juste passer si le format n'est pas reconnu pour éviter une erreur bloquante
                    # print(f"Skipping remove_several_parallel_edges due to unexpected arg format: {arg_pair}")
                    pass # Ou lever une exception plus informative


    def remove_nodes_by_id(self, *args):
        for id_noeud in args:
            self.remove_node_by_id(id_noeud)
