import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from node import *


#liste couleures spécifiques
couleurs_specifiques = [
    "red", "blue", "green","orange", "purple", "brown", "gray","yellow", "cyan", "magenta","black"
]
couleurs_specifiques_taille = len(couleurs_specifiques)

class MethodesImage:
    def save_as_dot_file(self, path: str, verbose=False):
        with open(path, "w") as file:
            file.write("digraph G {\n")
            
            for node in self.nodes.values():
                nid = node.get_id()
                label = node.get_label()

                # Détermine le style du nœud
                if nid in self.get_input_ids():
                    file.write(f'\t{nid} [label="{label}", style=filled, fillcolor=lightblue];\n')
                elif nid in self.get_output_ids():
                    file.write(f'\t{nid} [label="{label}", style=filled, fillcolor=lightcoral];\n')
                else:
                    file.write(f'\t{nid} [label="{label}"];\n')

            index_couleur = 0
            for node in self.nodes.values():
                col = couleurs_specifiques[index_couleur % couleurs_specifiques_taille]
                for child_id, multiplicite in node.get_children().items():
                    for i in range(multiplicite):
                        file.write(f"\t{node.get_id()} -> {child_id} [color={col} minlen={i+1}];\n")
                index_couleur += 1
            file.write("}\n")

    @classmethod
    def from_dot_file(cls, path: str):
        graph = cls.empty()
        dic = {}
        edges = []

        with open(path, "r") as file:
            lines = [line.strip() for line in file if line.strip()]

        # Étape 1 : Créer tous les nœuds
        for line in lines[1:-1]:  # On ignore "digraph G {" et "}"
            if "->" not in line:
                # Exemple : 7 [label="x1"];
                parts = line.split("[label=")
                node_id = int(parts[0].strip())
                label = parts[1].strip().strip('";[]')
                dic[node_id] = node(node_id, label, {}, {})

        # Étape 2 : Ajouter les arcs
        for line in lines[1:-1]:
            if "->" in line:
                # Exemple : 7 -> 6 [color=blue minlen=1];
                parts = line.split()
                src = int(parts[0])
                tgt = int(parts[2])
                dic[src].add_child_id(tgt)
                dic[tgt].add_parent_id(src)

        graph.nodes = dic
        graph.inputs = [n.get_id() for n in dic.values() if not n.get_parents()]
        graph.outputs = [n.get_id() for n in dic.values() if not n.get_children()]
        return graph

    
    def display(self, verbose=False):
        import os #pour le display du noeud
        self.save_as_dot_file("temp.dot",verbose)
        process = f"dot -Tpng temp.dot -o temp.png && start temp.png" #remplacer open par start sur windows
        os.system(process)