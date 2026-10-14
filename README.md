# Rush 3 - Satisfaction des passagers

## Équipe

| Membre | Responsabilité |
|---|---|
| Lilie Domingues | Organisation du dépôt, nettoyage des données, exploration (notebook 01), protection des données |
| Sofia Soltane | Plan de travail, nettoyage du fichier test, facteurs de satisfaction (notebook 02) |
| Adelaida Retuerto | Modèle prédictif (notebook 03), évaluation finale (notebook 04) |

## Lancer le code

1. `pip install -r requirements.txt`
2. Exécuter dans l'ordre : `notebooks/01_exploration.ipynb`, `02_facteurs.ipynb`, `03_modeles.ipynb`, `04_evaluation_finale.ipynb`.

`data_raw/test.csv` n'est jamais exploré. Il est seulement nettoyé par `src/nettoyer_test.py`, avec les règles fixées sur `train.csv` et sans regarder son contenu, puis utilisé une seule fois dans `04_evaluation_finale.ipynb` pour mesurer la performance du modèle choisi.

