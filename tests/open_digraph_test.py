import sys
import os
root=os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.open_digraph import *
from modules.bool_circ import *

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

        def test_iparallel_and_parallel(self):
            g1 = open_digraph([0], [1], [
                node(0, "", {}, {1: 1}),
                node(1, "", {0: 1}, {})
            ])
            g2 = open_digraph([0], [1], [
                node(0, "", {}, {1: 1}),
                node(1, "", {0: 1}, {})
            ])

            g1_copy = g1.copy()
            g1_copy.iparallel(g2)

            # test nombre de nœuds
            self.assertEqual(len(g1_copy.get_nodes()), 4)
            # test inputs et outputs
            self.assertEqual(len(g1_copy.inputs), 2)
            self.assertEqual(len(g1_copy.outputs), 2)
            
            # vérifier que chaque input pointe vers le bon output
            children_0 = g1_copy.get_node_by_id(g1_copy.inputs[0]).get_children()
            children_1 = g1_copy.get_node_by_id(g1_copy.inputs[1]).get_children()
            self.assertEqual(list(children_0.values()), [1])
            self.assertEqual(list(children_1.values()), [1])

            g1 = open_digraph([0, 1], [4], [
            node(0, "", {}, {2: 1}),
            node(1, "", {}, {2: 1}),
            node(2, "&", {0: 1, 1: 1}, {3: 1}),
            node(3, "~", {2: 1}, {4: 1}),
            node(4, "", {3: 1}, {})
        ])
        
            g2 = open_digraph([5], [8], [
                node(5, "", {}, {6: 1}),
                node(6, "~", {5: 1}, {7: 1}),
                node(7, "&", {6: 1, 6: 1}, {8: 1}),
                node(8, "", {7: 1}, {})
            ])
            
            g1_copy = g1.copy()
            g1_copy.iparallel(g2)
            
            # Test nombre de nœuds
            self.assertEqual(len(g1_copy.get_nodes()), 9)
            # Test nombre d'inputs et outputs
            self.assertEqual(len(g1_copy.inputs), 3)
            self.assertEqual(len(g1_copy.outputs), 2)

            # Vérifier les connexions de inputs
            for input_id in g1_copy.inputs:
                children = g1_copy.get_node_by_id(input_id).get_children()
                self.assertTrue(len(children) >= 1)  # doit avoir au moins une sortie

        def test_icompose_and_compose(self):
            g1 = open_digraph([0], [1], [
                node(0, "", {}, {1: 1}),
                node(1, "", {0: 1}, {})
            ])
            g2 = open_digraph([0], [1], [
                node(0, "", {}, {1: 1}),
                node(1, "", {0: 1}, {})
            ])

            g1_copy = g1.copy()
            g1_copy.icompose(g2)

            # test structure
            self.assertEqual(len(g1_copy.get_nodes()), 4)
            print(g1_copy.get_id_node_map())
            self.assertEqual(len(g1_copy.inputs), 1)
            self.assertEqual(len(g1_copy.outputs), 1)

            g1 = open_digraph([0], [4], [
        node(0, "", {}, {1: 1}),
        node(1, "&", {0: 1}, {2: 1}),
        node(2, "|", {1: 1}, {3: 1}),
        node(3, "~", {2: 1}, {4: 1}),
        node(4, "", {3: 1}, {})
    ])
    
            g2 = open_digraph([5], [6], [
                node(5, "", {}, {6: 1}),
                node(6, "", {5: 1}, {})
            ])
            
            g1_copy = g1.copy()
            g1_copy.icompose(g2)
            
            # Après composition séquentielle
            self.assertEqual(len(g1_copy.get_nodes()), 7)
            self.assertEqual(len(g1_copy.inputs), 1)
            self.assertEqual(len(g1_copy.outputs), 1)

            # Vérifier la connexion entre g2.output -> g1.input
            composed_input = g1_copy.inputs[0]
            composed_output = g1_copy.outputs[0]
            children_input = g1_copy.get_node_by_id(composed_input).get_children()
            parents_output = g1_copy.get_node_by_id(composed_output).get_parents()

            # Entrée doit avoir un enfant
            self.assertTrue(len(children_input) > 0)
            # Sortie doit avoir un parent
            self.assertTrue(len(parents_output) > 0)

            

        def test_identity(self):
            g = open_digraph.identity(3)
            self.assertEqual(len(g.get_nodes()), 6)

            for i in range(3):
                in_node = g.get_node_by_id(i)
                out_node = g.get_node_by_id(i + 3)

                # test qu'un input pointe vers le bon output
                self.assertEqual(list(in_node.get_children().keys()), [i + 3])
                self.assertEqual(list(out_node.get_parents().keys()), [i])

        def test_connected_components(self):
            g = open_digraph([], [], [
                node(0, "", {}, {1: 1}),
                node(1, "", {0: 1}, {}),
                node(2, "", {}, {3: 1}),
                node(3, "", {2: 1}, {}),
            ])

            nb, comp_dict = g.connected_components()

            self.assertEqual(nb, 2)
            self.assertEqual(set(comp_dict.values()), {0, 1})

            # Vérifie que 0 et 1 sont ensemble, 2 et 3 ensemble
            self.assertEqual(comp_dict[0], comp_dict[1])
            self.assertEqual(comp_dict[2], comp_dict[3])
            self.assertNotEqual(comp_dict[0], comp_dict[2])

            g = open_digraph([], [], [
            node(0, "", {}, {1: 1}),
            node(1, "", {0: 1}, {}),
            node(2, "", {}, {3: 1}),
            node(3, "", {2: 1}, {4: 1}),
            node(4, "", {3: 1}, {}),
            node(5, "", {}, {})
            ])

            nb_comp, id_to_comp = g.connected_components()

            # 3 composantes
            self.assertEqual(nb_comp, 3)

            # Chaque noeud dans la bonne composante
            comp0 = id_to_comp[0]
            comp1 = id_to_comp[2]
            comp2 = id_to_comp[5]
            self.assertEqual(id_to_comp[1], comp0)
            self.assertEqual(id_to_comp[3], comp1)
            self.assertEqual(id_to_comp[4], comp1)

            # Vérifie que chaque composante est cohérente
            self.assertNotEqual(comp0, comp1)
            self.assertNotEqual(comp0, comp2)
            self.assertNotEqual(comp1, comp2)

        def test_connected_components_subgraphs(self):
            g = open_digraph([], [], [
                node(0, "", {}, {1: 1}),
                node(1, "", {0: 1}, {}),
                node(2, "", {}, {3: 1}),
                node(3, "", {2: 1}, {}),
            ])

            subgraphs = g.connected_components_subgraphs()
            self.assertEqual(len(subgraphs), 2)

            ids_sets = [set(node.get_id() for node in sg.get_nodes()) for sg in subgraphs]

            # les deux sous-graphes doivent avoir {0,1} et {2,3}
            self.assertIn({0,1}, ids_sets)
            self.assertIn({2,3}, ids_sets)

            g = open_digraph([0,3], [2,4], [
            node(0, "", {}, {1: 1}),
            node(1, "", {0: 1}, {2: 1}),
            node(2, "", {1: 1}, {}),
            node(3, "", {}, {4: 1}),
            node(4, "", {3: 1}, {})
            ])

            subgraphs = g.connected_components_subgraphs()

            # On doit avoir 2 sous-graphes
            self.assertEqual(len(subgraphs), 2)

            # Vérifie que chaque sous-graphe a la bonne structure
            for subg in subgraphs:
                # Tous les noeuds doivent être connectés
                nb_comp, _ = subg.connected_components()
                self.assertEqual(nb_comp, 1)

            # Vérifie que les inputs/outputs sont corrects
            all_inputs = [id for sg in subgraphs for id in sg.get_input_ids()]
            all_outputs = [id for sg in subgraphs for id in sg.get_output_ids()]

            self.assertCountEqual(all_inputs, [0,3])
            self.assertCountEqual(all_outputs, [2,4])

            # Vérifie aussi que liaisons sont cohérentes à l'intérieur
            for sg in subgraphs:
                for nid in sg.get_id_node_map():
                    noeud = sg.get_node_by_id(nid)
                    for child_id in noeud.get_children():
                        self.assertIn(child_id, sg.get_id_node_map())
                    for parent_id in noeud.get_parents():
                        self.assertIn(parent_id, sg.get_id_node_map())
        
        print('----------------------------test de methode dikstra--------------------------------')
        def test_djikstra(self):
            
            n0 = node(0, 'A', {}, {1: 1, 2: 1})
            n1 = node(1, 'B', {0: 1}, {3: 1})
            n2 = node(2, 'C', {0: 1}, {3: 1})
            n3 = node(3, 'D', {1: 1, 2: 1}, {})
            n4 = node(4, 'E', {}, {}) 
            G = open_digraph([], [], [n0, n1, n2, n3, n4])
            G.is_well_formed()

            dist, prev = G.dijkstra(0, direction=1)

            self.assertEqual(dist[0], 0)
            self.assertEqual(dist[1], 1)
            self.assertEqual(dist[2], 1)
            self.assertEqual(dist[3], 2)
            self.assertNotIn(4, dist)

            self.assertEqual(prev[1], 0)
            self.assertEqual(prev[2], 0)
            self.assertIn(prev[3], [1, 2])

            dist_2, prev2 = G.dijkstra(3, direction=None)
            self.assertEqual(dist_2[0], 2)
            self.assertEqual(dist_2[3], 0)
            self.assertEqual(dist_2[2], 1)
            self.assertEqual(prev[1], 0)
            self.assertEqual(prev[2], 0)
            self.assertNotIn(4, dist_2)

        def test_dijkstra_2_noeud_isolé(self):
            n0 = node(0, '', {}, {})
            n1 = node(1, '', {}, {})
            G = open_digraph([], [], [n0, n1])
            G.is_well_formed()
            dist, prev = G.dijkstra(0, direction=1)
            self.assertEqual(dist, {0: 0})
            self.assertEqual(prev, {})

        def test_dijkstra_cycle_sur_lui_meme(self):
            n0 = node(0, '', {0: 1}, {0: 1})
            G = open_digraph([], [], [n0])
            G.is_well_formed()
            dist, prev = G.dijkstra(0, direction=1)
            self.assertEqual(dist, {0: 0})
            self.assertEqual(prev, {})

        def test_dijkstra_plusieur_chemin(self):
            a = node(0, '', {}, {1: 1, 2: 1})
            b = node(1, '', {0: 1}, {3: 1})
            c = node(2, '', {0: 1}, {})
            d = node(3, '', {1: 1}, {})
            G = open_digraph([], [2, 3], [a, b, c, d])
            G.is_well_formed()
            dist, prev = G.dijkstra(0, direction=1)
            self.assertEqual(dist[3], 2)
            self.assertEqual(prev[3], 1)

        def test_dijkstra_séparé(self):
            a = node(0, '', {}, {1: 1})
            b = node(1, '', {0: 1}, {})
            c = node(2, '', {}, {})
            G = open_digraph([0], [1], [a, b, c])
            G.is_well_formed()
            dist, prev = G.dijkstra(0, direction=1)
            self.assertIn(0, dist)
            self.assertIn(1, dist)
            self.assertNotIn(2, dist)

        def test_dijkstra_direction_inversé(self):
            a = node(0, '', {1: 1}, {})
            b = node(1, '', {2: 1}, {0: 1})
            c = node(2, '', {}, {1: 1})
            G = open_digraph([2], [0], [a, b, c])
            G.is_well_formed()
            dist, prev = G.dijkstra(0, direction=-1)
            self.assertEqual(dist[0], 0)
            self.assertEqual(dist[1], 1)
            self.assertEqual(dist[2], 2)
            self.assertEqual(prev[1], 0)

        def test_dijkstra_avec_tgt(self):
            a = node(0, '', {}, {1: 1})
            b = node(1, '', {0: 1}, {2: 1})
            c = node(2, '', {1: 1}, {3: 1})
            d = node(3, '', {2: 1}, {})
            g = open_digraph([0], [3], [a, b, c, d])
            g.is_well_formed()
            dist, prev = g.dijkstra(0, direction=1, tgt=2)
            self.assertEqual(dist, {0: 0, 1: 1, 2: 2})
            self.assertEqual(prev[2], 1)

        def test_dijkstra_tgt_eroroné(self):
            a = node(0, '', {}, {})
            g = open_digraph([], [], [a])
            g.is_well_formed()
            with self.assertRaises(TypeError):
                g.dijkstra(0, tgt="C")

        def test_dijkstra_identifiant_tgt_faux(self):
            a = node(0, '', {}, {})
            g = open_digraph([], [], [a])
            g.is_well_formed()
            with self.assertRaises(ValueError):
                g.dijkstra(0, tgt=5)

        def test_shortest_path(self):
            a = node(0, '', {}, {1: 1, 2: 1})
            b = node(1, '', {0: 1}, {})
            c = node(2, '', {0: 1}, {3: 1})
            d = node(3, '', {2: 1}, {})
            g = open_digraph([], [3], [a, b, c, d])
            g.is_well_formed()
            path = g.shortest_path(0, 3)
            path2 = g.shortest_path(2, 2)
            self.assertEqual(path, [0, 2, 3])
            self.assertEqual(path2, [2])

        def test_shortest_path_inaccessible(self):
            a = node(0, '', {}, {1: 1})
            b = node(1, '', {0: 1}, {})
            c = node(2, '', {}, {})
            g = open_digraph([0], [1], [a, b, c])
            g.is_well_formed()
            path = g.shortest_path(0, 2)
            self.assertEqual(path, [])

        def test_shortest_path_meme_noeud(self):
            a = node(0, '', {}, {})
            g = open_digraph([], [], [a])
            g.is_well_formed()
            path = g.shortest_path(0, 0)
            self.assertEqual(path, [0])

        def test_shortest_path_depuis_milieu(self):
            n0 = node(0, '', {}, {1: 1, 5: 1})
            n1 = node(1, '', {0: 1}, {5: 1})
            n2 = node(2, '', {}, {5: 1})
            n3 = node(3, '', {5: 1}, {})
            n4 = node(4, '', {5: 1}, {})
            n5 = node(5, '', {0: 1, 1: 1, 2: 1}, {3: 1, 4: 1})
            g = open_digraph([2], [3, 4], [n0, n1, n2, n3, n4, n5])
            g.is_well_formed()
            path_to_3 = g.shortest_path(5, 3)
            self.assertEqual(path_to_3, [5, 3])
            path_to_4 = g.shortest_path(5, 4)
            self.assertEqual(path_to_4, [5, 4])
        
        def test_shortest_path_plusieur_chemins(self):
            n0 = node(0, '', {}, {1: 1, 4: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {1: 1}, {3: 1})
            n3 = node(3, '', {4: 1, 2: 1}, {})
            n4 = node(4, '', {0: 1}, {3: 1})
            g = open_digraph([], [], [n0, n1, n2, n3, n4])
            g.is_well_formed()
            path = g.shortest_path(0, 3)
            self.assertEqual(path, [0, 4, 3])

        def test_dijkstra_plusieurs_chemins_egaux(self):
            n0 = node(0, '', {}, {1: 1, 2: 1})
            n1 = node(1, '', {0: 1}, {3: 1})
            n2 = node(2, '', {0: 1}, {3: 1})
            n3 = node(3, '', {1: 1, 2: 1}, {})
            g = open_digraph([], [], [n0, n1, n2, n3])
            g.is_well_formed()
            path = g.shortest_path(0, 3)
            self.assertIn(path, [[0, 1, 3], [0, 2, 3]])

        def test_dijkstra_avec_cycle(self):
            n0 = node(0, '', {2: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {1: 1}, {0: 1})
            g = open_digraph([], [], [n0, n1, n2])
            g.is_well_formed()
            path = g.shortest_path(0, 2, direction = 1)
            self.assertEqual(path, [0, 1, 2])

        def test_dijkstra_direction_none(self):
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1, 2: 1}, {})
            n2 = node(2, '', {}, {1: 1})
            g = open_digraph([0, 2], [], [n0, n1, n2])
            g.is_well_formed()
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

            g = open_digraph([0, 2], [9], [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9])
            g.is_well_formed()
            resultat = g.ancetres_communs_distances(5, 8)
            attendu = {0: (2, 3), 3: (1, 2), 1: (1, 1)}
            self.assertEqual(resultat, attendu)

        # Cas sans ancêtres communs
        def test_ancetres_communs_pas_dancetres(self):
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1}, {})
            n2 = node(2, '', {}, {3: 1})
            n3 = node(3, '', {2: 1}, {})
            g = open_digraph([], [], [n0, n1, n2, n3])
            g.is_well_formed()
            resultat = g.ancetres_communs_distances(1, 3)
            self.assertEqual(resultat, {})

        # Cas où u == v
        def test_ancetres_communs_meme_noeud(self):
            n0 = node(0, '', {}, {})
            g = open_digraph([], [], [n0])
            resultat = g.ancetres_communs_distances(0, 0)
            g.is_well_formed()
            self.assertEqual(resultat, {0: (0, 0)})

        # Cas où un noeud est ancêtre de l'autre
        def test_ancetres_communs_lun_ancetre_de_lautre(self):
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1}, {})
            g = open_digraph([0], [1], [n0, n1])
            g.is_well_formed()
            resultat = g.ancetres_communs_distances(0, 1)
            self.assertEqual(resultat, {0: (0, 1)})
        
         # Cas avec plusieurs chemins vers un même ancêtre commun
        def test_ancetres_communs_plusieur_chemins_vers_memenoeud(self):
            n0 = node(0, '', {}, {2: 1})
            n1 = node(1, '', {}, {3: 1})
            n2 = node(2, '', {0: 1, 4: 1}, {})
            n3 = node(3, '', {1: 1, 4: 1}, {})
            n4 = node(4, '', {}, {2: 1, 3: 1})
            g = open_digraph([0, 1], [], [n0, n1, n2, n3, n4])
            g.is_well_formed()
            resultat = g.ancetres_communs_distances(2, 3)
            self.assertEqual(resultat, {4: (1, 1)})

        def test_tri_topologique_td(self):
            # exemple du td
            n0 = node(0, '', {}, {3: 1})
            n1 = node(1, '', {}, {4: 1, 5: 1, 8: 1})
            n2 = node(2, '', {}, {4: 1})
            n3 = node(3, '', {0: 1}, {5: 1, 6: 1, 7: 1})
            n4 = node(4, '', {1: 1, 2: 1}, {6: 1})
            n5 = node(5, '', {1: 1, 3: 1}, {7: 1})
            n6 = node(6, '', {3: 1, 4: 1}, {8: 1, 9: 1})
            n7 = node(7, '', {3: 1, 5: 1}, {})
            n8 = node(8, '', {1: 1, 6: 1}, {})
            n9 = node(9, '', {6: 1}, {})

            g = open_digraph([0,2], [9], [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9])

            g.is_well_formed()

            attendu = [[0, 1, 2], [3, 4], [5, 6], [7, 8, 9]]

            resultat = g.tri_topologique_par_niveaux()

            self.assertEqual(resultat, attendu)

        def test_tri_topo_ligne(self):
            n0 = node(0, '', {3: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {1: 1}, {4: 1})
            i0 = node(3, '', {}, {0: 1})
            o0 = node(4, '', {2: 1}, {})

            g = open_digraph([3], [4], [n0, n1, n2, i0, o0])
            g.is_well_formed()

            attendu = [[3], [0], [1], [2], [4]]
            self.assertEqual(g.tri_topologique_par_niveaux(), attendu)

        def test_tri_topo_special(self):
            n0 = node(0, '', {3: 1}, {2: 1})
            n1 = node(1, '', {4: 1}, {2: 1})
            n2 = node(2, '', {0: 1, 1: 1}, {5: 1})
            i0 = node(3, '', {}, {0: 1})
            i1 = node(4, '', {}, {1: 1})
            o0 = node(5, '', {2: 1}, {})

            g = open_digraph([3, 4], [5], [n0, n1, n2, i0, i1, o0])
            g.is_well_formed()

            attendu = [[3, 4], [0, 1], [2], [5]]
            self.assertEqual(g.tri_topologique_par_niveaux(), attendu)

        def test_tri_topo_vide(self):
            g = open_digraph([], [], [])
            g.is_well_formed()
            self.assertEqual(g.tri_topologique_par_niveaux(), [])

        def test_tri_topo_un_noeud(self):
            n0 = node(0, '', {1: 1}, {2: 1})
            i0 = node(1, '', {}, {0: 1})
            o0 = node(2, '', {0: 1}, {})

            g = open_digraph([1], [2], [n0, i0, o0])
            g.is_well_formed()

            self.assertEqual(g.tri_topologique_par_niveaux(), [[1], [0], [2]])

        def test_tri_topo_cycle_2_noeuds(self):
            n0 = node(0, '', {2: 1, 1: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {0: 1, 3: 1})
            i0 = node(2, '', {}, {0: 1})
            o0 = node(3, '', {1: 1}, {})

            g = open_digraph([2], [3], [n0, n1, i0, o0])
            g.is_well_formed()

            with self.assertRaises(ValueError):
                g.tri_topologique_par_niveaux()

        def test_tri_topo_cycle_complexe(self):
            n0 = node(0, '', {2: 1, 3: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {2: 1, 4: 1})
            n2 = node(2, '', {1: 1}, {0: 1})
            i0 = node(3, '', {}, {0: 1})
            o0 = node(4, '', {1: 1}, {})

            g = open_digraph([3], [4], [n0, n1, n2, i0, o0])
            g.is_well_formed()

            with self.assertRaises(ValueError):
                g.tri_topologique_par_niveaux()
        
        def test_tri_topo_avec_noeud_isole(self):

            n0 = node(0, '', {3: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {5: 1})
            n2 = node(2, '', {4: 1}, {6: 1}) 
            i0 = node(3, '', {}, {0: 1})
            i1 = node(4, 'i', {}, {2: 1})
            o0 = node(5, '', {1: 1}, {})
            o1 = node(6, '', {2: 1}, {})

            g = open_digraph([3, 4], [5, 6], [n0, n1, n2, i0, i1, o0, o1])
            g.is_well_formed()

            attendu = [[3, 4], [0, 2], [1, 6], [5]]
            self.assertEqual(g.tri_topologique_par_niveaux(), attendu)

        def test_profondeur_noeud_ligne(self):
            n0 = node(0, '', {3: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {1: 1}, {4: 1})
            i0 = node(3, '', {}, {0: 1})
            o0 = node(4, '', {2: 1}, {})

            g = open_digraph([3], [4], [n0, n1, n2, i0, o0])
            g.is_well_formed()

            self.assertEqual(g.profondeur_noeud(3), 0)  
            self.assertEqual(g.profondeur_noeud(0), 1)
            self.assertEqual(g.profondeur_noeud(1), 2)
            self.assertEqual(g.profondeur_noeud(2), 3)
            self.assertEqual(g.profondeur_noeud(4), 4)  

        def test_profondeur_noeud_qui_converge(self):
            n0 = node(0, '', {3: 1}, {2: 1})
            n1 = node(1, '', {4: 1}, {2: 1})
            n2 = node(2, '', {0: 1, 1: 1}, {5: 1})
            i0 = node(3, '', {}, {0: 1})
            i1 = node(4, '', {}, {1: 1})
            o0 = node(5, '', {2: 1}, {})

            g = open_digraph([3, 4], [5], [n0, n1, n2, i0, i1, o0])
            g.is_well_formed()

            self.assertEqual(g.profondeur_noeud(2), 2)

        def test_profondeur_noeud_inexistant(self):
            n0 = node(0, '', {2: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {3: 1})
            i0 = node(2, '', {}, {0: 1})
            o0 = node(3, '', {1: 1}, {})

            g = open_digraph([2], [3], [n0, n1, i0, o0])
            g.is_well_formed()

            with self.assertRaises(ValueError):
                g.profondeur_noeud(9) 

        def test_profondeur_noeud_graphe_cyclique(self):
            n0 = node(0, '', {2: 1, 1: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {0: 1, 3: 1})
            i0 = node(2, '', {}, {0: 1})
            o0 = node(3, '', {1: 1}, {})

            g = open_digraph([2], [3], [n0, n1, i0, o0])
            g.is_well_formed()

            with self.assertRaises(ValueError):
                g.profondeur_noeud(0)  # le tri topologique lève une erreur à cause du cycle

        def test_profondeur_noeud_graphe_vide(self):
            g = open_digraph([], [], [])
            g.is_well_formed()
            
            with self.assertRaises(ValueError):
                g.profondeur_noeud(0)  

        def test_profondeur_noeud_solo(self):
            n0 = node(0, '', {}, {})
            g = open_digraph([], [], [n0])
            g.is_well_formed()
            self.assertEqual(g.profondeur_noeud(0), 0)

        def test_profondeur_noeud_separe(self):
            n0 = node(0, '', {}, {})
            n1 = node(1, '', {}, {})
            n2 = node(2, '', {}, {})
            g = open_digraph([], [], [n0, n1, n2])
            g.is_well_formed()
            self.assertEqual(g.profondeur_noeud(0), 0)
            self.assertEqual(g.profondeur_noeud(1), 0)
            self.assertEqual(g.profondeur_noeud(2), 0)

        def test_profondeur_graphe_ligne(self):
            n0 = node(0, '', {3: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {1: 1}, {4: 1})
            i0 = node(3, '', {}, {0: 1})
            o0 = node(4, '', {2: 1}, {})

            g = open_digraph([3], [4], [n0, n1, n2, i0, o0])
            g.is_well_formed()

            self.assertEqual(g.profondeur_graphe(), 5)

        def test_profondeur_graphe_vide(self):
            g = open_digraph([], [], [])
            g.is_well_formed()

            self.assertEqual(g.profondeur_graphe(), 0)

        def test_profondeur_graphe_plusieur_branche(self):
            n0 = node(0, '', {3: 1}, {6: 1})
            n1 = node(1, '', {4: 1}, {7: 1})
            n2 = node(2, '', {5: 1}, {8: 1})
            n3 = node(3, '', {}, {0: 1})
            n4 = node(4, '', {}, {1: 1})
            n5 = node(5, '', {}, {2: 1})
            n6 = node(6, '', {0: 1}, {})
            n7 = node(7, '', {1: 1}, {})
            n8 = node(8, '', {2: 1}, {})

            g = open_digraph([3, 4, 5], [6, 7, 8], [n0, n1, n2, n3, n4, n5, n6, n7, n8])
            g.is_well_formed()

            self.assertEqual(g.profondeur_graphe(), 3)

        def test_profondeur_graphe_cyclique(self):
            n0 = node(0, '', {2: 1, 1: 1}, {1: 1})
            n1 = node(1, '', {0: 1}, {0: 1, 3: 1})
            i0 = node(2, '', {}, {0: 1})
            o0 = node(3, '', {1: 1}, {})

            g = open_digraph([2], [3], [n0, n1, i0, o0])
            g.is_well_formed()

            with self.assertRaises(ValueError):
                g.profondeur_graphe()

        def test_profondeur_graphe_2branche_separe(self):
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1}, {})
            n2 = node(2, '', {}, {3: 1})
            n3 = node(3, '', {2: 1}, {4: 1})
            n4 = node(4, '', {3: 1}, {})

            g = open_digraph([0, 2], [1, 4], [n0, n1, n2, n3, n4])
            g.is_well_formed()

            self.assertEqual(g.profondeur_graphe(), 3)

        def test_plus_long_chemin_ligne(self):
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {1: 1}, {3: 1})
            n3 = node(3, '', {2: 1}, {})
            g = open_digraph([0], [3], [n0, n1, n2, n3])
            g.is_well_formed()

            longueur, chemin = g.plus_long_chemin(0, 3)
            self.assertEqual(longueur, 3)
            self.assertEqual(chemin, [0, 1, 2, 3])

        def test_plus_long_chemin_deux_chemins_egaux(self):
            n0 = node(0, '', {}, {1: 1, 2: 1})
            n1 = node(1, '', {0: 1}, {3: 1})
            n2 = node(2, '', {0: 1}, {3: 1})
            n3 = node(3, '', {1: 1, 2: 1}, {})
            g = open_digraph([], [], [n0, n1, n2, n3])
            g.is_well_formed()

            longueur, chemin = g.plus_long_chemin(0, 3)
            self.assertEqual(longueur, 2)
            self.assertIn(chemin, [[0, 1, 3], [0, 2, 3]])  # les deux chemins sont valides

        def test_plus_long_chemin_deux_chemins_taille_différentes(self):
            n0 = node(0, '', {}, {1: 1, 2: 1})
            n1 = node(1, '', {0: 1}, {4: 1})
            n2 = node(2, '', {0: 1}, {3: 1})
            n3 = node(3, '', {2: 1}, {4: 1})
            n4 = node(4, '', {1: 1, 3: 1}, {})
            g = open_digraph([], [], [n0, n1, n2, n3, n4])
            g.is_well_formed()

            longueur, chemin = g.plus_long_chemin(0, 4)
            self.assertEqual(longueur, 3)
            self.assertEqual(chemin, [0, 2, 3, 4])

        def test_plus_long_chemin_aucun_chemin(self):
            n0 = node(0, '', {}, {})
            n1 = node(1, '', {}, {})
            g = open_digraph([], [], [n0, n1])
            g.is_well_formed()

            longueur, chemin = g.plus_long_chemin(0, 1)
            self.assertIsNone(longueur)
            self.assertEqual(chemin, [])

        def test_plus_long_chemin_noeud_solo(self):
            n0 = node(0, '', {}, {})
            g = open_digraph([], [], [n0])
            g.is_well_formed()

            longueur, chemin = g.plus_long_chemin(0, 0)
            self.assertEqual(longueur, 0)
            self.assertEqual(chemin, [0])

        def test_plus_long_chemin_noeud_inexistant(self):
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1}, {})
            g = open_digraph([], [], [n0, n1])
            g.is_well_formed()

            with self.assertRaises(ValueError):
                g.plus_long_chemin(42, 1)

        def test_plus_long_chemin_graphe_vide(self):
            g = open_digraph([], [], [])
            g.is_well_formed()

            with self.assertRaises(ValueError):
                g.plus_long_chemin(0, 1)

        def test_plus_long_chemin_ligne_dans_autre_sens(self):
            #doit renovyer chemin vide car v inatteignable
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {1: 1}, {3: 1})
            n3 = node(3, '', {2: 1}, {})
            g = open_digraph([0], [3], [n0, n1, n2, n3])
            g.is_well_formed()

            longueur, chemin = g.plus_long_chemin(3, 0)
            self.assertEqual(longueur, None)
            self.assertEqual(chemin, [])

        def test_plus_long_chemin_branche_separe(self):
            n0 = node(0, '', {}, {1: 1})
            n1 = node(1, '', {0: 1}, {2: 1})
            n2 = node(2, '', {3: 1, 1: 1}, {})
            n3 = node(3, '', {4: 1}, {2: 1})
            n4 = node(4, '', {}, {3: 1})
            g = open_digraph([0], [], [n0, n1, n2, n3, n4])
            g.is_well_formed()

            longueur, chemin = g.plus_long_chemin(0, 3)
            self.assertEqual(longueur, None)
            self.assertEqual(chemin, [])
        print('-------------fin des test tp7 8 djikstra....-----------------')

        def test_min_max_id(self):
            g = open_digraph([], [], [
                node(10, "", {}, {}),
                node(20, "", {}, {}),
                node(30, "", {}, {})
            ])
            self.assertEqual(g.min_id(), 10)
            self.assertEqual(g.max_id(), 30)
    
        def test_shift_indices(self):
            g = open_digraph([], [], [
                node(0, "", {}, {1: 1}),
                node(1, "", {0: 1}, {2: 1}),
                node(2, "", {1: 1}, {})
            ])
            g.shift_indices(10)
            
            ids = g.get_id_node_map()
            self.assertIn(10, ids)
            self.assertIn(11, ids)
            self.assertIn(12, ids)
            
            self.assertEqual(g.get_node_by_id(10).get_children(), {11: 1})
            self.assertEqual(g.get_node_by_id(11).get_parents(), {10: 1})
            self.assertEqual(g.get_node_by_id(11).get_children(), {12: 1})
            self.assertEqual(g.get_node_by_id(12).get_parents(), {11: 1})

           

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

class TestBoolCirc(unittest.TestCase):

    def test_is_cyclic_false(self):
        # Graphe acyclique simple : 0 -> 1
        g = open_digraph([0], [1], [
            node(0, "|", {}, {1: 1}),
            node(1, "", {0:1}, {})
        ])
        bc = bool_circ(g)
        self.assertFalse(bc.is_cyclic())

        # Graphe cyclique simple : 0 -> 1 -> 0
        g = open_digraph([0], [1], [
            node(0, "", {1: 1}, {1: 1}),
            node(1, "", {0: 1}, {0: 1})
        ])
        with self.assertRaises(Exception):
            bool_circ(g)  #lève une exception car le graphe est cyclique

        g = open_digraph([0], [2,3], [
            node(0, "~", {}, {1: 1}),
            node(1, "&", {0: 1}, {2:1, 3:1}),
            node(2, "", {1:1}, {}),
            node(3, "", {1:1}, {})

        ])
        with self.assertRaises(Exception):
            bc = bool_circ(g)
        
      
        g = open_digraph([], [], [
            node(0, "", {}, {2: 1}),
            node(1, "", {}, {2: 1}),
            node(2, "", {0: 1, 1: 1}, {})
        ])
        with self.assertRaises(Exception):
            bc = bool_circ(g)

        # Noeud NON mal formé (2 sorties)
        g = open_digraph([], [], [
            node(0, "~", {}, {1: 1, 2: 1}),
            node(1, "", {0: 1}, {}),
            node(2, "", {0: 1}, {})
        ])
        with self.assertRaises(Exception):
            bool_circ(g)

        # Noeud AND sans sortie
        g = open_digraph([], [], [
            node(0, "&", {1: 1, 2: 1}, {}),
            node(1, "", {}, {0: 1}),
            node(2, "", {}, {0: 1})
        ])
        with self.assertRaises(Exception):
            bool_circ(g)

        # Noeud OR bien formé
        g = open_digraph([], [], [
            node(0, "2", {}, {2: 1}),
            node(1, "1", {}, {2: 1}),
            node(2, "|", {0: 1, 1: 1}, {3: 1}),
            node(3, "", {2: 1}, {})
        ])
        bc = bool_circ(g)
        self.assertTrue(True)                     

if __name__ == '__main__':
    unittest.main()
