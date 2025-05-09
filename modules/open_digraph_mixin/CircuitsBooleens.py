from node import node

class MethodesCircuitsBooleens:
    def min_id(self):
        """renvoie l'indice minimum des noeuds du graphe"""
        return min(self.get_id_node_map())
    
    def max_id(self):
        """renvoie l'indice maximum des noeuds du graphe"""
        return max(self.get_id_node_map())

    def shift_indices(self,n):
        """rajoute n à tous les indices du graphe"""
        ancien_nouveau = {}
    
        for node_obj in self.get_nodes(): # Renommé 'node' en 'node_obj' pour éviter conflit avec la classe 'node'
            old_id = node_obj.get_id()
            new_id = old_id + n
            ancien_nouveau[old_id] = new_id
        
        for node_obj in self.get_nodes():
            node_obj.set_id(ancien_nouveau[node_obj.get_id()])

        for node_obj in self.get_nodes():
            node_obj.parents = {ancien_nouveau[k]: v for k, v in node_obj.parents.items()}
            node_obj.children = {ancien_nouveau[k]: v for k, v in node_obj.children.items()}

        self.nodes = {ancien_nouveau[old_id]: node_obj for old_id, node_obj in self.nodes.items()}

        self.inputs = [ancien_nouveau[i] for i in self.inputs]
        self.outputs = [ancien_nouveau[o] for o in self.outputs]
    
    def iparallel(self,g):
        """Ajoute un bool_circ g à self"""
        g2=g.copy()
        if self.nodes: 
            M = self.max_id()
            m = g2.min_id() 
            if not g2.nodes:
                 shift = 0 
            else:
                 shift = M - m + 1
                 if shift < (M +1) and M > 0 and m < 0 : # Cas où M est grand positif et m petit négatif
                    shift = M + abs(m) +1 
                 elif shift <=0 and M > 0: 
                    shift = M +1

        else: # self est vide
            shift = 0 # Pa
        
        if shift != 0 and g2.nodes: 
            g2.shift_indices(shift)

        self.inputs += g2.inputs
        self.outputs += g2.outputs

        for noeud in g2.get_nodes():
            self.nodes[noeud.get_id()]=noeud
    
    def parallel(self, g2_orig): # g2_orig est le graphe 'g' de l'ancienne signature
        """renvoie un nouveau graphe qui est la composition parallèle des deux graphes en paramètre"""
        from open_digraph import open_digraph as OD_Class

        g1_nodes_copies = {nid: n.copy() for nid, n in self.nodes.items()}
        g1_inputs_copies = self.inputs.copy()
        g1_outputs_copies = self.outputs.copy()

        g2 = g2_orig.copy()

        offset = 0
        if self.nodes:
            offset = self.max_id() + 1
        
        g2_id_map = {}
        temp_g2_nodes_for_merging = {}
        for old_nid_g2, n_g2_orig in g2.nodes.items():
            new_nid_g2 = old_nid_g2 + offset
            g2_id_map[old_nid_g2] = new_nid_g2
            temp_g2_nodes_for_merging[new_nid_g2] = node(new_nid_g2, n_g2_orig.get_label(), {}, {})

        for old_nid_g2, n_g2_orig in g2.nodes.items():
            new_src_id_g2 = g2_id_map[old_nid_g2]
            src_node_in_merged_g2_part = temp_g2_nodes_for_merging[new_src_id_g2]
            for old_child_id_g2, mult in n_g2_orig.get_children().items():
                new_child_id_g2 = g2_id_map[old_child_id_g2]
                child_node_in_merged_g2_part = temp_g2_nodes_for_merging[new_child_id_g2]
                src_node_in_merged_g2_part.add_child_id(new_child_id_g2, mult)
                child_node_in_merged_g2_part.add_parent_id(new_src_id_g2, mult)
        
        final_merged_nodes_dict = {**g1_nodes_copies, **temp_g2_nodes_for_merging}
        final_merged_inputs = g1_inputs_copies + [g2_id_map[old_id] for old_id in g2.inputs]
        final_merged_outputs = g1_outputs_copies + [g2_id_map[old_id] for old_id in g2.outputs]

        merged_od_instance = OD_Class(final_merged_inputs, final_merged_outputs, list(final_merged_nodes_dict.values()))
        
        return merged_od_instance
    
    def icompose(self, f):
        """fait la composition séquentielle de self et f"""
        if len(self.get_input_ids()) != len(f.get_output_ids()):
            raise ValueError("Le nombre de sorties de f doit correspondre au nombre d’entrées de self.")
        g=f.copy()

        # S'assurer que self.nodes n'est pas vide avant d'appeler max_id
        if self.nodes and g.nodes:
            shift = self.max_id() - g.min_id() + 1
            if shift < (self.max_id() +1) and self.max_id() >0 and g.min_id() <0:
                 shift = self.max_id() + abs(g.min_id()) + 1
            elif shift <=0 and self.max_id() >0:
                 shift = self.max_id() +1
            g.shift_indices(shift)
        elif not self.nodes:
            pass # g ne doit pas être décalé si self est vide
        else: # g est vide, pas de décalage
            pass 

        for noeud in g.get_nodes():
            self.nodes[noeud.get_id()]=noeud

        # S'assurer que les IDs existent avant d'ajouter une arête
        for i in range(len(g.get_output_ids())):
            g_out_id = g.get_output_ids()[i]
            self_in_id = self.get_input_ids()[i]
            if g_out_id in self.nodes and self_in_id in self.nodes:
                 self.add_edge(g_out_id, self_in_id)
            # else: Gérer le cas où un ID n'est pas trouvé, peut-être lever une exception
        
        self.set_input_ids(g.get_input_ids())
    
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

        for node_obj in self.get_nodes(): # Renommé 'node' en 'node_obj'
            nid = node_obj.get_id()
            if nid not in seen:
                stack = [nid]
                while stack:
                    current = stack.pop()
                    if current not in seen:
                        seen.add(current)
                        comp_dict[current] = comp_id
                        # Récupérer le noeud actuel du graphe self
                        current_node_obj = self.get_node_by_id(current)
                        voisins = list(current_node_obj.get_children()) + list(current_node_obj.get_parents())
                        stack.extend(voisins)
                comp_id += 1

        return comp_id, comp_dict

    def connected_components_subgraphs(self):
        """
        Renvoie une liste d'open_digraph correspondant aux composantes connexes.
        """
        num_components , comp_dict = self.connected_components()

        comp_to_ids = {}
        for nid, cid in comp_dict.items():
            if cid not in comp_to_ids:
                comp_to_ids[cid]=[]
            comp_to_ids[cid].append(nid)

        subgraphs = []
        for ids_in_comp in comp_to_ids.values(): # Renommé 'ids' en 'ids_in_comp'
            component_nodes = [self.get_node_by_id(i).copy() for i in ids_in_comp]

            for node_obj in component_nodes: # Renommé 'node' en 'node_obj'
                node_obj.parents = {i: w for i, w in node_obj.parents.items() if i in ids_in_comp}
                node_obj.children = {i: w for i, w in node_obj.children.items() if i in ids_in_comp}

            component_inputs = [i for i in self.inputs if i in ids_in_comp]
            component_outputs = [o for o in self.outputs if o in ids_in_comp]
            
            # Utiliser OD_Class pour créer un open_digraph de base si self.__class__ n'est pas défini ici
            # ou si on veut explicitement un open_digraph. Mais self.__class__ est plus général.
            from open_digraph import open_digraph as OD_Class
            base_subgraph_od = OD_Class(component_inputs, component_outputs, component_nodes)
            if self.__class__ is OD_Class:
                subgraphs.append(base_subgraph_od)
            else:
                subgraphs.append(self.__class__(base_subgraph_od))

        return subgraphs

