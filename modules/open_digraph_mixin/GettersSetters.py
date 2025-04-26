class MethodesGettersSetters:
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
   