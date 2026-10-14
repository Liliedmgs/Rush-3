# À faire demain

Dans l'ordre. Une seule personne au clavier par fichier, et `git pull --rebase` avant de commencer.

| # | Tâche | Qui | Fait |

| 1 | Textes du notebook 02 | Sofia 
| 2 | Fichiers inutiles sur `test.csv` : supprimer ou garder | Tous
| 3 | Phrase manquante dans la partie 3 du rapport | Sofia 
| 6 | Supprimer ce fichier | Lilie 
| 7 | Fusionner `dev` dans `main` | Tous

---

## 1. Textes du notebook 02

`notebooks/02_facteurs.ipynb` n'a que du code. Ajouter une cellule de texte au-dessus de chaque bloc : clic dans la marge à gauche de la cellule, touche `A`, touche `M`, `Entrée`, coller, `Maj + Entrée`.

| Au-dessus de la cellule qui commence par | Texte à coller |
|---|---|
| `import sys` | `# 02 — Ce qui explique la satisfaction` puis : Objectif : trouver les services les plus liés à la satisfaction, et vérifier si ce lien tient quel que soit le profil. Les 14 notes sont utilisées ici : on explique le passé, on ne prédit pas. Tout est fait sur `train.csv`. |
| `tableau = pd.DataFrame` | `## Satisfaction selon la note de chaque service` puis : Pour chaque service, part de satisfaits selon la note (1 à 5). L'écart entre la note 5 et la note 1 mesure la force du lien. |
| `tableau["ecart"].sort_values()` | `## Les services classés par force du lien` |
| `def ecart(groupe)` | `## Le même calcul à profil égal` puis : Un lien global peut venir du profil plutôt que du service. On refait le calcul dans trois groupes : affaires en Business, affaires en Eco, personnel en Eco. |
| `PROFIL = [` | `## Vérification par forêt aléatoire` puis : L'importance par permutation mesure combien la forêt perd quand on mélange une variable. Les notes sans réponse sont remises à 0 : pour la forêt, c'est une valeur à part, distincte des notes 1 à 5. |

Puis supprimer la dernière cellule, vide (clic dans la marge, deux fois `D`), `Ctrl+S`, commit et push.

## 2. Fichiers inutiles sur `test.csv`

`src/nettoyer_test.py` et `data_clean/test_clean.csv` ne sont utilisés par aucun notebook, et ils contredisent la règle « `test.csv` ne sert qu'une fois ». Décider ensemble :

- **Supprimer** (conseillé) : `git rm src/nettoyer_test.py data_clean/test_clean.csv`, puis retirer du README la phrase sur `src/nettoyer_test.py`.
- **Garder** : corriger dans `src/rush3/prediction/evaluation_finale.py` la phrase « le SEUL code du dépôt qui lit test.csv ».

## 3. Phrase manquante dans la partie 3

Le service à bord (44,9), la propreté (41,3) et la place pour les jambes (41,2) sont plus liés à la satisfaction que la réservation en ligne (36,2), mais ne sont pas cités. Ajouter dans `rapport/partie_B.md` et dans le Google Doc :

> Le service à bord, la propreté et la place pour les jambes montrent aussi un lien fort, mais, comme le siège et le divertissement, ils ne comptent pas chez les voyageurs personnels en Eco (−0,7, 0,0 et 5,8) : ils ne sont donc pas prioritaires.



## 4. Supprimer ce fichier et plan md

Juste avant la fusion : `git rm A_FAIRE_DEMAIN.md`, commit, push.

## 7. Fusionner `dev` dans `main`

En dernier, quand tout est poussé. Sur GitHub : *Pull requests → New pull request*, base `main`, compare `dev`, *Create pull request*, puis *Merge*. Le jury regarde `main` : sans cette étape, il voit un dépôt vide.
