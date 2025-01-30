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
        
if __name__ == '__main__':
    unittest.main()

