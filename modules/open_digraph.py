class node:
    def __init__(self, identity, label, parents, children):
        '''
identity: int; its unique id in the graph
label: string;
parents: int->int dict; maps a parent node's id to its multiplicity
children: int->int dict; maps a child node's id to its multiplicity
'''
        self.id= identity
        self.label=label
        self.parents=parents
        self.children=children
    
    def __str__(self):
        print("Identité: /n", self.id, "label: /n", self.label)
        #print ("Noeuds parents: /n") j'y arrive pas

        

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
        print ("Noeuds d'entrée: /n")
        for i in self.inputs:
            print(i)
        print ("Noeuds de sortie: /n")
        for i in self.outputs:
            print(i)
        print("Noeuds du graphe: /n")
        for i in self.nodes:
            print(self.nodes[i])