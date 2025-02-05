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
        
        #-------------Tests méthodes de suppression-------------
        
        n0 = node(0, 'A', {}, {1: 2, 2: 1})  # 2 arêtes vers 1, 1 arête vers 2
        n1 = node(1, 'B', {0: 2}, {2: 1})  # 2 arêtes venant de 0, 1 arête vers 2
        n2 = node(2, 'C', {0: 1, 1: 1}, {})  # 1 arête venant de 0, 1 arête venant de 1
        
        G = open_digraph([0], [2], [n0, n1, n2])
        
        # Vérification initiale
        assert G.get_node_by_id(0).get_children() == {1: 2, 2: 1}
        assert G.get_node_by_id(1).get_parents() == {0: 2}
        assert G.get_node_by_id(1).get_children() == {2: 1}
        assert G.get_node_by_id(2).get_parents() == {0: 1, 1: 1}
        
        # Test de remove_edge (supprime une occurrence)
        G.remove_edge(0, 1)
        assert G.get_node_by_id(0).get_children() == {1: 1, 2: 1}  # 1 arête restante vers 1
        assert G.get_node_by_id(1).get_parents() == {0: 1}  # 1 arête restante de 0
        
        # Test de remove_parallel_edges (supprime toutes les occurrences)
        G.remove_parallel_edges(0, 1)
        assert G.get_node_by_id(0).get_children() == {2: 1}  # Plus d’arête vers 1
        assert 1 not in G.get_node_by_id(1).get_parents()  # 1 n'a plus 0 comme parent
        
        # Test de remove_node_by_id (supprime les arêtes associées au nœud)
        G.remove_node_by_id(1)
        assert G.get_node_by_id(0).get_children() == {2: 1}  # Plus d’arête vers 1
        assert 1 not in G.get_node_by_id(2).get_parents()  # Plus de lien depuis 1
        assert 1 in G.get_id_node_map()  # Le nœud 1 existe toujours
        
        # Test de remove_edges (supprime plusieurs arêtes individuelles)
        G.add_edge(0, 1)  # Ajout d'une nouvelle arête pour tester
        G.add_edge(1, 2)  # Ajout d'une nouvelle arête pour tester
        G.remove_edges((0, 1), (1, 2))
        assert G.get_node_by_id(0).get_children() == {2: 1}  # L'arête vers 1 supprimée
        assert G.get_node_by_id(1).get_children() == {}  # Plus d'arête vers 2
        
        # Test de remove_several_parallel_edges (supprime toutes les occurrences des arêtes)
        G.add_edge(0, 1)
        G.add_edge(0, 1)
        G.remove_several_parallel_edges((0, 1))
        assert 1 not in G.get_node_by_id(0).get_children()  # Plus d’arête vers 1
   
        
        # Test de remove_nodes_by_id (supprime les arêtes associées aux nœuds)
        G.add_edge(0, 1)
        G.add_edge(2, 1)
        G.remove_nodes_by_id(0, 2)
        assert 0 in G.get_id_node_map()  # Le nœud 0 existe toujours
        assert 2 in G.get_id_node_map()  # Le nœud 2 existe toujours
        assert G.get_node_by_id(0).get_children() == {}  # Plus d'arête sortante de 0
        assert G.get_node_by_id(2).get_parents() == {}  # Plus d'arête entrante vers 2
        
        #------------------------Tests pour add_input_node et add_output_node-------------
        n0 = node(0, 'A', {}, {1: 1})  # Pointe vers 1
        n1 = node(1, 'B', {0: 1}, {})  # Vient de 0
        G = open_digraph([0], [1], [n0, n1])
        
        # Test de add_input_node
        new_input_id = G.add_input_node(0)
        assert new_input_id in G.get_id_node_map()
        assert new_input_id in G.get_input_ids()
        assert G.get_node_by_id(new_input_id).get_children() == {0: 1}
        assert 0 in G.get_node_by_id(0).get_parents()
        
        # Test de add_output_node
        new_output_id = G.add_output_node(1)
        assert new_output_id in G.get_id_node_map()
        assert new_output_id in G.get_output_ids()
        assert G.get_node_by_id(new_output_id).get_parents() == {1: 1}
        assert 1 in G.get_node_by_id(1).get_children()
                

if __name__ == '__main__':
    unittest.main()

