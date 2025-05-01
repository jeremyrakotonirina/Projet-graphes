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

        g.set_inputs([ids[0] for ids in label_to_ids.values()]) #on récupère les inputs
        return g, inputs

    @classmethod
    def random_bool_circ(cls,
                         n: int,
                         bound: int,
                         nb_inputs: int = None,
                         nb_outputs: int = None,
                         operateurs_binaires=('&', '|', '^'),
                         operateurs_unaires=('~',)):
        """
        Génère un circuit booléen aléatoire :
         - n            : nombre de noeuds internes
         - bound        : multiplicité max des arêtes
         - nb_inputs    : nombre d'entrées souhaité (None → pas d'ajustement)
         - nb_outputs   : nombre de sorties souhaité (None → pas d'ajustement)
         - operateurs_binaires : labels pour portes binaires
         - operateurs_unaires  : labels pour portes unaires
        """
        # 0) Validation des opérateurs unaire
        if not operateurs_unaires:
            raise IndexError("liste des operateurs unaires vide")

        # 1) Générer le squelette DAG
        base = open_digraph.empty().random(
            n, bound,
            inputs=0,
            outputs=0,
            form="loop-free DAG"
        )
        print('voici le gaphe du nv circuit avant ')
        print(base)
        #base.display()

        # 2) Créer de vrais inputs/outputs là où il n'y en a pas
        for u in list(base.get_nodes()):
            if u.indegree() == 0:
                base.add_input_node(u.id)
            if u.outdegree() == 0:
                base.add_output_node(u.id)

        # ——— 2bis) Ajuster au nombre voulu d'entrées/sorties ———
        # Entrées
        if nb_inputs is not None:
            # augmenter si besoin
            while len(base.inputs) < nb_inputs:
                # choisir un noeud non-input
                candidats = [u.id for u in base.get_nodes() if u.id not in base.inputs]
                if not candidats:
                    break
                cible = random.choice(candidats)
                base.add_input_node(cible)
            # diminuer si trop d'inputs
            while len(base.inputs) > nb_inputs:
                # fusionner deux inputs au hasard
                p, q = random.sample(base.inputs, 2)
                new_in = base.add_node(label="")
                base.add_input_id(new_in)
                base.add_edge(new_in, p)
                base.add_edge(new_in, q)
                base.inputs.remove(p)
                base.inputs.remove(q)

        # Sorties
        if nb_outputs is not None:
            # augmenter si besoin
            while len(base.outputs) < nb_outputs:
                candidats = [u.id for u in base.get_nodes() if u.id not in base.outputs]
                if not candidats:
                    break
                cible = random.choice(candidats)
                base.add_output_node(cible)
            # diminuer si trop d'outputs
            while len(base.outputs) > nb_outputs:
                p, q = random.sample(base.outputs, 2)
                new_out = base.add_node(label="")
                base.add_output_id(new_out)
                base.add_edge(p, new_out)
                base.add_edge(q, new_out)
                base.outputs.remove(p)
                base.outputs.remove(q)
        # ————————————————————————————————————————————————

        # 3) Initialiser les labels internes
        for u in base.get_nodes():
            if u.indegree() > 0 and u.outdegree() > 0:
                u.set_label("")    # nœud interne
            else:
                u.set_label("  ")  # dummy input/output

        # 4) Étiquetage et split
        for u in list(base.get_nodes()):
            d_in, d_out = u.indegree(), u.outdegree()
            parents = list(u.get_parents().keys())
            enfants = list(u.get_children().keys())

            # porte unaire
            if d_in == 1 and d_out == 1:
                u.set_label(random.choice(operateurs_unaires))

            # noeud copie (1 entrée, >1 sorties) – on laisse le label vide
            elif d_in == 1 and d_out > 1:
                continue

            # porte binaire
            elif d_in > 1 and d_out == 1:
                u.set_label(random.choice(operateurs_binaires))

            # split fan-in>1 et fan-out>1
            elif d_in > 1 and d_out > 1:
                # retirer toutes les arêtes parallèles
                for p in parents:
                    base.remove_several_parallel_edges((p, u.id))
                for c in enfants:
                    base.remove_several_parallel_edges((u.id, c))
                # créer le noeud opérateur binaire
                u_op = base.add_node(label=random.choice(operateurs_binaires))
                # reconnecter parents → u_op
                for p in parents:
                    base.add_edge(p, u_op)
                # reconnecter u_op → u
                base.add_edge(u_op, u.id)
                # reconnecter u → anciens enfants
                for c in enfants:
                    base.add_edge(u.id, c)

        # 5) Retourner l’instance validée (vérifie la forme)
        return cls(base)
    
    
    
    @classmethod
    def adder(cls, n: int) -> "bool_circ":
        """
        Construire récursivement Adder_n :
        - n == 0 : full-adder 1-bit
        - n > 0 : ripple carry de deux Adder_{n-1}, avec renommage des indices
        """
        # --- Cas de base : full-adder 1-bit ---
        if n == 0:
            g = open_digraph.empty()

            # 1) Création des ports d’entrée
            id_Cin = g.add_node(label="Cin")
            id_A0  = g.add_node(label="A0")
            id_B0  = g.add_node(label="B0")
            g.add_input_id(id_Cin)
            g.add_input_id(id_A0)
            g.add_input_id(id_B0)

            # 2) Chaîne de XOR pour S0 = (A0 ⊕ B0) ⊕ Cin
            xor1 = g.add_node(label="^")
            g.add_edge(id_A0, xor1); g.add_edge(id_B0, xor1)
            xor2 = g.add_node(label="^")
            g.add_edge(xor1, xor2); g.add_edge(id_Cin, xor2)

            # 3) Sortie S0
            id_S0 = g.add_node(label="S0")
            g.add_edge(xor2, id_S0)
            g.add_output_id(id_S0)

            # 4) Trois AND pour les produits partiels
            and1 = g.add_node(label="&"); g.add_edge(id_A0, and1); g.add_edge(id_B0, and1)
            and2 = g.add_node(label="&"); g.add_edge(id_A0, and2); g.add_edge(id_Cin, and2)
            and3 = g.add_node(label="&"); g.add_edge(id_B0, and3); g.add_edge(id_Cin, and3)

            # 5) OR final pour la retenue Cout
            or1 = g.add_node(label="|")
            g.add_edge(and1, or1); g.add_edge(and2, or1); g.add_edge(and3, or1)
            id_Cout = g.add_node(label="Cout")
            g.add_edge(or1, id_Cout)
            g.add_output_id(id_Cout)

            return cls(g)

        # --- Cas récursif : ripple carry de deux Adder_{n-1} ---
        low  = cls.adder(n-1)
        high = cls.adder(n-1)

        # nombre de bits gérés par chaque sous‐adder
        m = (len(low.inputs) - 1) // 2

        # ── Renommage des ports du sous‐adder "high" ──
        # high.inputs = [Cin_high, A0…A_{m-1}, B0…B_{m-1}]
        cin_high_id, *rest = high.inputs
        a_high_ids = rest[:m]
        b_high_ids = rest[m:]

        for j, aid in enumerate(a_high_ids):
            high.get_node_by_id(aid).set_label(f"A{j + m}")
        for j, bid in enumerate(b_high_ids):
            high.get_node_by_id(bid).set_label(f"B{j + m}")

        # high.outputs = [S0…S_{m-1}, Cout_high]
        s_high_ids = high.outputs[:-1]
        for j, sid in enumerate(s_high_ids):
            high.get_node_by_id(sid).set_label(f"S{j + m}")

        # rendre "Cin_high" muet (noeud interne)
        high.get_node_by_id(cin_high_id).set_label("")

        # 1) Juxtaposition parallèle
        comp = low.parallel(high)

        # 2) Relier Cout_low → Cin_high
        cout_low = low.outputs[-1]
        idx_cin_high = len(low.inputs)
        cin_high_in_comp = comp.inputs[idx_cin_high]
        comp.add_edge(cout_low, cin_high_in_comp)

        # 3) Retirer Cin_high des ports externes
        new_ins = comp.inputs.copy()
        new_ins.pop(idx_cin_high)
        comp.set_inputs(new_ins)

        # 4) Retirer Cout_low des sorties intermédiaires
        new_outs = comp.outputs.copy()
        idx_cout_low = len(low.outputs) - 1
        new_outs.pop(idx_cout_low)
        comp.set_outputs(new_outs)

        return cls(comp)

    @classmethod
    def half_adder(cls, n: int) -> "bool_circ":
        """
        On part de Adder_n, puis on remplace la retenue d’entrée initiale
        (Cin du bit de poids faible) par une constante 0.
        """
        g = cls.adder(n)

        # On récupère l’ID du port Cin (toujours en position 0 de la liste inputs)
        id_cin0 = g.inputs[0]

        # On crée un noeud « 0 » et on le branche en lieu et place de l’input cin
        zero = g.add_node(label="0")
        g.add_edge(zero, id_cin0)

        # On retire Cin0 de la liste des entrées externes
        new_ins = [i for i in g.inputs if i != id_cin0]
        g.set_inputs(new_ins)

        return cls(g)

    
    
   
            
        
        
        

