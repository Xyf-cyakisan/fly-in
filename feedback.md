# Feedback — Single Responsibility pour `source/controller/MapConfig.py`

Résumé
------
Le fichier `source/controller/MapConfig.py` fonctionne comme un parseur complet
et un validateur de fichiers de carte. Il centralise la lecture de fichier, la
conversion des données, la validation de syntaxe et de sémantique, ainsi que
un petit bloc `__main__` pour tests manuels.

Observations (SRP)
------------------
- Violation partielle du SRP : la classe `MapConfig` regroupe plusieurs
  responsabilités : I/O, parsing, conversion de types, règles de validation et
  logique métier (ex. détection de duplications). Idéalement, chaque responsabilité
  aurait sa classe/module dédié.
- Points concentrés dans `MapConfig` :
  - Lecture de fichier et filtration des commentaires (`_read_file`).
  - Analyse lexicale / transformation en structure (`_convert_content_to_dict`).
  - Validation fine (noms, metadata, duplications, coordonées) via de multiples
    méthodes `_check_*` dispersées.
  - Conversion/coercion de types (`_convert_hubs_value_type`, `_convert_connections_value_type`).
  - Logique de sortie/affichage dans le bloc `if __name__ == "__main__"`.

Recommandations de découpage
----------------------------
Proposer une séparation claire en trois (ou quatre) composants :

1. `parser.Parser` (module `src/model/parser.py`)
   - Responsabilité : lecture du fichier, tokenisation minimale, construction
     d'une représentation brute (liste/tuples) et renvoi des lignes.
   - Déplacer : `_read_file`, la boucle qui itère sur les lignes, et la collecte
     initiale `content, lines`.

2. `converter.Converter` (ou utilitaire)
   - Responsabilité : convertir les valeurs string → types (int, tuples), normaliser
     structures.
   - Déplacer : `_convert_content_to_dict`, `_convert_hubs_value_type`,
     `_convert_connections_value_type`.

3. `validator.Validator` (module `src/model/validator.py`)
   - Responsabilité : toutes les vérifications qui lèvent des erreurs de format
     ou de cohérence.
   - Déplacer : `_check_mandatory_data`, `_check_metadata`, `_check_hub_names`,
     `_check_connections_duplicate`, `_all_data_types_covered`,
     `_check_metadata_type`, `_check_coordinates_duplicate`.
   - Retourner des exceptions spécifiques (`ParseError`, `ValidationError`) au
     lieu de ValueError générique.

4. `model.MapConfig` (data class)
   - Responsabilité : contenir les données finales validées (`nb_drones`,
     `start_hub`, `end_hub`, `hub`, `connection`, `metadata`).
   - Constructeur simple ; reçu des composants ci‑dessus une fois prêts.

Conseils d'implémentation
-------------------------
- Introduire des exceptions dédiées (`src/util/exceptions.py`) pour des messages
  clairs et testables (ex. `ParseError(line, msg)`).
- Rendre chaque validateur pur et testable (entrée → lève ou renvoie True).
- Ajouter des tests unitaires ciblant chaque petite responsabilité (parser,
  converter, validator, dataclass). Cela facilite la séparation.
- Garder la logique de `parse()` comme orchestration : appeler Parser →
  Converter → Validator → construire `MapConfig` immuable.

Points mineurs / bugs observés
-----------------------------
- Dans `_check_coordinates_duplicate` il y a une référence `dict_content.lines` au
  lieu de `dict_content['lines']` — cela lèvera probablement une `AttributeError`.
  (ligne utilisée pour formuler l'exception). À corriger.
- Certaines méthodes utilisent beaucoup d'indexations par clé de dictionnaire
  imbriquées (ex. `dict_content['metadata'][...][...]`) : factoriser l'accès et
  vérifier l'existence avant d'indexer évitera KeyError.
- L'utilisation de `list`/`tuple` mutables modifiées en place rend le flux moins
  lisible ; préférer la création de nouvelles structures immutables pour chaque
  étape de conversion.

Conclusion
----------
Actuellement `MapConfig` ne respecte pas strictement le SRP : elle fait trop de
choses. Le découpage proposé (Parser / Converter / Validator / Data model)
répondrait au SRP, améliorerait la testabilité et rendrait le code plus maintenable
pour la peer-review. Si tu veux, je peux fournir un patch qui effectue ce découpage
en conservant l'API `MapConfig.parse()` (orchestration) pour compatibilité.

Notes par catégorie
-------------------

- Parser
  - But: isoler toute lecture/filtrage de lignes, gestion des commentaires et
    numérotation de lignes pour messages d'erreur.
  - Ce que tu peux conserver: logique actuelle de `_read_file` mais extraire
    dans `parser.Parser.read()` qui renvoie `(content, lines)`.
  - Tests rapides: fichier avec commentaires, lignes vides, lignes malformées.

- Converter
  - But: transformer la représentation textuelle en structures typées (int,
    tuples, listes immuables). Ne doit pas lever d'erreurs de cohérence métier
    (seulement de type/coercion).
  - Ce que tu peux extraire: `_convert_content_to_dict`, `_convert_hubs_value_type`,
    `_convert_connections_value_type`.
  - Bénéfice: facilite le caching et la réutilisation en mémoire.

- Validator
  - But: regrouper toutes les règles métier et les invariants (unicité de nom,
    interdiction de tirets, duplications de liens, types de metadata valides,
    coordonnées uniques, capacités positives, start/end uniques, etc.).
  - Ce que tu peux extraire: toutes les méthodes `_check_*` qui lèvent actuellement
    `ValueError` ; remplacer par des exceptions spécifiques pour tests.
  - Bénéfice: tests unitaires simples par règle, meilleure lisibilité des erreurs
    (ligne + cause clairement formatée).

- MapConfig / Model (data)
  - But: contenir le résultat final validé. Devrait être passif (data-only),
    idéalement immuable (tuples, frozenset, Mapping immuable).
  - Ce que tu peux conserver: la signature `MapConfig(nb_drones, start_hub, ...)`
    mais construire l'objet après validation via l'orchestrateur.
  - Bénéfice: réduit la surface de la classe à une responsabilité unique.

Prochaine étape suggérée
-----------------------
- Si tu veux que j'applique le refactoring, je peux d'abord ajouter des wrappers
  (squelettes de modules `parser.py`, `converter.py`, `validator.py`) et faire
  une migration progressive où `MapConfig.parse()` appelle ces composants. Cela
  minimise le risque et conserve l'API existante.

Évaluation finale (SRP)
----------------------

- Respect du Single Responsibility Principle : NON (score: 5/10)
  - Justification courte : `MapConfig` effectue au moins quatre responsabilités
    distinctes (I/O, parsing/tokenisation, conversion/coercion de types,
    validation métier). Les responsabilités sont mélangées dans une même classe
    et plusieurs méthodes ont des responsabilités secondaires implicites.
  - Conséquences : testabilité réduite, complexité pour les revues, risque
    d'effets de bord lors de modifications futures.

- Ce qu'il faudrait pour monter la note à ≥9/10 :
  1. Extraire le lecteur de fichier (`Parser`) et le rendre responsable uniquement
     de la lecture/filtrage/numérotation.
  2. Extraire la conversion/coercion (`Converter`) pour produire des structures
     typées à partir des strings.
  3. Extraire toutes les vérifications métier dans un `Validator` pur.
  4. Réduire `MapConfig` à une data-class immuable construite après validation.
  5. Remplacer `ValueError` générique par des exceptions spécifiques et ajouter
     des tests unitaires ciblés.

- Remarque rapide: il y a au moins une erreur potentielle (référence
  `dict_content.lines` vs `dict_content['lines']`) qui mérite correction avant
  extraction.

Si tu veux, j'applique un refactor minimal qui conserve l'API `MapConfig.parse()`
en orchestrant `Parser` → `Converter` → `Validator` → `MapConfig` (progressif).
