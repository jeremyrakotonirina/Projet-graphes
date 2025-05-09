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
            elif noeud.get_label() == "&" or noeud.get_label() == "|" or noeud.get_label() == '^':
                if noeud.outdegree() != 1 :
                    raise Exception ("un noeud ET ou OU n'a pas de degré sortant de 1")
            elif noeud.get_label() == "~":
                if noeud.indegree() != 1 or noeud.outdegree() != 1:
                    raise Exception ("un noeud NON ne respecte pas 1 entrée et 1 sortie")
            elif noeud.get_label() == "0" or noeud.get_label() == "1" : 
                if noeud.outdegree() != 1 or noeud.indegree() !=0 : 
                    raise Exception(f"le noeud {noeud.get_label()} doit avoir indegree=0 et outdegree=1")
    

    @classmethod
    def parse_parentheses(cls, *args):
        """
        Transforme une chaîne s complètement parenthésée en bool_circ 
        """
        g = bool_circ(open_digraph.empty())  # Circuit vide

        for chaine in args:
            current_node = g.add_node('', {}, {})  # Création du premier noeud vide
            s2 = ''
            for char in chaine:
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

        g.set_input_ids([ids[0] for ids in label_to_ids.values()]) #on récupère les inputs
        return g, inputs

    
    @classmethod
    def random_bool_circ(cls,n: int,
                         borne: int,
                         nb_entrees: int = None,
                         nb_sorties: int = None,
                         operateurs_binaires=('&', '|', '^'),
                         operateurs_unaires=('~',)):
        """
        Génère un circuit booléen aléatoire : n noeuds internes, multiplicité max borne.
        """
        if not operateurs_unaires:
            raise IndexError("Liste des opérateurs unaires vide")

        graphe = open_digraph.empty().random(n, borne, inputs=0, outputs=0, form="loop-free DAG")
        print('Graphe initial :', graphe)

        for nd in list(graphe.get_nodes()):
            if nd.indegree() == 0:
                graphe.add_input_node(nd.id)
            if nd.outdegree() == 0:
                graphe.add_output_node(nd.id)

        if nb_entrees is not None:
            while len(graphe.inputs) < nb_entrees:
                candidats = [nd.id for nd in graphe.get_nodes() if nd.id not in graphe.inputs]
                if not candidats:
                    break
                cible = random.choice(candidats)
                graphe.add_input_node(cible)
            while len(graphe.inputs) > nb_entrees:
                p, q = random.sample(graphe.inputs, 2)
                nouvel_entree = graphe.add_node(label="")
                graphe.add_input_id(nouvel_entree)
                graphe.add_edge(nouvel_entree, p)
                graphe.add_edge(nouvel_entree, q)
                graphe.inputs.remove(p)
                graphe.inputs.remove(q)

        if nb_sorties is not None:
            while len(graphe.outputs) < nb_sorties:
                candidats = [nd.id for nd in graphe.get_nodes() if nd.id not in graphe.outputs]
                if not candidats:
                    break
                cible = random.choice(candidats)
                graphe.add_output_node(cible)
            while len(graphe.outputs) > nb_sorties:
                p, q = random.sample(graphe.outputs, 2)
                nouvelle_sortie = graphe.add_node(label="")
                graphe.add_output_id(nouvelle_sortie)
                graphe.add_edge(p, nouvelle_sortie)
                graphe.add_edge(q, nouvelle_sortie)
                graphe.outputs.remove(p)
                graphe.outputs.remove(q)

        for nd in graphe.get_nodes():
            if nd.indegree() > 0 and nd.outdegree() > 0:
                nd.set_label("")
            else:
                nd.set_label("  ")

        for nd in list(graphe.get_nodes()):
            deg_entree, deg_sortie = nd.indegree(), nd.outdegree()
            parents = list(nd.get_parents().keys())
            enfants = list(nd.get_children().keys())

            if deg_entree == 1 and deg_sortie == 1:
                nd.set_label(random.choice(operateurs_unaires))
            elif deg_entree > 1 and deg_sortie == 1:
                nd.set_label(random.choice(operateurs_binaires))
            elif deg_entree > 1 and deg_sortie > 1:
                for p in parents:
                    graphe.remove_several_parallel_edges((p, nd.id))
                for c in enfants:
                    graphe.remove_several_parallel_edges((nd.id, c))
                op_noeud = graphe.add_node(label=random.choice(operateurs_binaires))
                for p in parents:
                    graphe.add_edge(p, op_noeud)
                graphe.add_edge(op_noeud, nd.id)
                for c in enfants:
                    graphe.add_edge(nd.id, c)

        return cls(graphe)
    
    
    
    @classmethod
    def adder(cls, n: int):
        if n == 0:
            g = open_digraph.empty()
            id_Cin = g.add_node(label="Cin")
            id_A0  = g.add_node(label="A0")
            id_B0  = g.add_node(label="B0")
            g.add_input_id(id_Cin)
            g.add_input_id(id_A0)
            g.add_input_id(id_B0)

            xor1 = g.add_node(label="^")
            g.add_edge(id_A0, xor1); g.add_edge(id_B0, xor1)

            and1 = g.add_node(label="&"); g.add_edge(id_A0, and1); g.add_edge(id_B0, and1)
            copie1 = g.add_node(label=""); g.add_edge(xor1, copie1)
            copie2 = g.add_node(label=""); g.add_edge(id_Cin, copie2)
            and2 = g.add_node(label="&"); g.add_edge(copie1, and2); g.add_edge(copie2, and2)
            xor2 = g.add_node(label="^"); g.add_edge(copie1, xor2); g.add_edge(copie2, xor2)

            id_S0 = g.add_node(label="S0")
            g.add_edge(xor2, id_S0)
            g.add_output_id(id_S0)

            or1 = g.add_node(label="|")
            g.add_edge(and1, or1); g.add_edge(and2, or1)
            id_Cout = g.add_node(label="Cout")
            g.add_edge(or1, id_Cout)
            g.add_output_id(id_Cout)

            return cls(g)

        else:
            low = cls.adder(n - 1)
            high = cls.adder(n - 1)

            m = (len(low.inputs) - 1) // 2

            high_input_labels = ['Cin']
            for j_idx in range(m):
                high_input_labels.append(f"A{j_idx+m}")
                high_input_labels.append(f"B{j_idx+m}")
            for nid, lbl in zip(high.inputs, high_input_labels):
                high.get_node_by_id(nid).set_label(lbl)

            high_output_labels = [f"S{j+m}" for j in range(m)] + ["Cout"]
            for nid, lbl in zip(high.outputs, high_output_labels):
                high.get_node_by_id(nid).set_label(lbl)

            high.get_node_by_id(high.inputs[0]).set_label("")  

            comp = low.parallel(high)

            cout_low = low.outputs[-1]
            idxcin_high = len(low.inputs)
            cinx= comp.inputs[idxcin_high]
            comp.add_edge(cout_low, cinx)

            new_ins = comp.inputs.copy()
            new_ins.pop(idxcin_high)
            comp.set_input_ids(new_ins)
            
            new_outs = comp.outputs.copy()
            idxclo = len(low.outputs) - 1
            new_outs.pop(idxclo)
            comp.set_output_ids(new_outs)

            return cls(comp)


    @classmethod
    def half_adder(cls, n: int) :
        """
        On part de Adder_n, puis on remplace la retenue dentrée initiale
        (Cin du bit de poids faible) par une constante 0.
        """
        g = cls.adder(n)
        zero = g.get_node_by_id(g.inputs[0])
        zero.set_label("0")
        return cls(g)
    
    @classmethod
    def registre_entier(cls, value: int, size: int = 8):
        """
        Retourne un circuit qui produit en sortie la représentation binaire
        de 'value' par rapoerr a 'size' bits
        """
        if value < 0 or value >= 2**size:
            raise ValueError(f"Impossible dencoder {value} avec {size} bits.")
        if size < 1:
            raise ValueError(f"Impossible d’avoir une taille de registre < 1 : size = {size}")
        g = open_digraph.empty()
        bits = bin(value)[2:].zfill(size)  
        for b in bits:
            const_id = g.add_node(label=b)       
            g.add_output_node(const_id)          

        return cls(g)
    
    def simplif_or_const(self, id_or: int, id_const: int) -> int:
        """
        Simplifie une porte OR qui a au moins un parent constant (0 ou 1), pour toute 

        Arguments :
            id_or     ID  OR
            id_const ID  constant ("0" ou "1")

        Retourne lID du noeud qui remplace OR (ou id_or si on garde la porte).
        """
        or_node = self.get_node_by_id(id_or)
        parents = list(or_node.get_parents().keys())
        others  = [p for p in parents if p != id_const]
        lbl     = self.get_node_by_id(id_const).get_label()

        if lbl == "1":
            id_replace = id_const

        else:  
            if len(others) > 1:
                self.remove_edge(id_const, id_or)
                # supprimer 0 s’il n’a plus d’enfant
                if not self.get_node_by_id(id_const).get_children():
                    self.remove_node_by_id(id_const)
                    del self.nodes[id_const]

                return id_or

            elif len(others) == 1:
                id_replace = others[0]
            else:
                id_replace = id_const
        for child_id, mult in list(or_node.get_children().items()):
            for _ in range(mult):
                self.add_edge(id_replace, child_id)
            for _ in range(mult):
                self.remove_edge(id_or, child_id)
        for p in parents:
            self.remove_edge(p, id_or)

        self.remove_node_by_id(id_or)
        del self.nodes[id_or]

        if lbl == "0" and id_replace != id_const:
            if id_const in self.get_id_node_map() and not self.get_node_by_id(id_const).get_children():
                self.remove_node_by_id(id_const)
                del self.nodes[id_const]

        return id_replace
    

    def simplify_copies_const(self, id_copy: int, id_const: int) -> int:
        """
        Simplifie un noeud de copie alimenté par une constante.
        Pour chaque arc du noeud copie, on crée un nouveau
        noeud constant identique et on le branche à lenfant.
        Puis on supprime le nœud copie et, sil nest plus utilisé,
        le noeud constant dorigine.
        Retourne lID du constant dorigine (ou None si supprimé).
        """
        const = self.get_node_by_id(id_const)
        lbl = const.get_label()
        if lbl not in {'0', '1'}:
            raise ValueError("id_const doit être '0' ou '1'")

        copy = self.get_node_by_id(id_copy)
        for child_id, mult in list(copy.get_children().items()):
            for _ in range(mult):
                new_c = self.add_node(label=lbl)
                self.add_edge(new_c, child_id)

        self.remove_node_by_id(id_copy)
        del self.nodes[id_copy]

        # si le constant d’origine n’a plus d’enfants, on l’enlève aussi
        if not const.get_children():
            self.remove_node_by_id(id_const)
            del self.nodes[id_const]
            return None

        return id_const

    

    def simplify_non_const(self, id_not: int, id_const: int) -> int:
        """
        Simplifie une porte NON  :

        Args:
            id_not    ID du neud NON 
            id_const ID du noeud constant (étiquette '0' ou '1') en entrée de id_not
        Retourne lID du noeud constant qui remplace la porte NON.
        """
        not_node = self.get_node_by_id(id_not)
        if not_node.get_label() != "~":
            raise ValueError("id_not doit être une porte NON (~)")

        parents = list(not_node.get_parents().keys())
        if parents != [id_const]:
            raise ValueError("id_const doit être l’unique parent de la porte NON")
        
        const_node = self.get_node_by_id(id_const)
        lbl = const_node.get_label()
        if lbl not in {"0", "1"}:
            raise ValueError("id_const doit être un nœud constant '0' ou '1'")
        new_lbl = "1" if lbl == "0" else "0"
        id_new_const = self.add_node(label=new_lbl)
        for child_id, mult in list(not_node.get_children().items()):
            for _ in range(mult):
                self.add_edge(id_new_const, child_id)
        self.remove_edge(id_const, id_not)
        self.remove_node_by_id(id_not)
        del self.nodes[id_not]
        if not const_node.get_children():
            self.remove_node_by_id(id_const)
            del self.nodes[id_const]

        return id_new_const

    def simplify_et_const(self, id_and: int, id_const: int) -> int:
        """
        Simplifie une porte ET (&) alimentée par une constante :

        Args:
            id_and    ID du noeuud ET (&)
            id_const  ID du noeud constant ('0' ou '1') en entrée de la porte
        Retourne lID duoeurd qui remplace la porte ET.
        """
        and_node = self.get_node_by_id(id_and)
        if and_node.get_label() != "&":
            raise ValueError("id_and doit être une porte ET (&)")

        const_node = self.get_node_by_id(id_const)
        lbl = const_node.get_label()
        if lbl not in {"0", "1"}:
            raise ValueError("id_const doit être un nœud constant '0' ou '1'")

        parents = list(and_node.get_parents().keys())
        others = [p for p in parents if p != id_const]

        if lbl == "0":
            id_replace = id_const

        else: 
            if len(others) > 1:
                self.remove_edge(id_const, id_and)
                if not const_node.get_children():
                    self.remove_node_by_id(id_const)
                    del self.nodes[id_const]
                return id_and
            elif len(others) == 1:
                id_replace = others[0]
            else: 
                id_replace = id_const
        for child_id, mult in list(and_node.get_children().items()):
            for _ in range(mult):
                self.add_edge(id_replace, child_id)
        for p in parents:
            self.remove_edge(p, id_and)

        self.remove_node_by_id(id_and)
        del self.nodes[id_and]

        if lbl == "1" and id_replace != id_const:
            if id_const in self.get_id_node_map() and not const_node.get_children():
                self.remove_node_by_id(id_const)
                del self.nodes[id_const]

        return id_replace

    def simplify_ou_exclusive(self, id_xor: int, id_const: int) -> int:
        """
        Simplifie une porte OU exclusif  alimentée par une constante :

        Retourne lID du nœud remplaçant (XOR, variable, NOT ou constant).
        """
        xor_node = self.get_node_by_id(id_xor)
        if xor_node.get_label() != "^":
            raise ValueError("id_xor doit être une porte ^")
        const_node = self.get_node_by_id(id_const)
        lbl = const_node.get_label()
        if lbl not in {"0", "1"} or id_const not in xor_node.get_parents():
            raise ValueError("id_const doit être un parent constant '0' ou '1'")
        parents = list(xor_node.get_parents().keys())
        others = [p for p in parents if p != id_const]
        children = list(xor_node.get_children().items())

        if lbl == "0":
            if len(others) > 1:
                self.remove_edge(id_const, id_xor)
                if not const_node.get_children():
                    self.remove_node_by_id(id_const)
                    del self.nodes[id_const]
                return id_xor
            if len(others) == 1:
                rep = others[0]
            else:
                return id_const
            for child_id, m in children:
                for _ in range(m):
                    self.add_edge(rep, child_id)
            for p in parents:
                self.remove_edge(p, id_xor)
            self.remove_node_by_id(id_xor)
            del self.nodes[id_xor]
            if not const_node.get_children():
                self.remove_node_by_id(id_const)
                del self.nodes[id_const]
            return rep

        else :
            self.remove_edge(id_const, id_xor)
            id_not = self.add_node(label="~")
            for child_id, m in children:
                for _ in range(m):
                    self.remove_edge(id_xor, child_id)
                for _ in range(m):
                    self.add_edge(id_xor, id_not)
                    self.add_edge(id_not, child_id)
            if not const_node.get_children():
                self.remove_node_by_id(id_const)
                del self.nodes[id_const]
        return id_not

    

    def simplif_and_const(self, id_and: int, id_const: int) -> int:
        """
        Simplifie une porte AND qui a au moins un parent constant (0 ou 1), pour toute arité )

        Arguments :
            id_and     ID  AND
            id_const  ID constant ("0" ou "1")
            
            Retourne lID du nœud qui remplace AND (ou id_and si on garde la porte).
        """
        and_node = self.get_node_by_id(id_and)
        if and_node.get_label() != '&':
            return id_and 
            
        const_node = self.get_node_by_id(id_const)
        const_label = const_node.get_label()

        if const_label not in ('0', '1'):
            raise ValueError(f"Le noeud {id_const} avec label {const_label} n'est pas une constante '0' ou '1'.")

        parents_ids = list(and_node.get_parents().keys())
        other_parents_ids = [p_id for p_id in parents_ids if p_id != id_const]
        noeud_remplac = -1 
        if const_label == '0':
            noeud_remplac = id_const
        elif const_label == '1':
            if not other_parents_ids:
                noeud_remplac = id_const
            elif len(other_parents_ids) == 1:
                noeud_remplac = other_parents_ids[0]
            else:
                self.remove_edge(id_const, id_and)
                if not const_node.get_children() and id_const not in self.outputs:
                    for p_id in list(const_node.get_parents().keys()):
                        self.remove_edge(p_id, id_const)
                    if id_const in self.nodes:
                         del self.nodes[id_const]
                    if id_const in self.inputs:
                        self.inputs.remove(id_const)
                return id_and 
            
        enfantdebase = dict(and_node.get_children())
        for child_id, mult in enfantdebase.items():
            for _ in range(mult):
                self.add_edge(noeud_remplac, child_id)

        for p_id in list(and_node.get_parents().keys()):
            edgeasupp = and_node.get_parents().get(p_id, 0)
            for _ in range(edgeasupp):
                self.remove_edge(p_id, id_and)

        for enfantamaj in list(enfantdebase.keys()):
            noeudamaj = self.get_node_by_id(enfantamaj)
            if noeudamaj and id_and in noeudamaj.get_parents():
                originenfant= enfantdebase[enfantamaj]
                for _ in range(originenfant):
                    self.remove_edge(id_and, enfantamaj)

        if id_and in self.nodes:
            del self.nodes[id_and]
        if id_and in self.inputs:
            self.inputs.remove(id_and)
        if id_and in self.outputs:
            self.outputs = [noeud_remplac if o_id == id_and else o_id for o_id in self.outputs]

        assup = True
        if noeud_remplac == id_const:
            assup = False # La constante est le noeud de remplacement, ne pas la supprimer
        
        if assup and id_const in self.nodes:
            node_a_verif = self.get_node_by_id(id_const)
            if node_a_verif and not node_a_verif.get_children() and id_const not in self.outputs:
                # Suppression manuelle de id_const
                for p in list(node_a_verif.get_parents().keys()): # Devrait être vide pour une constante
                    numarete = node_a_verif.get_parents().get(p, 0)
                    for _ in range(numarete):
                        self.remove_edge(p, id_const)
                if id_const in self.nodes: # Revérifier car remove_edge peut l'avoir affecté
                    del self.nodes[id_const]
                if id_const in self.inputs:
                    self.inputs.remove(id_const)
        
        return noeud_remplac
    
    def simplif_not_const(self, id_not: int) -> int:
        """
        Simplifie une porte NOT dont l_parent est une constante (0 ou 1).

        Retourne lID du noeud constant qui remplace la porte NOT.
        """
        not_node = self.get_node_by_id(id_not)
        if not_node.get_label() != '~':
            return id_not 

        parents_ids = list(not_node.get_parents().keys())
        if not parents_ids:
            return id_not 
        
        parent_id = parents_ids[0]
        parent_node = self.get_node_by_id(parent_id)
        parent_label = parent_node.get_label()

        noeud_remplac = -1

        if parent_label == '0':
            not_node.set_label('1')
            noeud_remplac = id_not 
            self.remove_edge(parent_id, id_not)
            # Si le parent 0 n_a plus d_enfants et n_est pas une sortie, le supprimer
            if not parent_node.get_children() and parent_id not in self.outputs:
                # Suppression manuelle
                if parent_id in self.nodes:
                    del self.nodes[parent_id]
                if parent_id in self.inputs:
                    self.inputs.remove(parent_id)

        elif parent_label == '1':
            not_node.set_label('0')
            noeud_remplac = id_not
            # Supprimer l_ancienne connexion au parent 1
            self.remove_edge(parent_id, id_not)

            if not parent_node.get_children() and parent_id not in self.outputs:
                # Suppression manuelle
                if parent_id in self.nodes:
                    del self.nodes[parent_id]
                if parent_id in self.inputs:
                    self.inputs.remove(parent_id)
        else:
            # Le parent nest pas une constante, on ne peut pas simplifier ici.
            return id_not
        not_node = self.get_node_by_id(id_not)
        if not_node.get_label() != '~':
            return id_not

        parents_ids = list(not_node.get_parents().keys())
        if not parents_ids:
            return id_not
        
        parent_id = parents_ids[0]
        parent_node = self.get_node_by_id(parent_id)
        parent_label = parent_node.get_label()

        new_const_label = ""
        if parent_label == '0':
            new_const_label = '1'
        elif parent_label == '1':
            new_const_label = '0'
        else:
            return id_not 

        not_node.set_label(new_const_label) # id_not devient le noeud constant de remplacement
        self.remove_edge(parent_id, id_not) 

    
        if parent_id in self.nodes: 
            pearent_a_verif = self.get_node_by_id(parent_id)
            if not pearent_a_verif.get_children() and parent_id not in self.outputs:
                for p in list(pearent_a_verif.get_parents().keys()):
                    self.remove_edge(p, parent_id)
                # Ensuite, supprimer le noeud lui-même
                if parent_id in self.nodes:
                    del self.nodes[parent_id]
                if parent_id in self.inputs: 
                    self.inputs.remove(parent_id)

        return id_not 

    def simplif_xor_const(self, id_xor: int, id_const: int) -> int:
        xor_node = self.get_node_by_id(id_xor)
        if not xor_node or xor_node.get_label() != "^":
            return id_xor

        const_node = self.get_node_by_id(id_const)
        if not const_node:
             return id_xor 
        const_label = const_node.get_label()
        if const_label not in ("0", "1"):
            raise ValueError(f"Le noeud {id_const} n'est pas une constante 0 ou 1.")

        parents_ids = list(xor_node.get_parents().keys())
        autreparent = [p_id for p_id in parents_ids if p_id != id_const]

        id_replacement_node = -1 
        passup = -1    

        if not autreparent:
            id_replacement_node = id_const
        elif len(autreparent) > 1:
            return id_xor
        else:
            autreparentid = autreparent[0]
            autreparentnoeud = self.get_node_by_id(autreparentid)
            if not autreparentnoeud:
                return id_xor 

            if const_label == "0":
                id_replacement_node = autreparentid
            else: # const_label == "1"
                if autreparentnoeud.get_label() == "~":
                    grand_parents_ids = list(autreparentnoeud.get_parents().keys())
                    if grand_parents_ids:
                        id_replacement_node = grand_parents_ids[0]
                        passup = autreparentid
                    else:
                        pass 
                
                if id_replacement_node == -1:
                    id_new_not = self.add_node(label="~")
                    self.add_edge(autreparentid, id_new_not)
                    id_replacement_node = id_new_not
        
        if id_replacement_node == -1:
            return id_xor

        enfantori = dict(xor_node.get_children()) 
        for child_id, mult in enfantori.items():
            for _ in range(mult):
                self.add_edge(id_replacement_node, child_id)

        for p_id in list(xor_node.get_parents().keys()):
            numarete = xor_node.get_parents()[p_id]
            for _ in range(numarete):
                self.remove_edge(p_id, id_xor)

        for child_id in list(enfantori.keys()):
            child_node = self.get_node_by_id(child_id)
            if child_node and id_xor in child_node.get_parents():
                arete_enf = enfantori[child_id]
                for _ in range(arete_enf):
                    self.remove_edge(id_xor, child_id)

        if id_xor in self.nodes:
            del self.nodes[id_xor]
        if id_xor in self.inputs: self.inputs.remove(id_xor)
        if id_xor in self.outputs:
            self.outputs = [id_replacement_node if o_id == id_xor else o_id for o_id in self.outputs]

        noeud_averif = self.get_node_by_id(id_const)
        if noeud_averif and not noeud_averif.get_children() and id_const not in self.outputs:
            for p_id_of_const in list(noeud_averif.get_parents().keys()):
                arete_parent = noeud_averif.get_parents().get(p_id_of_const, 0)
                for _ in range(arete_parent):
                    self.remove_edge(p_id_of_const, id_const)
            if id_const in self.nodes: del self.nodes[id_const]
            if id_const in self.inputs: self.inputs.remove(id_const)

        if passup != -1 and passup in self.nodes:
            passupnoeud = self.get_node_by_id(passup)
            if passupnoeud and not passupnoeud.get_children() and passup not in self.outputs:
                for p_of_not_id in list(passupnoeud.get_parents().keys()):
                     numaretepasparent = passupnoeud.get_parents().get(p_of_not_id, 0)
                     for _ in range(numaretepasparent):
                        self.remove_edge(p_of_not_id, passup)
                
                if passup in self.nodes: del self.nodes[passup]
                if passup in self.inputs: self.inputs.remove(passup)
        
        return id_replacement_node

    def simplify_copy_node(self, id_copy: int) -> int:
        """
        Simplifie un noeud de copie (label=\"") qui a exactement un parent et un enfant.
        La règle est Copie(X) -> X, ce qui signifie que le noeud copie est supprimé
        et son parent est directement connecté à son enfant.
        Si le noeud copie a plusieurs enfants, cette règle simple ne s_applique pas directement
        de cette manière (il faudrait dupliquer le parent ou la structure en amont).
        Cette méthode gère le cas simple 1 parent, 1 enfant pour le noeud copie.


        Retourne lid du parent si la simplification a eu lieu, sinon id_copy.
        """
        copy_node = self.get_node_by_id(id_copy)
        if copy_node.get_label() != "":
            return id_copy # Pas un noeud copie

        parents = list(copy_node.get_parents().keys())
        children = list(copy_node.get_children().keys())

        if len(parents) == 1 and len(children) == 1:
            parent_id = parents[0]
            child_id = children[0]
            
            self.add_edge(parent_id, child_id) # Utilise la multiplicité de l_arc entrant

            # Supprimer les anciennes arêtes
            self.remove_edge(parent_id, id_copy)
            self.remove_edge(id_copy, child_id)

            # Supprimer le noeud copie manuellement
            if id_copy in self.nodes:
                del self.nodes[id_copy]
            if id_copy in self.inputs: self.inputs.remove(id_copy)
            if id_copy in self.outputs: 
                # Si la copie était une sortie, son parent devient la sortie
                self.outputs = [parent_id if o_id == id_copy else o_id for o_id in self.outputs]
            
            return parent_id 
        return id_copy # Pas de simplification applicable



    def evaluate(self, input_values: dict) -> None:
        """
        Évalue le circuit booléen avec les valeurs d'entrée fournies.
        Les valeurs d'entrée sont propagées et le circuit est simplifié
        en appliquant les règles de la Table du TD11.

        Arguments:
            input_values:Un dictionnaire où les clés sont les labels des entré et kes valeurs sont "0" ou "1".
        """
        for node_id in list(self.inputs): 
            if node_id not in self.nodes: continue
            node = self.get_node_by_id(node_id)
            node_label = node.get_label()
            if node_label in input_values:
                const_value = input_values[node_label]
                node.set_label(const_value)
        changementrecursif = True
        while changementrecursif:
            changementrecursif = False
            iddenoeud = list(self.nodes.keys()) 
            for node_id in iddenoeud:
                if node_id not in self.nodes: # Le noeud a pu être supprimé
                    continue
                node = self.get_node_by_id(node_id)
                noeuddorigine = node.get_label()
                actionffaite = False
                if noeuddorigine in ("&", "|", "^", "~"):
                    parent_avant_simplif = dict(node.get_parents()) # Copie des parents
                    parenttrouvé = -1
                    for p_id in parent_avant_simplif.keys():
                        if p_id not in self.nodes: continue
                        parent_node = self.get_node_by_id(p_id)
                        if parent_node.get_label() in ("0", "1"):
                            parenttrouvé = p_id
                            break
                    
                    if parenttrouvé != -1:
                        num_nodes_before = len(self.nodes)
                        children_before = dict(node.get_children()) if node_id in self.nodes else {}
                        parents_before = dict(node.get_parents()) if node_id in self.nodes else {}

                        if noeuddorigine == "&":
                            self.simplif_and_const(node_id, parenttrouvé)
                            actionffaite = True
                        elif noeuddorigine == "|":
                            self.simplif_or_const(node_id, parenttrouvé)
                            actionffaite = True
                        elif noeuddorigine == "^":
                            self.simplif_xor_const(node_id, parenttrouvé)
                            actionffaite = True
                        
                        if actionffaite:
                            # Vérifier si un changement a eu lieu
                            if node_id not in self.nodes or len(self.nodes) < num_nodes_before:
                                changementrecursif = True
                            elif node_id in self.nodes: # Le noeud existe toujours
                                current_node_after = self.get_node_by_id(node_id)
                                if current_node_after.get_label() != noeuddorigine or current_node_after.get_parents() != parents_before or current_node_after.get_children() != children_before:
                                    changementrecursif = True
                            if changementrecursif: break # Sortir de la boucle for des noeuds, et refaire un etour

                    elif noeuddorigine == "~": # Porte NOT, vérifier son unique parent
                        if parent_avant_simplif: 
                            parent_id = list(parent_avant_simplif.keys())[0]
                            if parent_id in self.nodes:
                                parent_node = self.get_node_by_id(parent_id)
                                if parent_node.get_label() in ("0", "1"):
                                    label_avant = node.get_label()
                                    self.simplif_not_const(node_id)
                                    actionffaite = True
                                    if node_id not in self.nodes or (node_id in self.nodes and self.get_node_by_id(node_id).get_label() != label_avant):
                                        changementrecursif = True
                                        break 
                
                if changementrecursif and actionffaite : continue 
                if node_id in self.nodes and self.get_node_by_id(node_id).get_label() == "": 
                    node_copy = self.get_node_by_id(node_id)
                    parents_of_copy = list(node_copy.get_parents().keys())
                    noeudcopieavantsipmlif = len(self.nodes)

                    if parents_of_copy:
                        parent_id = parents_of_copy[0]
                        if parent_id in self.nodes:
                            parent_node = self.get_node_by_id(parent_id)
                            if parent_node.get_label() in ("0", "1"):
                                self.simplify_copies_const(node_id, parent_id)
                                actionffaite = True
                                if node_id not in self.nodes or len(self.nodes) < noeudcopieavantsipmlif:
                                    changementrecursif = True
                                    break
                    
                    if changementrecursif and actionffaite : continue

                    if node_id in self.nodes:
                        valretour = self.simplify_copy_node(node_id)
                        actionffaite = True 
                        
                        if node_id not in self.nodes:
                            changementrecursif = True
                            break 
            if changementrecursif:
                continue

        
