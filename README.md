# Rush 3 - Satisfaction des passagers

## Équipe

| Membre | Responsabilité |
|---|---|
| Lilie Domingues | Organisation du dépôt, nettoyage des données, exploration (notebook 01), protection des données |
| Sofia Soltane | Plan de travail, nettoyage du fichier test, facteurs de satisfaction (notebook 02) |
| Adelaida Retuerto | Socle commun `src/rush3/core`, modèle prédictif (`src/rush3/prediction`, notebook 03), évaluation finale (notebook 04), tests |

## Lancer le code

1. `pip install -r requirements.txt` (installe aussi le paquet `rush3` ; à relancer après chaque `git pull` qui modifie `src/rush3/`, sinon « No module named rush3 »)
2. `pytest` : vérifie le nettoyage, les mesures et les règles du projet.
3. Exécuter dans l'ordre : `notebooks/01_exploration.ipynb`, `02_facteurs.ipynb`, `03_modeles.ipynb`, `04_evaluation_finale.ipynb`.

`data_raw/test.csv` n'est jamais exploré. Il est seulement nettoyé par `src/nettoyer_test.py`, avec les règles fixées sur `train.csv` et sans regarder son contenu, puis utilisé une seule fois dans `04_evaluation_finale.ipynb` pour mesurer la performance du modèle choisi.

## Prédiction des mécontents (notebooks 03 et 04)

Question : quels passagers approcher à l'atterrissage, sachant qu'on ne peut en approcher que 10 % ?

**Variables utilisées** (`LANDING_COLS`, `src/rush3/core/schema.py`) : seulement ce que la compagnie connaît à l'atterrissage, soit type de client, âge, motif du voyage, classe, distance, retards au départ et à l'arrivée. Aucune des 14 notes du questionnaire (rempli après le vol), pas de genre. La version déployée de l'arbre retenu n'utilise pas l'âge (`DEPLOIEMENT_COLS`, `src/rush3/prediction/modeles.py`) ; l'âge ne sert qu'à n'approcher aucun mineur.

**Mesure** : part de vrais insatisfaits parmi les 10 % de passagers les mieux classés, convertie en euros (une approche coûte 40 €, un vrai insatisfait approché rapporte 100 €).

**Résultats** (validation croisée à 5 blocs sur `train.csv`, `results/03_comparaison_modeles.json`) :

| Stratégie | Précision top 10 % | Bénéfice pour 1 000 passagers | Gain sur la règle simple |
|---|---|---|---|
| Hasard | 0,567 | 1 667 € | −3 298 € |
| Règle simple (voyage personnel) | 0,897 | 4 965 € | 0 € |
| Régression logistique | 0,937 | 5 367 € | +402 € |
| Arbre de décision (4 niveaux) | 0,955 | 5 551 € | +586 € |
| Gradient boosting | 0,965 | 5 653 € | +688 € |

- Le genre n'apporte rien. L'âge n'apporte rien à l'arbre retenu (95,6 % sans, 95,5 % avec) ; il n'est utile qu'au gradient boosting (`results/03_variables_sensibles.json`).
- Version déployée (arbre sans l'âge, aucun mineur signalé) : 94,9 %, soit 5 494 € pour 1 000 passagers (`results/03_comparaison_modeles.json`, clé `deploiement`).
- Sur 1 000 passagers, environ 470 insatisfaits ne sont pas approchés : c'est la limite de capacité (10 %), pas une erreur du modèle.
- Modèle retenu : `MODELE_CHOISI` dans `src/rush3/prediction/modeles.py`, déployé sans l'âge (`construire_deploiement`).

**Organisation du code**

| Fichier | Rôle |
|---|---|
| `src/rush3/core/` | commun : chemins (`config.py`), colonnes (`schema.py`), nettoyage (`donnees.py`), calcul économique (`economie.py`), contrats JSON (`contrats.py`) |
| `src/common.py` | réexporte `rush3.core` pour les notebooks 01 et 02 |
| `src/rush3/prediction/modeles.py` | règle simple et les trois modèles, préparation des données dans un `Pipeline` |
| `src/rush3/prediction/validation.py` | validation croisée à 5 blocs, essais avec et sans âge / genre, version déployée |
| `src/rush3/prediction/metriques.py` | précision sur le top 10 % |
| `src/rush3/prediction/evaluation_finale.py` | seul code qui lit `test.csv` |
| `tests/` | nettoyage, contrats, mesures, et règles : seul le notebook 04 lit `test.csv`, la prédiction n'utilise aucune note |

`04_evaluation_finale.ipynb` n'est exécuté qu'une seule fois, quand le modèle est définitivement choisi. Ses chiffres sont rapportés tels quels, même s'ils sont moins bons que la validation croisée. Il a été exécuté le 14/10/2026 avec l'arbre à 7 informations, âge compris ; la version sans l'âge a été décidée ensuite, sur `train.csv` seulement, et le notebook n'a pas été relancé.
