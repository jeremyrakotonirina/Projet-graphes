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


        
        

