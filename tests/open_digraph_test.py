import sys
import os
root=os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.open_digraph import *

class InitTest(unittest.TestCase):
    
    def test_init_node(self):
        nO=node(0,'i',{},{1:1})
        self.assertEqual(nO.id,0)
        self.assertEqual(nO.label, 'i')
        self.assertEqual(nO.parents, {})
        self.assertEqual(nO.children, {1:1})
        self.assertIsInstance(nO,node)
        
        #--------Tests pour copy()--------------------
        n1 = node(1, "A", {2: 1}, {3: 1})
        n1_copy = n1.copy()
        self.assertIsNot(n1_copy, n1)
        self.assertEqual(n1_copy.id, n1.id)
        self.assertEqual(n1_copy.label, n1.label)
        self.assertEqual(n1_copy.parents, n1.parents)
        self.assertEqual(n1_copy.children, n1.children)
        n1_copy.parents[4] = 2
        self.assertNotEqual(n1_copy.parents, n1.parents)
    
    def test_init_opendigraph(self):
        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1, 1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        self.assertEqual(G.inputs, [3,4])
        self.assertEqual(G.outputs, [5,6])
        self.assertEqual(G.nodes[1],n1)
        self.assertIsInstance(G.nodes[2], node)
        self.assertIsInstance(G, open_digraph)
        
        #------------Tests pour copy()---------------------------
        G_copy = G.copy()
        self.assertIsNot(G_copy, G)
        self.assertIsNot(G_copy.inputs, G.inputs)
        self.assertIsNot(G_copy.outputs, G.outputs)
        self.assertEqual(G_copy.inputs, G.inputs)
        self.assertEqual(G_copy.outputs, G.outputs)
        for id in G.nodes:
            self.assertIsNot(G_copy.nodes[id], G.nodes[id])
            self.assertEqual(G_copy.nodes[id].id, G.nodes[id].id)
            self.assertEqual(G_copy.nodes[id].label, G.nodes[id].label)
            self.assertEqual(G_copy.nodes[id].parents, G.nodes[id].parents)
            self.assertEqual(G_copy.nodes[id].children, G.nodes[id].children)
        G_copy.nodes[0].label = "X"
        self.assertNotEqual(G_copy.nodes[0].label, G.nodes[0].label)
        
        
class MethodesDigraphTest(unittest.TestCase):        
        def test_methodes_suppresion(self):
            n0 = node(0, 'A', { }, {1: 2, 2: 1})  # 2 arêtes vers 1, 1 arête vers 2
            n1 = node(1, 'B', {0: 2}, {2: 1})  # 2 arêtes venant de 0, 1 arête vers 2
            n2 = node(2, 'C', {0: 1, 1: 1}, {})  # 1 arête venant de 0, 1 arête venant de 1
            
            G = open_digraph([0], [2], [n0, n1, n2])
            
            G.add_edge(0, 1)  # Ajout d'une arête entre 0 et 1
            G.add_edge(1, 2)  # Ajout d'une arête entre 1 et 2
            G.remove_edges((0, 1))  # Suppression des arêtes ajoutées
            
            self.assertEqual( G.get_node_by_id(0).get_children(), {1: 2, 2: 1} ) # Une seule arête vers 1 supprimée (reste 2)
            self.assertEqual( G.get_node_by_id(1).get_children() , {2: 2} ) # Une seule arête vers 2 supprimée (reste 0, donc supprimé)
            
            G.add_edge(0, 1)  # Ajout d'une arête entre 0 et 1 (multiplicité +1)
            G.add_edge(0, 1)  # Ajout d'une seconde arête entre 0 et 1 (multiplicité +1)
            G.remove_several_parallel_edges((0, 1))  # Suppression de toutes les occurrences
            
            self.assertNotIn(1, G.get_node_by_id(0).get_children())
            
            G.add_edge(0, 1)  # Ajout d'une arête entre 0 et 1
            G.add_edge(2, 1)  # Ajout d'une arête entre 2 et 1
            G.remove_nodes_by_id(0, 2)  # Suppression des nœuds 0 et 2
            
            self.assertIn(0, G.get_id_node_map())  
            self.assertIn(2, G.get_id_node_map())    # Le nœud 2 doit pas être supprimé
            self.assertEqual( G.get_node_by_id(0).get_children() , {})  # Plus d'arêtes sortantes de 0
            self.assertEqual( G.get_node_by_id(0).get_parents() , {})  # Plus d'arêtes entrantes vers 0
            self.assertEqual( G.get_node_by_id(2).get_children() , {})  # Plus d'arêtes sortantes de 2
            self.assertEqual( G.get_node_by_id(2).get_parents() , {})  # Plus d'arêtes entrantes vers 2
        
        def test_add_node(self):
            G = open_digraph([], [], [])  # Graphe vide
        
            id_n0 = G.add_node("A")
            self.assertEqual(G.get_node_by_id(id_n0).label, "A")
            self.assertEqual(G.get_node_by_id(id_n0).get_parents(), {})
            self.assertEqual(G.get_node_by_id(id_n0).get_children(), {})
        
            id_n1 = G.add_node("B", parents=[id_n0])
            self.assertEqual(G.get_node_by_id(id_n1).label, "B")
            self.assertEqual(G.get_node_by_id(id_n1).get_parents(), {id_n0: 1})
            self.assertEqual(G.get_node_by_id(id_n0).get_children(), {id_n1: 1})
        
            id_n2 = G.add_node("C", children=[id_n1])
            self.assertEqual(G.get_node_by_id(id_n2).get_children(), {id_n1: 1})
            self.assertEqual(G.get_node_by_id(id_n1).get_parents(), {id_n0: 1, id_n2: 1})
        
        def test_add_input_output_node(self):
             
            n0 = node(0, 'A', {}, {1: 1})  # Pointe vers 1
            n1 = node(1, 'B', {0: 1}, {})  # Vient de 0
            G = open_digraph([0], [1], [n0, n1])
            
            new_input_id = G.add_input_node(1)
            assert new_input_id in G.get_id_node_map()
            assert new_input_id in G.get_input_ids()
            assert G.get_node_by_id(new_input_id).get_children() == {1: 1}
            assert new_input_id in G.get_node_by_id(1).get_parents()
            
            new_output_id = G.add_output_node(1)
            assert new_output_id in G.get_id_node_map()
            assert new_output_id in G.get_output_ids()
            assert G.get_node_by_id(new_output_id).get_parents() == {1: 1}
            assert new_output_id in G.get_node_by_id(1).get_children()
            
        
        def test_is_well_formed(self):
            n0 = node(0, 'A', {}, {1: 1})  
            n1 = node(1, 'B', {0: 1}, {2: 1})  
            n2 = node(2, 'C', {1: 1}, {})  
            G = open_digraph([0], [2], [n0, n1, n2])
            self.assertTrue(G.is_well_formed())
        
            n3 = node(3, 'D', {}, {4: 1, 5: 1})
            G = open_digraph([3], [2], [n3, n1, n2])
            self.assertFalse(G.is_well_formed())
        
            n4 = node(4, 'E', {1: 1, 2: 1}, {})
            G = open_digraph([0], [4], [n0, n1, n4])
            self.assertFalse(G.is_well_formed())
        
            G = open_digraph([0], [2], [n0, n1, n2])
            new_id=G.add_node("X", parents=[1])
            self.assertTrue(G.is_well_formed())
        
            G.remove_node_by_id(new_id)
            self.assertTrue(G.is_well_formed())

            G.add_edge(1, 3)
            self.assertTrue(G.is_well_formed())
        
            G.remove_edge(1, 3)
            self.assertTrue(G.is_well_formed())
         
            G.add_input_node(3)
            self.assertTrue(G.is_well_formed())
        
            G.add_output_node(1)
            self.assertTrue(G.is_well_formed())
            

class testMatrice(unittest.TestCase):
        def test_graphe_matrice(self):
            n = 4
            bound = 3
            forms = ["free",  "loop-free"] 
            G=open_digraph([],[],[])
            for form in forms: #tests sur quelques formes
                print(f"\nTest random graph avec form: {form}")
                G = G.random(n, bound, form=form)#graphe d'origine
                print(G)
                adjacency = G.adjacency_matrix() #matrice du graphe
                afficher_matrice(adjacency)
                G2= graph_from_adjacency_matrix(adjacency) #G2 doit être égal à G
                print(G2)
                
        def test_affichage_matrice(self):
            n = 5  # Taille de la matrice
            bound = 3  # Valeur maximale des arêtes
            
            print("\nTest random_int_matrix:")
            m1 = random_int_matrix(n, bound, True)
            afficher_matrice(m1)
            
            print("Test random_symetric_int_matrix:")
            m2 = random_symetric_int_matrix(n, bound, True)
            afficher_matrice(m2)
            
            print("Test random_oriented_int_matrix:")
            m3 = random_oriented_int_matrix(n, bound, True)
            afficher_matrice(m3)
            
            print("Test random_triangular_int_matrix:")
            m4 = random_triangular_int_matrix(n, bound, True)
            afficher_matrice(m4)
            
            self.assertTrue( all(m1[i][i] == 0 for i in range(n)), "La diagonale de random_int_matrix doit être nulle")
            self.assertTrue(all(m2[i][j] == m2[j][i] for i in range(n) for j in range(n)), 
                            "random_symetric_int_matrix doit être symétrique")
        
            self.assertTrue(all((m3[i][j] == 0 or m3[j][i] == 0) for i in range(n) for j in range(n)), 
                            "random_oriented_int_matrix ne doit pas avoir d'arêtes bidirectionnelles")
        
            self.assertTrue(all(m4[i][j] == 0 for i in range(n) for j in range(i)), 
                            "random_triangular_int_matrix doit être triangulaire")

                      

if __name__ == '__main__':
    unittest.main()

