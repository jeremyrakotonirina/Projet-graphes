class MethodesCircuitsBooleens:
    def min_id(self):
        """renvoie l'indice minimum des noeuds du graphe"""
        return min(self.get_id_node_map())
    
    def max_id(self):
        """renvoie l'indice maximum des noeuds du graphe"""
        return max(self.get_id_node_map())

    def shift_indices(self,n):
        """rajoute n à tous les indices du graphe"""
        old_to_new = {}
    
        for node in self.get_nodes():
            old_id = node.get_id()
            new_id = old_id + n
            old_to_new[old_id] = new_id
        
        for node in self.get_nodes():
            node.set_id(old_to_new[node.get_id()])  # change l'id lui-même

        for node in self.get_nodes():
            node.parents = {old_to_new[k]: v for k, v in node.parents.items()}
            node.children = {old_to_new[k]: v for k, v in node.children.items()}

        self.nodes = {old_to_new[old_id]: node for old_id, node in self.nodes.items()}

        self.inputs = [old_to_new[i] for i in self.inputs]
        self.outputs = [old_to_new[o] for o in self.outputs]
    
    def iparallel(self,g):
        """Ajoute un bool_circ g à self"""
        g2=g.copy()
        #éviter les conflits d'indices
        M = self.max_id()
        m = g2.min_id()
        shift = M - m + 1
        g2.shift_indices(shift)

        self.inputs += g2.inputs
        self.outputs += g2.outputs

        for noeud in g2.get_nodes():
            self.nodes[noeud.get_id()]=noeud
    
    def parallel(self, g):
        """renvoie un nouveau graphe qui est la composition parallèle des deux graphes en paramètre"""
        g2=self.copy()
        g2.iparallel(g)
        return g2
    
    def icompose(self, f):
        """fait la composition séquentielle de self et f"""

        if len(self.get_input_ids()) != len(f.get_output_ids()):
            raise ValueError("Le nombre de sorties de f doit correspondre au nombre d’entrées de self.")
        g=f.copy()

        shift = self.max_id() - g.min_id() + 1
        g.shift_indices(shift) #décalage des indices

        for noeud in g.get_nodes():
            self.nodes[noeud.get_id()]=noeud

        for i in range(len(g.get_output_ids())):
            self.add_edge(g.get_output_ids()[i], self.get_input_ids()[i])
        
        self.set_inputs(g.get_input_ids())
    
    def compose(self, g):
        """renvoie un graphe qui est la composée séquentielle des deux graphes en paramètre"""
        g2=self.copy()
        g2.icompose(g)
        return g2
    
    
    
    def connected_components(self):
        """
        Renvoie un tuple (nb_composantes, dict_id_to_comp)
        - nb_composantes : int, nombre de composantes connexes
        - dict_id_to_comp : dict, associe chaque id à une composante
        """
        seen = set()
        comp_dict = {}
        comp_id = 0

        for node in self.get_nodes():
            nid = node.get_id()
            if nid not in seen:
                # parcourir les composante connexe
                stack = [nid]
                while stack:
                    current = stack.pop()
                    if current not in seen:
                        seen.add(current)
                        comp_dict[current] = comp_id
                        node = self.get_node_by_id(current)
                        voisins = list(node.get_children()) + list(node.get_parents())
                        stack.extend(voisins)
                comp_id += 1

        return comp_id, comp_dict

    def connected_components_subgraphs(self):
        """
        Renvoie une liste d'open_digraph correspondant aux composantes connexes.
        """
        a , comp_dict = self.connected_components()

        # Regroupement des noeuds par composante
        comp_to_ids = {}
        for nid, cid in comp_dict.items():
            if cid not in comp_to_ids:
                comp_to_ids[cid]=[]
            comp_to_ids[cid].append(nid)

        subgraphs = []
        for ids in comp_to_ids.values():
            # On extrait les noeuds de la composante
            nodes = [self.get_node_by_id(i).copy() for i in ids]

            # On corrige les parents/enfants pour ne garder que ceux dans la composante
            for node in nodes:
                node.parents = {i: w for i, w in node.parents.items() if i in ids}
                node.children = {i: w for i, w in node.children.items() if i in ids}

            # On filtre les inputs/outputs
            inputs = [i for i in self.inputs if i in ids]
            outputs = [o for o in self.outputs if o in ids]

            subgraphs.append(self.__class__(inputs, outputs, nodes))

        return subgraphs