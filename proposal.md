# Proposition d'architecture MVC pour le projet "Fly-in" (version 1.4)

Résumé
------
Proposition d'une structure MVC simple, claire et orientée objets pour implémenter
le simulateur de drones décrit dans le sujet. Respecte Python 3.10+, flake8, mypy,
et l'interdiction d'utiliser des bibliothèques de graphes externes.

Arborescence proposée
---------------------

- proposal.md
- src/
  - main.py                # point d'entrée (contrôleur MVC global)
  - config.py              # constantes, options CLI
  - model/
    - __init__.py
    - zone.py              # classes Zone, StartZone, EndZone, Connection
    - graph.py             # classe Graph (gestion des noeuds/aretes, validation)
    - drone.py             # classe Drone (id, state, path, position)
    - parser.py            # Parser strict du format d'entrée (lève erreurs avec ligne)
  - view/
    - __init__.py
    - terminal_view.py     # affichage coloré (couleurs ANSI) et format de sortie
    - logger.py            # journalisation, mode debug
  - controller/
    - __init__.py
    - simulator.py         # moteur de simulation (boucle de tours, réservation)
    - scheduler.py         # algorithme d'assignation/ordonnancement multi-drones
    - pathfinder.py        # recherche de chemins (A*/Dijkstra modifiés)
  - util/
    - types.py             # type aliases et petites fonctions utilitaires
    - exceptions.py        # exceptions personnalisées de parsing/simulation
- tests/                   # pytest tests unitaires (parser, graph, scheduler)
- Makefile
- README.md
- .gitignore

Rôles et responsabilités (par dossier)
-------------------------------------

- src/model:
  - `Zone` : encapsule métadonnées (type, color, max_drones, coords). Méthodes
    pour coût de mouvement et validation (blocked -> inaccessible).
  - `Connection` (dans graph.py ou séparé) : capacités de lien, identifiant,
    état transitoire (combien d'entrants en vol).
  - `Graph` : API de lecture/validation, indexation par nom, itérateurs, méthodes
    pour voisins, capacités et clones immuables pour simulation.
  - `Drone` : suit l'ID, état (idle,moving,in_transit,delivered), chemin courante,
    historique de mouvements.
  - `Parser` : lecture ligne à ligne, validation stricte, erreurs détaillées
    (ligne + message). Renvoie un objet `Graph` et `nb_drones`.

- src/controller:
  - `Pathfinder` : implémentation A* ou Dijkstra adaptée au coût par destination
    (priority, restricted), retourne chemins pondérés et plusieurs chemins
    disjoints/partiellement disjoints. Caching des chemins par paire (memoize).
  - `Scheduler` : répartit les drones sur plusieurs chemins disponibles, calcule
    priorités (zones priority, capacities) et planifie mouvements par tour.
    Utilise réservation optimiste par turn-slot (two-phase commit : collect, validate,
    commit) pour éviter conflits.
  - `Simulator` : boucle principale. À chaque tour :
    1) demander au Scheduler les actions proposées pour chaque drone,
    2) valider contraintes (zone capacity, link capacity, mouvements multi-turn),
    3) appliquer et générer la ligne de sortie formatée (ex: D1-roof1 ...),
    4) marquer livrés et finir quand tous arrivés.

- src/view:
  - `TerminalView` : fonctions pour afficher état (ANSI colors), résumer métriques,
    et produire la sortie exacte demandée (une ligne par tour). Optionnellement
    produire une version verbose pour debug.

Algorithme de pathfinding & scheduling (bref)
-------------------------------------------

- Pathfinding: A* avec heuristique euclidienne basée sur coordonnées, coût de
  l'arête = coût de la zone destination (1 normal/priority, 2 restricted). Bloqués
  ignorés. Retourne chemins k-shortest simples (adaptation légère de Yen ou
  itération sur A* en marquant arêtes temporairement) pour proposer alternatives.
- Caching: conserver résultats A* par paire (start,goal) et invalidation si
  capacités statiques modifiées (rare). Cela évite recomputations coûteuses.
- Scheduler: heuristique greedy + round-robin sur chemins disjoints, priorise
  zones `priority`. Réservation par turn-slot pour empêcher collisions et gérer
  multi-turn (restricted) en occupant le lien pendant 2 tours.

Contraintes parser / robustesse
--------------------------------

- Le `Parser` lève `ParseError(line, message)` à la première erreur détectée.
- Vérifie unicité des noms, présence d'un start et d'un end, types valides,
  capacités positives, et non-duplication des connexions (a-b / b-a).

Tests et qualité
---------------

- `tests/` : cas unitaires pour parser (bon/mauvais fichiers), graph (capacités),
  pathfinder (coûts), scheduler (scénarios simples). Utiliser `pytest`.
- CI local : target `make lint` exécute `flake8 .` et `mypy . --warn-return-any ...`

Makefile (obligatoires)
----------------------

- `install`: crée venv et installe dépendances dev (`pytest`, `colorama`, ...)
- `run`: `python -m src.main path/to/map.txt`
- `debug`: `python -m pdb -m src.main path/to/map.txt` (ou `python -m pdb src/main.py`)
- `clean`: supprime `__pycache__`, `.mypy_cache`, `build` éventuel
- `lint`: exécute flake8 et mypy avec flags demandés

Visualisation
-------------

- Terminal coloré via `colorama` (facultatif mais recommandé) : chaque zone
  colorée si metadata `color=` présente. `TerminalView` s'occupe d'affichage et
  produit la sortie ligne-par-tour pour l'évaluation automatique.

Extensions et options bonus
--------------------------

- GUI minimal avec `tkinter` ou export JSON pour visualiser en outil externe.
- Optimisations : implémenter une variante de flow/time-expanded network pour
  cas de très grands nombres de drones (optionnel).

Notes finales
-------------

Cette architecture est volontairement modulaire et orientée objets pour faciliter
tests et relectures durant la peer-review. Si tu veux, j'implémente le squelette
des classes (fichiers vides + docstrings) et le `Makefile` ensuite.
