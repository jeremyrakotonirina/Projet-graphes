# Projet Graphes – `open_digraph`

Implémentation en Python d’une structure de **graphes orientés ouverts** (`open_digraph`) et de **circuits booléens** (`bool_circ`), avec diverses opérations utiles pour les TPs de théorie des graphes / logique booléenne (génération aléatoire, vérifications de forme, chemins, circuits etc.). Adapté pour être réutilisé comme petite bibliothèque pédagogique de manipulation de graphes et circuits booléens en Python.

## Contenu du projet

- **`modules/node.py`** : définition de la classe `node`
  - Noeud identifié par un `id`, un `label`, et ses dictionnaires de **parents** / **enfants** (avec multiplicités).
- **`modules/open_digraph.py`** : définition de la classe principale `open_digraph`
  - Construction de graphes ouverts (entrées, sorties, noeuds internes).
  - Génération de graphes aléatoires (`free`, `DAG`, `oriented`, `undirected`, `loop-free`, etc.).
  - Vérification de bonne formation (`is_well_formed`), affichage, copie, etc.
  - Intègre plusieurs *mixins* :
    - `GettersSetters`, `Ajout`, `Suppression`, `Image`, `CircuitsBooleens`, `Chemins`.
- **`modules/bool_circ.py`** : classe `bool_circ(open_digraph)`
  - Modélisation de **circuits booléens** sur un `open_digraph`.
  - Labels supportés :
    - `&` : ET, `|` : OU, `^` : OU exclusif, `~` : NON, `''` : copie, `0` et `1` : constantes.
  - Vérification de bonne formation des circuits (`is_well_formed`, `is_cyclic`, etc.).
  - Méthodes de construction :
    - `parse_parentheses` : création d’un circuit booléen à partir d’expressions booléennes complètement parenthésées.
    - `random_bool_circ` : génération de circuits booléens aléatoires.
- **`modules/FonctionsMatrices.py`** : fonctions utilitaires sur les matrices
  - Génération de matrices d’adjacence aléatoires (triangulaires, symétriques, orientées, sans boucles…).
- **Mixins dans `modules/open_digraph_mixin/`** :
  - `Ajout.py`, `Suppression.py`, `Image.py`, `CircuitsBooleens.py`, `Chemins.py`, `GettersSetters.py` :
    - méthodes pour manipuler les graphes (ajout/suppression de noeuds/arêtes, calculs de chemins, opérations liées aux circuits booléens, export d’images, etc.).
- **`tests/open_digraph_test.py`** :
  - Batterie de tests unitaires sur les principales fonctionnalités.
- **`worksheet.py`** :
  - Petit script d’essais / TP (génération d’un graphe aléatoire, sauvegarde en `.dot`, relecture, affichage, etc.).

## Pré-requis

- Bibliothèques Python :
  - `matplotlib` (utilisé via `matplotlib.colors` dans `open_digraph.py`)
- Optionnel mais recommandé :

##Structure
Projet-graphes-main/
└── Projet-graphes-main/
    ├── modules/
    │   ├── node.py
    │   ├── open_digraph.py
    │   ├── bool_circ.py
    │   ├── FonctionsMatrices.py
    │   └── open_digraph_mixin/
    │       ├── Ajout.py
    │       ├── Suppression.py
    │       ├── Image.py
    │       ├── CircuitsBooleens.py
    │       └── Chemins.py
    ├── tests/
    │   └── open_digraph_test.py
    ├── worksheet.py
    └── README.md
