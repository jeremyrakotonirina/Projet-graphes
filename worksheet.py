from modules.open_digraph import *
import inspect

"""  Exercice 9 du TP1 

print(f"\n Methodes de la classe node: \n {dir(node)}\n")
print(f"\n Methodes de la classe node: \n {dir(open_digraph)}\n")

print(f"\n Documentation de node.copy : \n {inspect.getdoc(node.copy)}\n")
print(f"Lignes de code de node.copy : \n {inspect.getsourcelines(node.copy)}\n")
print(f"Fichier ou se trouve node.copy : \n {inspect.getfile(node.copy)}\n")
"""

#test effectués pour voir si les dot fonctionnaient
""" 
G=open_digraph([],[],[])
G = G.random(4, 3, form='loop-free')#graphe d'origine
print(G)
G.save_as_dot_file("test.dot", verbose=False)

P=open_digraph([],[],[])
P = P.from_dot_file("test.dot")
print(P)
G.display()
"""

