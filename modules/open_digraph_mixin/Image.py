import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from node import *


#liste couleures spécifiques
couleurs_specifiques = [
    "red", "blue", "green","orange", "purple", "brown", "gray", "white","yellow", "cyan", "magenta",
]
couleurs_specifiques_taille = len(couleurs_specifiques)

class MethodesImage:
    def save_as_dot_file(self, path:str, verbose=False):
        with open(path, "w") as file:
            file.write("digraph G {\n")
            for node in self.nodes.values():
                if(verbose):
                    file.write(f'\t{node.get_id()} [label="{node.get_label()}, {node.get_id()}"];\n')
                else:
                    file.write(f'\t{node.get_id()};\n')
            index_couleur = 0
            for node in self.nodes.values():
                col = couleurs_specifiques[index_couleur]
                for children,multiplicite in node.get_children().items():
                    for i in range(multiplicite):
                        #col = ["red", "blue", "green", "aqua", "brown", "darkmagenta"][i % 3]
                        #col = x11_colors[i%x11_colors_taille]
                        file.write(f"\t{node.get_id()} -> {children} [color={col} minlen={i+1}];\n") #afin de differencier les arretes on leur atribue une couleur dependant de leur parent
                index_couleur +=1
            file.write("}")

        
    @classmethod
    def from_dot_file(self, path:str):
        graph = self.empty()
        dic = {}
        with open(path, "r") as file:
            lines = lignes_sans_v = [ligne.strip() for ligne in file]  #recupère toutes les lignes
        i = 1
        fin = len(lines)-1
        print(fin)
        while i < fin:
            print("i=",i)
            words = lines[i].split()
            if len(words) == 1:
                n = node(int(words[0].strip(';')), "", {}, {})
                dic[int(words[0].strip(';'))] = n
            elif words[1] != "->":
                n = node(int(words[0].strip(';')), "label",{},{})
                dic[int(words[0].strip(';'))] = n
            else:
                multiplicite = 1
                words_S = lines[i+1].split()
                #while(i + 1 < len(lines) and lines[i + 1].split()[0] == words[0] and lines[i + 1].split()[2] == words[2]):
                #while(words_S[0] == words[0] and words_S[2] == words[2]):
                while(i + 1 < len(lines) and lines[i+1].split()[0] == words[0] and lines[i+1].split()[2] == words[2]):
                    multiplicite += 1
                    words_S = lines[i+1].split()
                    i += 1
                for i in range(multiplicite):
                    print(multiplicite)
                    dic[int(words[0].strip(';'))].add_child_id(int(words[2].strip(';')), multiplicite)
                    print(dic[int(words[0].strip(';'))])
                    dic[int(words[2].strip(';'))].add_parent_id(int(words[0].strip(';')), multiplicite)
            i+=1
        """
        i = 1
        while i < len(lines)-1:
            words = lines[i].split()
            if words[1] != "->":
                n = node(int(words[0]), words[1].split('"')[1],{},{})
                dic[int(words[0])] = n
                i += 1
            else:
                multiplicite = 1
                words_S = lines[i+1].split()
                while(i + 1 < len(lines) and lines[i + 1].split()[0] == words[0] and lines[i + 1].split()[2] == words[2]):
                    multiplicite += 1
                    i += 1
                dic[int(words[0])].add_child_id(int(words[2]), multiplicite)
                dic[int(words[2])].add_parent_id(int(words[0]), multiplicite)
                i += 1
        """
        graph.nodes = dic
        print(dic)
        """for n in dic.values():
            for p in n.get_parents().keys():
                graph.add_edge(n.get_id(), p)
            for c in n.get_children().keys():
                graph.add_edge(n.get_id(), c)"""
        # faut coder la partie du input et output
        #graph.inputs = 
        #graph.outputs = 
        return graph

    
    def display(self, verbose=False):
        import os #pour le display du noeud
        self.save_as_dot_file("temp.dot",verbose)
        process = f"dot -Tpng temp.dot -o temp.png && open temp.png" #remplacer open par start sur windows
        os.system(process)