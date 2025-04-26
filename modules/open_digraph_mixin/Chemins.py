class MethodesChemins:
    def dijkstra(self, src, direction=None, tgt = None):
        """
        Algorithme de Dijkstra qui respecte le squelette du tp7 modifié pour s'arrêter dès qu'on atteint tgt (si différent de None).
        Retourne les dictionnaires dist(contenant les distance par raport a source) et prev(contient les parents).
        """
        
        if direction not in (None, 1, -1):
            raise ValueError("direction doit être None, 1 ou -1")
        
        if tgt is not None:
            if not isinstance(tgt, int):
                raise TypeError("tgt doit être un identifiant entier d'un noeud (int)")
            if tgt not in self.get_id_node_map():
                raise ValueError("tgt doit être un identifiant de noeud existant dans le graphe")
        
        Q = [src]
        dist = {src: 0}
        prev = {}

        while Q:
            # Trouver le noeud avec la distance minimale
            u = min(Q, key=lambda node_id: dist[node_id])
            Q.remove(u)

            if tgt is not None and u == tgt:
                break

            u_noeud= self.get_node_by_id(u)

            # Détermination des voisins selon la direction(parents, enfants ou les 2)
            if direction is None:
                voisins = list(u_noeud.get_children().keys()) + list(u_noeud.get_parents().keys())
            elif direction == 1:
                voisins = list(u_noeud.get_children().keys())
            elif direction == -1:
                voisins = list(u_noeud.get_parents().keys())

            for v in voisins:
                if v not in dist:
                    Q.append(v)
                if v not in dist or dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    prev[v] = u

        return dist, prev
    
    def shortest_path(self, u, v, direction=None):
        """
        Retourne la liste des identifiant formant le plus court chemin de u à v.
        Retourne [] si aucun chemin n'existe.
        """
        dist, prev = self.dijkstra(u, direction=direction, tgt=v)

        if v not in dist:
            return []  # Aucun chemin possible

        chemin = []
        curr = v
        while curr in prev:
            chemin.append(curr)
            curr = prev[curr]
        chemin.append(u)
        chemin.reverse()
        return chemin
    
    def ancetres_communs_distances(self, u, v):
        """
        Retourne un dictionnaire des ancêtres communs aux noeuds id1 et id2,
        avec pour chacun un tuple (distance depuis id1, distance depuis id2).
        """
        dist1, prev1 = self.dijkstra(u, direction=-1)
        dist2, prev2 = self.dijkstra(v, direction=-1)
        ancetres = []
        for cle in dist1:
            if cle in dist2:
                ancetres.append(cle)
        return {k: (dist1[k], dist2[k]) for k in ancetres}
    

    def tri_topologique_par_niveaux(self) :
        """Réalise un tri topologique par niveaux du graphe.
            Renvoie une liste de listes, chaque sous-liste contenant les identifiants des noeuds du niveau correspondant à l'indice dans la liste.
        Si le graphe contient un cycle, une erreur est levée.
        """
        # 1. Calcul des degrés entrants pour chaque nœud
        degres_entrants = {}
        for node in self.get_nodes():
            degres_entrants[node.id] = len(node.get_parents())

        niveaux = []  # Liste des niveaux
        niveau_courant = [node_id for node_id, deg in degres_entrants.items() if deg == 0]

        while niveau_courant:
            niveaux.append(niveau_courant)
            prochain_niveau = []

            for u in niveau_courant:
                enfants = self.get_node_by_id(u).get_children()
                for v in enfants:
                    degres_entrants[v] -= 1
                    if degres_entrants[v] == 0:
                        prochain_niveau.append(v)

            niveau_courant = prochain_niveau

        # Vérification de la présence d'un cycle
        for v in degres_entrants:
            if degres_entrants[v] > 0:
                raise ValueError("Le graphe contient un cycle")

        return niveaux
    
    def profondeur_noeud(self, id_noeud):
        """
        Retourne la profondeur du noeud d'identifiant `id_noeud`
        dans le graphe, calculée via le tri topologique par niveaux.
        """
        niveaux = self.tri_topologique_par_niveaux()
        indice = 0  # compteur de niveau
        for niveau in niveaux:
            if id_noeud in niveau:
                return indice
            indice += 1
        raise ValueError(f"Le noeud {id_noeud} n'est pas présent dans le graphe ou est inaccessible.")
    
    def profondeur_graphe(self):
        """
        Retourne la profondeur du graphe entier,
        c'est-à-dire le nombre total de niveaux dans le tri topologique.
        """
        return len(self.tri_topologique_par_niveaux())
    
    
    
    def plus_long_chemin(self, u, v):
        """
        Calcule le plus long chemin du nœud `u` vers `v` dans un graphe acyclique.
        Retourne une paire : (longueur du chemin, liste des IDs sur le chemin)
        """
        niveaux = self.tri_topologique_par_niveaux()

        # Trouver le niveau contenant u
        niveau_depart = -1
        for i in range(len(niveaux)):
            if u in niveaux[i]:
                niveau_depart = i
                break
        if niveau_depart == -1:
            raise ValueError("Le noeud de départ n'existe pas dans le graphe")

        # Initialisation
        dist = {u: 0}
        prev = {}

        # Parcours des niveaux à partir de celui juste après u
        for i in range(niveau_depart + 1, len(niveaux)):
            for w in niveaux[i]:
                max_parent = None
                max_dist = -1

                for parent_id in self.get_node_by_id(w).get_parents():
                    if parent_id in dist:
                        if dist[parent_id] > max_dist:
                            max_dist = dist[parent_id]
                            max_parent = parent_id

                if max_parent is not None:
                    dist[w] = max_dist + 1
                    prev[w] = max_parent

        # Construction du chemin si v est atteignable
        if v not in dist:
            return (None, [])  # Aucun chemin de u à v

        chemin = [v]
        courant = v
        while courant in prev:
            courant = prev[courant]
            chemin.append(courant)
        chemin.reverse()

        return (dist[v], chemin)