from open_digraph import *


class bool_circ(open_digraph):
    """Label des noeuds :
    & : ET
    | : OU
    ~ : NON
    '' : copie
    ^  : OU exclusif
    Constantes 0 et 1
    """
    def __init__ (self, g):
        """crée un circuit booléen en utilisant g qui est un open_digraph"""
        super().__init__(g.inputs.copy(), g.outputs.copy(), 
                         [noeud.copy() for noeud in g.nodes.values()])
        self.is_well_formed()
    
    
    def is_cyclic(self):
        """renvoie un booléen si le graphe est cyclique avec l'algorithme du cours"""
        copie=self.copy()
        while copie.get_nodes() != [] : #s'il a encore des noeuds
            feuilles = [n.id for n in copie.get_nodes() if n.outdegree() == 0]
            if feuilles == []: #s'il n'a pas de feuille
                return True
            else:
                id_supp=feuilles[0] #supprime une feuille
                copie.remove_node_by_id(id_supp) #supprime les aretes associées
                del copie.nodes[id_supp] #supprime le noeud
                feuilles.remove(id_supp)
                if id_supp in copie.outputs:
                    copie.outputs.remove(id_supp)
        return False
    
    def is_well_formed(self):
        """vérifie que le circuit booléen est bien formé, lève une exception sinon"""

        if self.is_cyclic():
            raise Exception("le graphe est cyclique")
        for noeud in self.get_nodes():
            if noeud.get_label() == "":
                if noeud.indegree() != 1 :
                    raise Exception ("un noeud copie n'a pas de degré entrant de 1")
            elif noeud.get_label() == "&" or noeud.get_label() == "|":
                if noeud.outdegree() != 1 :
                    raise Exception ("un noeud ET ou OU n'a pas de degré sortant de 1")
            elif noeud.get_label() == "~":
                if noeud.indegree() != 1 or noeud.outdegree() != 1:
                    raise Exception ("un noeud NON ne respecte pas 1 entrée et 1 sortie")

    @classmethod
    def parse_parentheses(cls, s):
        """
        Transforme une chaîne s complètement parenthésée en bool_circ 
        """
        g = bool_circ(open_digraph.empty())  # Circuit vide
        current_node = g.add_node('', {}, {})  # Création du premier noeud vide
        s2 = ''

        for char in s:
            if char == '(': 
                # Ajouter le label accumulé au current_node
                noeud=g.get_node_by_id(current_node)
                noeud.set_label(noeud.get_label()+s2)
                # Créer un nouveau parent
                parent = g.add_node('', {}, {current_node: 1})
                noeud.add_parent_id(parent, 1)
                current_node = parent
                s2 = ''
            elif char == ')':
                # Ajouter le label accumulé au current_node
                noeud=g.get_node_by_id(current_node)
                noeud.set_label(noeud.get_label()+s2)
                # Remonter : current_node devient son unique fils
                children = list(noeud.get_children())
                if len(children)>1:
                    raise Exception("il y a plusieurs enfants")  # Normalement il n'y a qu'un fils
                current_node = children[0]
                s2 = ''
            else:
                s2 += char

        label_to_ids = {} #dictionnaire {label:[id_noeud]}
        for node in g.get_nodes():
            lbl = node.get_label()
            if lbl.startswith("x"):  # On suppose que toutes les variables commencent par "x"
                if lbl not in label_to_ids:
                    label_to_ids[lbl] = []
                label_to_ids[lbl].append(node.get_id())

        inputs = []
        for lbl, ids in label_to_ids.items():
            main_id = ids[0]
            for other_id in ids[1:]:
                g.fusion_nodes(main_id, other_id)  # On fusionne tous les noeuds de même label
            g.get_node_by_id(main_id).set_label('')  # on le met en noeud 'copie'
            inputs.append(lbl)

        g.set_inputs([ids[0] for ids in label_to_ids.values()]) #on récupère les inputs
        return g, inputs
        
        

