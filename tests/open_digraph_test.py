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
            G.is_well_formed()
       
            n3 = node(3, 'D', {}, {4: 1, 5: 1})
            G = open_digraph([3], [2], [n3, n1, n2])
            with self.assertRaises(Exception):
                 G.is_well_formed()
       
            n4 = node(4, 'E', {1: 1, 2: 1}, {})
            G = open_digraph([0], [4], [n0, n1, n4])
            with self.assertRaises(Exception):
                 G.is_well_formed()
       
            G = open_digraph([0], [2], [n0, n1, n2])
            new_id=G.add_node("X", parents=[1])
            G.is_well_formed()
       
            G.remove_node_by_id(new_id)
            G.is_well_formed()

            G.add_edge(1, 3)
            G.is_well_formed()
       
            G.remove_edge(1, 3)
            G.is_well_formed()
         
            G.add_input_node(3)
            G.is_well_formed()
       
            G.add_output_node(1)
            G.is_well_formed()
        
        print('----------------------------test de methode dikstra--------------------------------')
        def test_djikstra(self):
            
            a = node(0, 'A', {}, {1: 1, 2: 1})
            b = node(1, 'B', {0: 1}, {3: 1})
            c = node(2, 'C', {0: 1}, {3: 1})
            d = node(3, 'D', {1: 1, 2: 1}, {})
            e = node(4, 'E', {}, {})  # isolé
            G = open_digraph([0], [3], [a, b, c, d, e])

            dist, prev = G.dijkstra(0, direction=1)

            self.assertEqual(dist[0], 0)
            self.assertEqual(dist[1], 1)
            self.assertEqual(dist[2], 1)
            self.assertEqual(dist[3], 2)
            self.assertNotIn(4, dist)

            self.assertEqual(prev[1], 0)
            self.assertEqual(prev[2], 0)
            self.assertIn(prev[3], [1, 2])

            dist_undirected, _ = G.dijkstra(3, direction=None)
            self.assertEqual(dist_undirected[0], 2)
            self.assertEqual(dist_undirected[3], 0)
            self.assertEqual(dist_undirected[2], 1)
            self.assertEqual(prev[1], 0)
            self.assertEqual(prev[2], 0)
            self.assertNotIn(4, dist_undirected)

        def test_dijkstra_isolated_source(self):
            a = node(0, 'A', {}, {})
            b = node(1, 'B', {}, {})
            G = open_digraph([0], [1], [a, b])
            dist, prev = G.dijkstra(0, direction=1)
            self.assertEqual(dist, {0: 0})
            self.assertEqual(prev, {})

        def test_dijkstra_self_loop(self):
            a = node(0, 'A', {0: 1}, {0: 1})
            G = open_digraph([0], [0], [a])
            dist, prev = G.dijkstra(0, direction=1)
            self.assertEqual(dist, {0: 0})
            self.assertEqual(prev, {})

        def test_dijkstra_multiple_paths(self):
            a = node(0, 'A', {}, {1: 1, 2: 1})
            b = node(1, 'B', {0: 1}, {3: 1})
            c = node(2, 'C', {0: 1}, {})
            d = node(3, 'D', {1: 1}, {})
            G = open_digraph([0], [3], [a, b, c, d])
            dist, prev = G.dijkstra(0, direction=1)
            self.assertEqual(dist[3], 2)
            self.assertEqual(prev[3], 1)

        def test_dijkstra_disconnected(self):
            a = node(0, 'A', {}, {1: 1})
            b = node(1, 'B', {0: 1}, {})
            c = node(2, 'C', {}, {})
            G = open_digraph([0], [1], [a, b, c])
            dist, prev = G.dijkstra(0, direction=1)
            self.assertIn(0, dist)
            self.assertIn(1, dist)
            self.assertNotIn(2, dist)

        def test_dijkstra_reverse_direction(self):
            a = node(0, 'A', {1: 1}, {})
            b = node(1, 'B', {2: 1}, {0: 1})
            c = node(2, 'C', {}, {1: 1})
            G = open_digraph([2], [0], [a, b, c])
            dist, prev = G.dijkstra(0, direction=-1)
            self.assertEqual(dist[0], 0)
            self.assertEqual(dist[1], 1)
            self.assertEqual(dist[2], 2)
            self.assertEqual(prev[1], 0)

        def test_dijkstra_with_tgt_early_stop(self):
            a = node(0, 'A', {}, {1: 1})
            b = node(1, 'B', {0: 1}, {2: 1})
            c = node(2, 'C', {1: 1}, {3: 1})
            d = node(3, 'D', {2: 1}, {})
            g = open_digraph([0], [3], [a, b, c, d])
            dist, prev = g.dijkstra(0, direction=1, tgt=2)
            self.assertEqual(dist, {0: 0, 1: 1, 2: 2})
            self.assertEqual(prev[2], 1)

        def test_dijkstra_invalid_tgt_type(self):
            a = node(0, 'A', {}, {})
            g = open_digraph([0], [], [a])
            with self.assertRaises(TypeError):
                g.dijkstra(0, tgt="C")

        def test_dijkstra_invalid_tgt_id(self):
            a = node(0, 'A', {}, {})
            g = open_digraph([0], [], [a])
            with self.assertRaises(ValueError):
                g.dijkstra(0, tgt=5)

        def test_shortest_path_valid(self):
            a = node(0, 'A', {}, {1: 1, 2: 1})
            b = node(1, 'B', {0: 1}, {})
            c = node(2, 'C', {0: 1}, {3: 1})
            d = node(3, 'D', {2: 1}, {})
            g = open_digraph([0], [3], [a, b, c, d])
            path = g.shortest_path(0, 3)
            path2 = g.shortest_path(2, 2)
            self.assertEqual(path, [0, 2, 3])
            self.assertEqual(path2, [2])

        def test_shortest_path_inaccessible(self):
            a = node(0, 'A', {}, {1: 1})
            b = node(1, 'B', {0: 1}, {})
            c = node(2, 'C', {}, {})
            g = open_digraph([0], [1, 2], [a, b, c])
            path = g.shortest_path(0, 2)
            self.assertEqual(path, [])

        def test_shortest_path_same_node(self):
            a = node(0, 'A', {}, {})
            g = open_digraph([0], [0], [a])
            path = g.shortest_path(0, 0)
            self.assertEqual(path, [0])

        def test_shortest_path_from_middle_node(self):
            n0 = node(0, 'A', {}, {1: 1})
            n1 = node(1, 'B', {}, {5: 1})
            n2 = node(2, 'C', {}, {5: 1})
            n3 = node(3, 'D', {5: 1}, {})
            n4 = node(4, 'E', {5: 1}, {})
            n5 = node(5, 'U', {0: 1, 1: 1, 2: 1}, {3: 1, 4: 1})
            g = open_digraph([0, 1, 2], [3, 4], [n0, n1, n2, n3, n4, n5])
            path_to_3 = g.shortest_path(5, 3)
            self.assertEqual(path_to_3, [5, 3])
            path_to_4 = g.shortest_path(5, 4)
            self.assertEqual(path_to_4, [5, 4])
        
        def test_shortest_path_multiple_routes(self):
            n0 = node(0, '', {}, {1: 1, 4: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {1: 1}, {3: 1})
            n3 = node(3, '', {2: 1}, {})
            n4 = node(4, '', {0: 1}, {3: 1})
            g = open_digraph([0], [3], [n0, n1, n2, n3, n4])
            path = g.shortest_path(0, 3)
            self.assertEqual(path, [0, 4, 3])

        def test_dijkstra_multiple_equal_paths(self):
            n0 = node(0, '', {}, {1: 1, 2: 1})
            n1 = node(1, '', {0: 1}, {3: 1})
            n2 = node(2, '', {0: 1}, {3: 1})
            n3 = node(3, '', {1: 1, 2: 1}, {})
            g = open_digraph([0], [3], [n0, n1, n2, n3])
            path = g.shortest_path(0, 3)
            self.assertIn(path, [[0, 1, 3], [0, 2, 3]])

        def test_dijkstra_with_cycle(self):
        # 0 → 1 → 2 → 0 (cycle)
            n0 = node(0, '', {2: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {1: 1}, {0: 1})
            g = open_digraph([0], [2], [n0, n1, n2])
            path = g.shortest_path(0, 2, direction = 1)
            self.assertEqual(path, [0, 1, 2])

        def test_dijkstra_direction_none_parents_and_children(self):
            # 0 → 1 ← 2 (0 et 2 sont tous deux liés à 1)
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1, 2: 1}, {})
            n2 = node(2, '', {}, {1: 1})
            g = open_digraph([0, 2], [1], [n0, n1, n2])
            path_0_to_2 = g.shortest_path(0, 2, direction=None)
            self.assertEqual(path_0_to_2, [0, 1, 2])

        def test_ancetres_communs_distances_td(self):

            #exactement le meme test que celui du td!!
            n0 = node(0, '', {}, {3: 1})
            n1 = node(1, '', {}, {5: 1, 8: 1, 4: 1})
            n2 = node(2, '', {}, {4: 1})
            n3 = node(3, '', {0: 1}, {5: 1, 6: 1, 7: 1})
            n4 = node(4, '', {1: 1, 2: 1}, {6: 1})
            n5 = node(5, '', {1: 1, 3: 1}, {7: 1})
            n6 = node(6, '', {3: 1, 4: 1}, {8: 1, 9: 1})
            n7 = node(7, '', {3: 1, 5: 1}, {})
            n8 = node(8, '', {1: 1, 6: 1}, {})
            n9 = node(9, '', {6: 1}, {})

            g = open_digraph([0, 2], [7], [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9])
            resultat = g.ancetres_communs_distances(5, 8)
            attendu = {0: (2, 3), 3: (1, 2), 1: (1, 1)}
            self.assertEqual(resultat, attendu)

        # Cas sans ancêtres communs
        def test_ancetres_communs_none(self):
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1}, {})
            n2 = node(2, '', {}, {3: 1})
            n3 = node(3, '', {2: 1}, {})
            g = open_digraph([], [], [n0, n1, n2, n3])
            resultat = g.ancetres_communs_distances(1, 3)
            self.assertEqual(resultat, {})

        # Cas où u == v
        def test_ancetres_communs_same_node(self):
            n0 = node(0, '', {}, {})
            g = open_digraph([0], [], [n0])
            resultat = g.ancetres_communs_distances(0, 0)
            self.assertEqual(resultat, {0: (0, 0)})

        # Cas où un nœud est ancêtre de l'autre
        def test_ancetres_communs_parent_child(self):
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1}, {})
            g = open_digraph([0], [1], [n0, n1])
            resultat = g.ancetres_communs_distances(0, 1)
            self.assertEqual(resultat, {0: (0, 1)})
        
         # Cas avec plusieurs chemins vers un même ancêtre commun
        def test_ancetres_communs_multiple_paths(self):
        # 4 → 2 ← 0
        # 4 → 3 ← 1
            n0 = node(0, '', {}, {2: 1})
            n1 = node(1, '', {}, {3: 1})
            n2 = node(2, '', {0: 1, 4: 1}, {})
            n3 = node(3, '', {1: 1, 4: 1}, {})
            n4 = node(4, '', {}, {2: 1, 3: 1})
            g = open_digraph([0, 1], [], [n0, n1, n2, n3, n4])
            resultat = g.ancetres_communs_distances(2, 3)
            self.assertEqual(resultat, {4: (1, 1)})

           

class testMatrice(unittest.TestCase):
        def test_graphe_matrice(self):
            n = 4
            bound = 2
            forms = ["free"] #on peut rajouter loop_free, DAG,...
            G=open_digraph([],[],[])
            for form in forms: #tests sur quelques formes
                print(f"\nTest random graph avec form: {form}")
                G = G.random(n, bound, inputs=2, outputs=2, form=form)#graphe d'origine
                print(G)
                G.display()
                adjacency = G.adjacency_matrix() #matrice du graphe
                afficher_matrice(adjacency)
              
               
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