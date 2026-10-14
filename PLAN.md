# Plan de travail — Rush 3 « Customer Satisfaction »

Ce document dit qui fait quoi, dans quel ordre, et pourquoi. Il est écrit pour être suivi pas à pas, même sans expérience en code. Cochez les cases `[ ]` → `[x]` au fur et à mesure.

> Remplacez **A**, **B**, **C** par vos prénoms dès le début (ici et dans le README).

---

## Où on en est (13 octobre)

### Fait

- [x] Dépôt organisé : `data_raw/`, `data_clean/`, `src/`, `notebooks/`.
- [x] Règles de nettoyage écrites dans `src/common.py` (fonction `nettoyer`).
- [x] `train.csv` nettoyé → `data_clean/train_clean.csv` (notebook 01).
- [x] `test.csv` nettoyé → `data_clean/test_clean.csv` (script `src/nettoyer_test.py`), avec les mêmes règles et sans rien regarder du contenu.

> **Attention :** `src/nettoyer_test.py` lit `test.csv` uniquement pour le nettoyer. Personne n'ouvre `test_clean.csv` dans les notebooks 01, 02 ou 03. Pour la vérification de l'étape 5, chercher aussi `test_clean` dans le dépôt.

### Reste à faire, d'après la consigne

Le nettoyage n'est que la préparation : aucun livrable n'est encore commencé.

- [ ] **On fait tout à trois**, étape par étape, en suivant le guide de la section 9. A, B et C désignent seulement qui tient le clavier et qui signe la partie : l'écrire ici et dans le README.
- [ ] **Explorer les données**, sur `train` seulement : graphiques et tableaux (mécontents par classe, motif, âge ; où sont les `0` ; retards extrêmes). → Étape 1
- [ ] **Expliquer la satisfaction**, avec les 14 notes. Pour chaque facteur recommandé : est-il lié ? la compagnie peut-elle agir ? est-ce une cause ? → Étape 2
- [x] **Prédire les mécontents**, sans les 14 notes : liste justifiée de ce qu'on sait à l'atterrissage, règle simple sans modèle, au moins deux modèles comparés sans `test`, choix du modèle avec le coût de ses erreurs. → Étape 3
- [ ] **Protection des données** : conditions pour que ce soit acceptable (enfants compris), chaque information du modèle est-elle acceptable, ce que voit l'employé sur un passager signalé. → Étape 4
- [x] **Contrôle final sur `test`**, une seule fois, tout à la fin. → Étape 5
- [ ] **Rapport PDF**, 8 pages max, avec un résumé d'une page pour la directrice en ouverture. → Étape 6
- [ ] **Code reproductible** : mêmes chiffres à chaque lancement. → Étape 7
- [ ] **Oral** de 10 minutes puis questions. → Étape 8
- [ ] **README** : qui a fait quoi (il ne contient que le titre pour l'instant).
- [ ] **Historique git** : des commits de chacune des trois, depuis son propre compte.

---

## 1. Ce qu'on doit rendre

| Livrable | Contraintes |
|---|---|
| Rapport PDF | 8 pages max hors annexes. La page 1 est un résumé pour la directrice. |
| Code | Reproduit **tous** les chiffres et figures du rapport. Lancé deux fois, il donne les mêmes résultats. |
| Oral | 10 minutes + questions sur nos choix. |
| Dépôt git | L'historique montre la répartition du travail ; le README dit qui a fait quoi. |

La directrice n'est pas data scientist : chaque résultat doit pouvoir s'expliquer en une phrase simple.

---

## 2. Les 5 règles à ne jamais enfreindre

Ce sont les pièges du sujet. Un seul d'entre eux suffit à invalider le travail.

1. **`test.csv` n'est ouvert qu'une seule fois, à la toute fin.** Il représente les passagers du mois prochain. On ne le regarde pas, on ne fait aucun graphique dessus, on ne s'en sert pas pour choisir un modèle. Un seul fichier de code a le droit de le lire : `04_evaluation_finale.ipynb`.
2. **Le modèle de prédiction n'utilise que ce qu'on sait à l'atterrissage.** Les 14 notes de service (wifi, siège, repas…) viennent du questionnaire, rempli *après* le vol : interdites dans le modèle. Elles servent uniquement à la partie « facteurs explicatifs ».
3. **Un `0` dans une note ne veut pas dire « très mauvais ».** Il veut dire « pas de réponse » ou « service non concerné ». On le traite comme une valeur manquante.
4. **Tout est reproductible.** Partout où il y a du hasard, on écrit `random_state=42`. Aucun chiffre n'est tapé à la main dans le rapport : il sort du code.
5. **Corrélation ≠ cause ≠ levier d'action.** Pour chaque facteur recommandé, on dit les trois : est-il lié à la satisfaction ? la compagnie peut-elle agir dessus ? est-ce vraiment lui qui cause la satisfaction ?

---

## 3. Ce qu'on sait déjà des données

Mesuré sur `train.csv` (103 904 passagers, 25 colonnes) :

- 56,7 % des passagers sont « neutral or dissatisfied ». C'est notre cible à prédire.
- 310 valeurs manquantes, toutes dans `Arrival Delay in Minutes`. Aucun doublon.
- `Unnamed: 0` et `id` sont des numéros de ligne : à supprimer.
- Retard au départ et retard à l'arrivée disent presque la même chose (corrélation 0,965).
- 7 931 passagers ont moins de 18 ans (minimum 7 ans), dont 83,6 % d'insatisfaits.
- Taux d'insatisfaction : voyage personnel 89,8 % contre affaires 41,7 % ; Eco 81,4 %, Eco Plus 75,4 %, Business 30,6 % ; non fidèle 76,3 % contre fidèle 52,3 %.

### Le calcul économique (à comprendre par les trois)

Chiffres de la directrice : une approche coûte 40 € ; 1 insatisfait sur 3 ne revient pas (600 € perdus) ; l'approche en récupère la moitié.

- Gain espéré quand on approche un **vrai** insatisfait : 600 × 1/3 × 1/2 = **100 €**.
- Gain quand on approche un passager satisfait : 0 €. On a quand même payé 40 €.
- Donc **bénéfice par approche = 100 × précision − 40**, où la précision est la part de vrais insatisfaits parmi les passagers approchés.
- Seuil de rentabilité : précision de 40 %.
- Contrainte : on ne peut approcher que 10 % des passagers, soit 100 sur 1 000.

Ce que ça donne pour 1 000 passagers à l'arrivée :

| Stratégie | Précision | Bénéfice |
|---|---|---|
| Approcher 100 passagers au hasard | 56,7 % | 100 × (56,7 − 40) = 1 670 € |
| Règle simple : 100 voyageurs « personnels » | 89,8 % | 4 980 € |
| Maximum théorique (aucune erreur) | 100 % | 6 000 € |

**Conséquence importante :** la règle simple est déjà très bonne. Notre modèle ne peut gagner qu'entre 4 980 € et 6 000 €. Il faudra dire honnêtement combien il apporte en plus, et si ça justifie sa complexité. C'est exactement ce que le sujet appelle « aller au-delà du meilleur score ».

**La bonne mesure n'est donc pas l'accuracy** (le pourcentage de bonnes réponses sur tout le monde), mais la **précision sur les 10 % de passagers les mieux classés** par le modèle, convertie en euros.

---

## 4. Organisation du dépôt

```
Rush 3/
├── README.md                      qui a fait quoi + comment lancer le code
├── PLAN.md                        ce fichier
├── requirements.txt               liste des bibliothèques Python et leurs versions
├── data_raw/                      données d'origine, jamais modifiées à la main
│   ├── train.csv
│   └── test.csv
├── data_clean/                    données nettoyées, produites par le code (jamais à la main)
├── src/
│   └── common.py                  fonctions partagées (chargement, nettoyage)
├── notebooks/
│   ├── 01_exploration.ipynb       → A
│   ├── 02_facteurs.ipynb          → B
│   ├── 03_modeles.ipynb           → C
│   └── 04_evaluation_finale.ipynb → C (seul fichier qui lit test.csv)
├── figures/                       images générées par les notebooks
├── results/                       tableaux et chiffres générés (csv / json)
└── rapport/
    └── rapport.pdf
```

**Pourquoi un notebook par personne ?** Un notebook est un fichier difficile à fusionner quand deux personnes le modifient en même temps. Si chacun reste dans le sien, il n'y a jamais de conflit git.

**Pourquoi `src/common.py` ?** Les trois notebooks doivent charger et nettoyer les données exactement de la même façon. Sinon B et C obtiendront des chiffres différents sans comprendre pourquoi. On écrit ces fonctions une fois, et tout le monde les importe.

---

## 5. Répartition

| | A — Données & conformité | B — Facteurs explicatifs | C — Modèle prédictif |
|---|---|---|---|
| Question traitée | À quoi ressemblent les données ? Peut-on légalement faire ça ? | Qu'est-ce qui explique la satisfaction ? | Qui approcher à l'atterrissage ? |
| Code | `src/common.py`, `01_exploration.ipynb` | `02_facteurs.ipynb` | `03_modeles.ipynb`, `04_evaluation_finale.ipynb` |
| Variables utilisées | toutes | toutes, y compris les notes | seulement celles connues à l'atterrissage |
| Rapport | Exploration, Protection des données | Facteurs, Recommandations | Modèles, coût des erreurs |
| Autre | README, `requirements.txt`, vérification finale de reproductibilité | Assemblage du rapport | Slides de l'oral |

Le résumé de la page 1 et la répétition de l'oral se font à trois.

---

## 6. Étapes

### Étape 0 — Mise en place (tous ensemble, 1 h)

Rien d'autre ne peut commencer avant, donc on le fait à trois sur un seul écran.

- [ ] Chacun vérifie son identité git, sinon ses commits seront attribués à quelqu'un d'autre :
  ```bash
  git config user.name
  git config user.email
  ```
  Pour corriger : `git config user.name "Prénom Nom"` et `git config user.email "adresse@..."`.
- [ ] Créer les dossiers `data_raw/`, `src/`, `notebooks/`, `figures/`, `results/`, `rapport/` et déplacer les deux CSV dans `data_raw/`.
- [ ] Créer `requirements.txt` (pandas, numpy, scikit-learn, matplotlib, seaborn, jupyter) puis installer : `pip install -r requirements.txt`. Une fois que tout marche, noter les versions exactes avec `pip freeze` : deux versions différentes d'une bibliothèque peuvent donner des chiffres différents.
- [ ] **A** écrit `src/common.py` pendant que B et C regardent. Il contient :
  - `load_train()` : lit `data_raw/train.csv`, supprime `Unnamed: 0` et `id`, crée une colonne `insatisfait` qui vaut 1 si `satisfaction` est « neutral or dissatisfied », sinon 0.
  - `load_test()` : même chose pour `test.csv`. **Appelée uniquement dans le notebook 04.**
  - `RATING_COLS` : la liste des 14 colonnes de notes.
  - `LANDING_COLS` : la liste des colonnes connues à l'atterrissage (voir étape 3).
  - `SEED = 42`.
- [ ] Remplir le README : noms, rôles, commande pour lancer le code.
- [ ] Premier commit de chacun (voir section 7), pour vérifier que les trois arrivent à pousser.

### Étape 1 — Exploration (A, jour 1)

But : décrire les données et repérer leurs problèmes. Tout se fait sur `train.csv`.

- [ ] Taille, types des colonnes, valeurs manquantes, doublons.
- [ ] Répartition de la cible (graphique en barres : satisfaits / insatisfaits).
- [ ] Compter les `0` dans chaque note. Sont-ils liés à un profil particulier (par exemple, ceux qui n'ont pas fait l'embarquement en ligne) ? C'est ce qui justifie de les traiter comme « sans réponse ».
- [ ] Distribution de l'âge, de la distance, des retards (histogrammes). Repérer les valeurs extrêmes : un retard de 1 592 minutes, on le garde ou pas, et pourquoi ?
- [ ] Taux d'insatisfaction par classe, type de voyage, fidélité, tranche d'âge.
- [ ] Le croisement classe × type de voyage : un voyageur d'affaires en Eco est-il aussi insatisfait qu'un voyageur personnel en Eco ?
- [ ] Écrire noir sur blanc les décisions de nettoyage et les reporter dans `common.py` : que fait-on des 310 retards manquants ? des `0` ?
- [ ] Enregistrer chaque figure dans `figures/` avec `plt.savefig(...)`.

**Limite à signaler dans le rapport :** le modèle est entraîné sur des gens qui ont répondu au questionnaire, mais il sera appliqué à tous les passagers. Ceux qui répondent ne ressemblent pas forcément aux autres. On ne peut pas le corriger avec ces données, mais il faut le dire.

### Étape 2 — Facteurs explicatifs (B, jour 1 → matin jour 2)

But : dire à la directrice où mettre son budget. Ici les 14 notes sont autorisées, puisqu'on explique le passé au lieu de prédire à l'atterrissage.

- [ ] Remplacer les `0` des notes par « manquant » avant tout calcul.
- [ ] **Niveau 1, descriptif.** Pour chaque note : taux de satisfaction selon la note donnée (1 à 5). Un graphique par service, ou un seul graphique classant les services par force du lien.
- [ ] **Niveau 2, à profil égal.** Les passagers Business notent mieux *et* sont plus satisfaits : la classe brouille tout. On refait donc l'analyse séparément par classe et type de voyage, ou avec une régression logistique qui contient les notes + classe + type de voyage + fidélité. Un facteur qui reste important une fois le profil pris en compte est plus crédible.
- [ ] **Niveau 3, vérification croisée.** Entraîner une forêt aléatoire et regarder l'importance par permutation. Si les deux méthodes désignent les mêmes facteurs, la conclusion est solide.
- [ ] Remplir le tableau central du rapport, une ligne par facteur :

  | Facteur | Lié à la satisfaction ? (chiffre) | La compagnie peut agir ? | Est-ce une cause ? |
  |---|---|---|---|
  | Embarquement en ligne | … | oui (appli, site) | à argumenter |
  | Type de voyage | très fort | non | non : c'est un profil, pas un service |
  | Emplacement de la porte | aucun | peu (dépend de l'aéroport) | — |
  | … | | | |

- [ ] Pour la colonne « cause », garder trois doutes en tête :
  - **Facteur caché** : la classe ou le motif du voyage explique à la fois la note et la satisfaction.
  - **Effet de halo** : un passager content met de bonnes notes partout. La note est alors une conséquence de la satisfaction, pas sa cause.
  - **Données d'observation** : seul un test réel (améliorer le wifi sur certains vols et comparer) prouverait une cause. On peut le proposer comme recommandation.
- [ ] En tirer 3 à 5 recommandations chiffrées, classées par priorité.

### Étape 3 — Modèle prédictif (C, jour 1 → matin jour 2)

But : classer les passagers à l'atterrissage pour approcher les 10 % les plus à risque.

- [x] **Établir la liste des variables connues à l'atterrissage** et la justifier (le sujet dit que c'est à nous de l'établir) :

  | Variable | Connue à l'atterrissage ? | Remarque |
  |---|---|---|
  | Classe, type de voyage, fidélité | oui | dossier de réservation |
  | Distance du vol | oui | |
  | Retard au départ, retard à l'arrivée | oui | très corrélés : en garder un seul ou les deux, à tester |
  | Âge | oui | question des mineurs → décider avec A |
  | Genre | oui | n'apporte presque rien (57,3 % contre 56,1 %) → l'exclure se défend bien |
  | Les 14 notes | **non** | questionnaire rempli après le vol |

- [x] **Découper `train.csv` pour comparer les modèles**, puisque `test.csv` est interdit. On utilise la validation croisée à 5 blocs : on coupe les données en 5 parts, on entraîne sur 4, on mesure sur la 5e, et on recommence 5 fois en changeant la part mise de côté. On obtient 5 mesures, donc une moyenne et une idée de sa stabilité.
  ```python
  from sklearn.model_selection import StratifiedKFold
  cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
  ```
- [x] **Écrire la mesure métier** (une seule fois, réutilisée partout) :
  ```python
  import numpy as np

  def precision_top10(y_vrai, scores):
      """Part de vrais insatisfaits parmi les 10 % de passagers les mieux classés."""
      n = int(len(scores) * 0.10)
      meilleurs = np.argsort(scores)[::-1][:n]
      return np.asarray(y_vrai)[meilleurs].mean()

  def benefice_pour_1000(precision):
      return 100 * (100 * precision - 40)
  ```
- [x] **Les points de comparaison sans modèle** : approche au hasard, puis la règle simple (voyageurs personnels). Les mesurer avec la même validation croisée.
- [x] **Modèle 1 : régression logistique.** Simple, et chaque variable reçoit un poids qu'on peut expliquer à la directrice.
- [x] **Modèle 2 : arbre de décision peu profond** (3 ou 4 niveaux). Il se lit comme une suite de questions : « voyage personnel ? → classe Eco ? → … ».
- [x] **Modèle 3 (si le temps le permet) : forêt aléatoire ou gradient boosting.** Souvent plus performant, mais c'est une boîte noire.
- [x] Mettre le prétraitement (remplissage des valeurs manquantes, encodage des catégories) **dans un `Pipeline` scikit-learn**. Sinon le nettoyage « voit » les données de validation et les scores sont trop optimistes.
- [x] Tableau comparatif : pour chaque stratégie, précision sur le top 10 %, bénéfice pour 1 000 passagers, et écart entre les 5 blocs.
- [x] **Coût des erreurs**, en mots simples :
  - Fausse alerte (on approche un passager satisfait) : 40 € dépensés pour rien.
  - Oubli (un insatisfait pas approché) : 100 € de gain espéré manqués. Avec une capacité de 10 % et 56,7 % d'insatisfaits, la grande majorité sera forcément oubliée : le dire clairement.
- [x] **Choisir le modèle à déployer** et l'argumenter sur trois critères : bénéfice, facilité d'explication, données personnelles nécessaires. Si un modèle complexe ne rapporte que quelques euros de plus que la règle simple, recommander le plus simple est une conclusion valable.
- [x] Tester le modèle avec et sans l'âge, avec et sans le genre : combien perd-on ? Ce chiffre sert directement à A pour la partie protection des données.

### Étape 4 — Protection des données (A, jour 2)

But : dire à quelles conditions le signalement des passagers serait acceptable. Le sujet impose trois réponses.

- [ ] **Les conditions.** Les données ont été collectées pour mesurer la satisfaction ; signaler des passagers au personnel est un usage nouveau (RGPD, principe de limitation des finalités, art. 5 et 6.4). Points à traiter : sur quelle base légale (consentement ou intérêt légitime), information des passagers, droit de s'y opposer (art. 21), analyse d'impact avant le lancement (art. 35), durée de conservation, et le fait que la plupart des passagers signalés n'ont jamais répondu à un questionnaire.
- [ ] **Les enfants.** Les mineurs ont une protection renforcée (considérant 38). Proposer une règle nette, par exemple : aucun mineur n'est signalé individuellement ; s'il voyage accompagné, on s'adresse à l'adulte. Vérifier avec C ce que ça change au résultat.
- [ ] **Chaque variable du modèle**, dans un tableau : est-elle nécessaire ? acceptable ? Le principe est de n'utiliser que le strict nécessaire (minimisation). Une variable qui n'améliore pas le modèle n'a aucune raison d'y être : c'est l'argument pour le genre.
- [ ] **Ce que voit l'équipe au sol.** Proposer un écran concret : numéro de siège ou nom, et une mention neutre du type « attention prioritaire ». Pas de score, pas de motif, pas d'âge. Le personnel ne doit pas savoir *pourquoi* le passager est signalé.

Les numéros d'articles sont des points de départ : relisez le texte avant de les citer dans le rapport.

### Étape 5 — Évaluation finale sur `test.csv` (C, jour 2 après-midi)

À faire **une seule fois**, quand le modèle est définitivement choisi et que plus rien ne changera.

- [x] Créer `04_evaluation_finale.ipynb`. En haut, une cellule de texte : « Ce notebook est le seul qui lit test.csv. Exécuté une fois, le [date et heure]. »
- [x] Réentraîner le modèle choisi sur tout `train.csv`, l'appliquer à `test.csv`, calculer la précision sur le top 10 % et le bénéfice pour 1 000 passagers.
- [x] Appliquer aussi la règle simple à `test.csv`, pour que la comparaison finale soit honnête.
- [x] Enregistrer les chiffres dans `results/`.
- [x] **Si le résultat déçoit, on ne retouche pas le modèle.** On rapporte le chiffre tel quel et on commente l'écart avec la validation croisée. Modifier le modèle après avoir vu le test, c'est exactement ce que le sujet interdit.
- [x] Vérification : chercher `load_test` et `test.csv` dans tout le dépôt. Ils ne doivent apparaître que dans `common.py` (la définition) et le notebook 04.

### Étape 6 — Rapport (B assemble, chacun écrit sa partie, jour 2)

| Page | Contenu | Auteur |
|---|---|---|
| 1 | Résumé pour la directrice : le problème, 3 constats, 3 recommandations, le gain en euros | tous |
| 2 | Données et exploration, limites | A |
| 3–4 | Facteurs : tableau lié / actionnable / causal | B |
| 5–6 | Modèles : points de comparaison, validation, coût des erreurs, choix, résultat final sur test | C |
| 7 | Recommandations | B |
| 8 | Protection des données | A |
| Annexes | Détails techniques, figures supplémentaires | tous |

- [ ] Chaque chiffre du rapport est recopié depuis `results/` ou une sortie de notebook, jamais de mémoire.
- [ ] Faire relire la page 1 par quelqu'un qui n'a pas suivi le projet : s'il ne comprend pas, la directrice non plus.

### Étape 7 — Vérification de reproductibilité (A, fin de jour 2)

- [ ] Dans chaque notebook : menu « Restart Kernel and Run All ». Tout doit s'exécuter de haut en bas sans erreur.
- [ ] Le refaire une seconde fois et comparer les fichiers de `results/` : ils doivent être identiques.
- [ ] Idéalement, cloner le dépôt dans un dossier vide sur un autre ordinateur et relancer. C'est le seul vrai test de « le code tourne tel quel ».
- [ ] Vérifier que le README explique l'ordre d'exécution : 01 → 02 → 03 → 04.

### Étape 8 — Oral (C prépare les slides, répétition à trois)

- [ ] Proposition de découpage des 10 minutes : 1 min contexte, 3 min facteurs (B), 3 min modèle et euros (C), 2 min protection des données (A), 1 min recommandations.
- [ ] Répéter au moins une fois chronomètre en main.
- [ ] Préparer les questions probables :
  - Pourquoi ne pas avoir utilisé les notes dans le modèle ?
  - Comment avez-vous choisi le modèle sans toucher à `test.csv` ?
  - Qu'est-ce que le modèle apporte de plus que « approcher les voyageurs personnels » ?
  - Le wifi cause-t-il vraiment l'insatisfaction ?
  - Que faites-vous des enfants ?
  - Pourquoi pas l'accuracy ?

---

## 7. Git, pas à pas

Le sujet note l'historique : il doit montrer que le travail a été partagé. **Un seul commit par personne ne suffit pas.** Visez un commit à chaque petite étape terminée, soit plusieurs par jour chacun, depuis votre propre compte.

Routine à chaque fois que vous avez fini quelque chose :

```bash
git pull --rebase                  # récupérer le travail des autres d'abord
git status                         # voir ce que vous avez modifié
git add notebooks/02_facteurs.ipynb figures/   # ajouter VOS fichiers, pas "git add ."
git commit -m "Facteurs : taux de satisfaction par note de service"
git push
```

Règles pour éviter les ennuis :

- Ne modifiez que vos propres fichiers. Si vous avez besoin d'un changement dans `common.py`, demandez à A, ou prévenez les deux autres avant.
- Faites `git pull --rebase` avant de commencer à travailler et avant chaque `push`.
- Un message de commit dit ce qui a été fait : « Modèles : ajout de la régression logistique », pas « update ».
- Si git affiche un conflit, n'improvisez pas : appelez les deux autres, on le règle à trois.

---

## 8. Calendrier indicatif

| Moment | A | B | C |
|---|---|---|---|
| J1 matin | Étape 0 (à trois), puis exploration | Étape 0, puis notes de service (niveau 1) | Étape 0, puis liste des variables + mesure métier + points de comparaison |
| J1 après-midi | Fin de l'exploration, décisions de nettoyage dans `common.py` | Analyse à profil égal (niveau 2) | Régression logistique + arbre, validation croisée |
| J2 matin | Protection des données | Tableau des facteurs, recommandations | Comparaison finale, coût des erreurs, choix du modèle |
| J2 après-midi | Vérification de reproductibilité, README | Assemblage du rapport | Évaluation sur `test.csv`, slides |
| J2 fin | Résumé page 1 et répétition de l'oral, à trois | | |

Point de synchronisation de 10 minutes à chaque demi-journée : chacun dit ce qu'il a fini, ce qui le bloque, et ce dont il a besoin des autres.

---

## 9. Guide pas à pas : le code à taper

Ce guide reprend les étapes de la section 6 avec le code exact. Pour chaque cellule : ce qu'on tape, **pourquoi**, et **ce qu'on doit voir**. Si le résultat est différent, on s'arrête et on cherche avant de continuer.

Tout le code a été testé sur `train.csv`. Les résultats attendus viennent de ce test. Seul le notebook 04 n'a pas été lancé, puisqu'il lit `test.csv`.

### Les règles du travail à trois

- **Une seule personne modifie un notebook à la fois.** Deux personnes sur le même notebook = conflit git.
- **On change de clavier à chaque étape**, pour que l'historique montre des commits des trois comptes.
- Avant de commencer : `git pull`. Dès qu'une étape est finie : `git add` de ses fichiers, `git commit -m "..."`, `git push`.
- Dans un notebook, on ajoute une cellule avec **+ Code**, on la lance avec **Maj + Entrée**.
- Si le terminal affiche `>>`, il attend la fin d'une commande (souvent un guillemet oublié) : **Ctrl + C** et on retape.
- Un fichier avec un point `●` sur son onglet n'est pas enregistré : **Ctrl + S**.

---

### Étape 1 — Explorer (`notebooks/01_exploration.ipynb`)

Le notebook contient déjà 4 cellules (chargement et nettoyage). On clique **Run All**, puis on ajoute les cellules suivantes à la fin.

**Cellule 1.1 : préparer les graphiques**

```python
import matplotlib.pyplot as plt

(RACINE / "figures").mkdir(exist_ok=True)
```

*Pourquoi :* `matplotlib` dessine les graphiques. La seconde ligne crée le dossier `figures`, où on range chaque image pour le rapport.

**Cellule 1.2 : combien de contents et de mécontents**

```python
compte = df["insatisfait"].map({1: "Neutre ou insatisfait", 0: "Satisfait"}).value_counts()
print(compte)

compte.plot(kind="bar", rot=0)
plt.ylabel("Nombre de passagers")
plt.title("Répartition de la satisfaction")
plt.savefig(RACINE / "figures" / "01_cible.png", bbox_inches="tight")
plt.show()
```

*Pourquoi :* c'est le premier chiffre à montrer à la directrice. `map` remplace 1 et 0 par des mots, `value_counts` compte, `savefig` enregistre l'image.

*On doit voir :* 58 879 mécontents et 45 025 contents (56,7 % contre 43,3 %).

**Cellule 1.3 : qui est mécontent**

```python
for col in ["Type of Travel", "Class", "Customer Type"]:
    print((df.groupby(col)["insatisfait"].mean() * 100).round(1))
    print()
```

*Pourquoi :* `groupby` range les passagers par groupe. La moyenne d'une colonne de 0 et de 1 donne directement le pourcentage de mécontents du groupe.

*On doit voir :* voyage personnel 89,8 %, affaires 41,7 % ; Eco 81,4 %, Eco Plus 75,4 %, Business 30,6 % ; non fidèle 76,3 %, fidèle 52,3 %.

**Cellule 1.4 : où sont les 0 dans les notes**

```python
zeros = (brut[RATING_COLS] == 0).sum().sort_values(ascending=False)
print(zeros)
```

*Pourquoi :* le sujet dit qu'un 0 veut dire « pas de réponse ». On regarde `brut` (avant nettoyage), car dans `df` les 0 sont déjà devenus des cases vides.

*On doit voir :* presque tous les 0 sont dans 4 notes : horaires (5 300), réservation en ligne (4 487), wifi (3 103), embarquement en ligne (2 428).

**Cellule 1.5 : les 0 du wifi ne sont pas du hasard**

```python
sans_wifi = brut[brut["Inflight wifi service"] == 0]
print(len(sans_wifi), "passagers ont 0 au wifi")
print((sans_wifi["satisfaction"] == "satisfied").mean().round(3), "sont satisfaits")
```

*Pourquoi :* si les 0 étaient des mauvaises notes, ces passagers seraient mécontents. On vérifie.

*On doit voir :* 3 103 passagers, dont 99,7 % satisfaits. Ce ne sont donc pas des mauvaises notes : on a raison de les traiter comme « sans réponse ». À dire dans le rapport, car ce groupe est très particulier.

**Cellule 1.6 : âge, distance, retards**

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
df["Age"].plot(kind="hist", bins=30, ax=axes[0], title="Âge")
df["Flight Distance"].plot(kind="hist", bins=30, ax=axes[1], title="Distance du vol")
df["Departure Delay in Minutes"].plot(kind="hist", bins=50, ax=axes[2], title="Retard au départ (minutes)", logy=True)
plt.savefig(RACINE / "figures" / "01_distributions.png", bbox_inches="tight")
plt.show()

df[["Age", "Flight Distance", "Departure Delay in Minutes", "Arrival Delay in Minutes"]].describe().round(1)
```

*Pourquoi :* un histogramme montre comment les valeurs se répartissent et fait ressortir les valeurs bizarres. `logy=True` écrase l'échelle, sinon les rares gros retards sont invisibles. `describe` donne minimum, moyenne et maximum.

*On doit voir :* âge de 7 à 85 ans (moyenne 39) ; la moitié des vols n'ont aucun retard ; retard maximum 1 592 minutes au départ.

*Décision à écrire :* on garde les très gros retards (1 093 passagers ont plus de 3 h de retard à l'arrivée). Ce sont de vrais retards, pas des erreurs, et ce sont justement des passagers qu'on veut repérer.

**Cellule 1.7 : l'âge et les mineurs**

```python
tranches = pd.cut(df["Age"], bins=[0, 17, 25, 40, 60, 100],
                  labels=["moins de 18", "18-25", "26-40", "41-60", "plus de 60"])
print((df.groupby(tranches, observed=True)["insatisfait"].mean() * 100).round(1))
print((df["Age"] < 18).sum(), "mineurs")
```

*Pourquoi :* `pd.cut` découpe l'âge en tranches. Le sujet insiste sur les enfants : il faut savoir combien ils sont.

*On doit voir :* moins de 18 ans 83,6 %, 18-25 ans 65,6 %, 26-40 ans 59,1 %, 41-60 ans 42,3 %, plus de 60 ans 79,2 %. 7 931 mineurs.

**Cellule 1.8 : classe et motif en même temps**

```python
croise = df.pivot_table(index="Class", columns="Type of Travel", values="insatisfait", aggfunc="mean") * 100
croise.round(1)
```

*Pourquoi :* les voyageurs d'affaires sont surtout en Business. On croise les deux pour savoir lequel compte vraiment.

*On doit voir :*

| | Affaires | Personnel |
|---|---|---|
| Business | 28,0 | 87,8 |
| Eco | 70,4 | 89,8 |
| Eco Plus | 60,7 | 91,3 |

Les voyageurs personnels sont mécontents quelle que soit la classe. Les voyageurs d'affaires, eux, dépendent beaucoup de la classe.

**Cellule 1.9 : les retards**

```python
print(df["Departure Delay in Minutes"].corr(df["Arrival Delay in Minutes"]).round(3))

retard = pd.cut(df["Arrival Delay in Minutes"], bins=[-1, 0, 15, 60, 2000],
                labels=["aucun", "1 à 15 min", "16 à 60 min", "plus d'1 h"])
print((df.groupby(retard, observed=True)["insatisfait"].mean() * 100).round(1))
```

*Pourquoi :* la corrélation va de 0 (aucun rapport) à 1 (c'est la même information). On vérifie aussi si le retard rend mécontent.

*On doit voir :* corrélation 0,966, donc les deux retards disent presque la même chose. Mécontents : 52,7 % sans retard, 58,7 % de 1 à 15 min, 64,5 % de 16 à 60 min, 64,3 % au-delà. Le retard compte, mais bien moins que le motif du voyage.

**Enregistrer :**

```bash
git add notebooks/01_exploration.ipynb figures/
git commit -m "Exploration : cible, profils, zéros, âge, retards"
git push
```

---

### Étape 2 — Expliquer la satisfaction (`notebooks/02_facteurs.ipynb`)

On crée un nouveau notebook `02_facteurs.ipynb` dans `notebooks/`. Ici les 14 notes sont autorisées.

**Cellule 2.1 : charger**

```python
import sys
sys.path.append("..")

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from src.common import load_train, RATING_COLS, RACINE, SEED

df = load_train()
df["satisfait"] = 1 - df["insatisfait"]

(RACINE / "figures").mkdir(exist_ok=True)
(RACINE / "results").mkdir(exist_ok=True)
```

*Pourquoi :* `sys.path.append("..")` permet au notebook de trouver le dossier `src`. On crée une colonne `satisfait` (l'inverse de `insatisfait`), plus naturelle quand on parle de ce qui rend content. On crée aussi `results`, où on range les tableaux chiffrés.

**Cellule 2.2 : niveau 1, satisfaction selon la note donnée**

```python
tableau = pd.DataFrame({note: df.groupby(note)["satisfait"].mean() * 100 for note in RATING_COLS}).T
tableau.columns = [1, 2, 3, 4, 5]
tableau["ecart"] = tableau[5] - tableau[1]
tableau = tableau.sort_values("ecart", ascending=False).round(1)

tableau.to_csv(RACINE / "results" / "02_satisfaction_par_note.csv")
tableau
```

*Pourquoi :* pour chaque service, on calcule le pourcentage de contents parmi ceux qui ont mis 1, puis 2, jusqu'à 5. L'« écart » est la différence entre ceux qui ont mis 5 et ceux qui ont mis 1 : plus il est grand, plus ce service est lié à la satisfaction.

*On doit voir :* en tête, embarquement en ligne (écart 73,4), wifi (66,5), divertissement (50,9), service à bord (44,9), confort du siège (42,7). En bas, emplacement de la porte (7,7) et horaires (−6,1) : aucun lien.

**Cellule 2.3 : le graphique**

```python
tableau["ecart"].sort_values().plot(kind="barh", figsize=(8, 6))
plt.xlabel("Écart de satisfaction entre la note 5 et la note 1 (points)")
plt.title("Quels services sont les plus liés à la satisfaction ?")
plt.savefig(RACINE / "figures" / "02_ecart_par_note.png", bbox_inches="tight")
plt.show()
```

*Pourquoi :* c'est le graphique principal de la partie « facteurs » du rapport. Une barre par service, la plus longue en haut.

**Cellule 2.4 : niveau 2, à profil égal**

```python
def ecart(groupe):
    resultat = {}
    for note in RATING_COLS:
        taux = groupe.groupby(note)["satisfait"].mean() * 100
        resultat[note] = taux[5] - taux[1]
    return pd.Series(resultat).round(1)

affaires_business = df[(df["Type of Travel"] == "Business travel") & (df["Class"] == "Business")]
affaires_eco = df[(df["Type of Travel"] == "Business travel") & (df["Class"] == "Eco")]
perso_eco = df[(df["Type of Travel"] == "Personal Travel") & (df["Class"] == "Eco")]

profil = pd.DataFrame({
    "tous": ecart(df),
    "affaires en Business": ecart(affaires_business),
    "affaires en Eco": ecart(affaires_eco),
    "personnel en Eco": ecart(perso_eco),
}).sort_values("tous", ascending=False)

profil.to_csv(RACINE / "results" / "02_ecart_par_profil.csv")
profil
```

*Pourquoi :* les passagers Business notent mieux **et** sont plus contents. Un service peut donc sembler important juste parce que ce sont eux qui le notent bien. On refait le même calcul dans trois groupes de passagers qui se ressemblent. Si un service reste important dans chaque groupe, il est crédible.

*On doit voir :* chez les voyageurs personnels en Eco, presque tous les écarts tombent à zéro (divertissement −0,1, siège 0,2, propreté 0,0). Seuls restent le wifi (100), la réservation en ligne (72,0) et l'embarquement en ligne (31,7). **C'est une conclusion forte :** pour ces passagers, améliorer le siège ou le repas ne changerait presque rien.

**Cellule 2.5 : niveau 3, vérification par une autre méthode**

```python
PROFIL = ["Customer Type", "Type of Travel", "Class", "Age", "Flight Distance", "Arrival Delay in Minutes"]
X = pd.get_dummies(df[RATING_COLS + PROFIL], drop_first=True).astype(float).fillna(0)
y = df["satisfait"]

X_app, X_val, y_app, y_val = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)

foret = RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1).fit(X_app, y_app)
print("Bonnes réponses sur la validation :", round(foret.score(X_val, y_val), 3))

imp = permutation_importance(foret, X_val, y_val, n_repeats=5, random_state=SEED, n_jobs=-1)
importance = pd.Series(imp.importances_mean, index=X.columns).sort_values(ascending=False).round(4)

importance.to_csv(RACINE / "results" / "02_importance.csv")
importance
```

*Pourquoi, ligne par ligne :*
- `get_dummies` transforme les mots (« Eco », « Business ») en colonnes de 0 et de 1, car un modèle ne lit que des nombres.
- `fillna(0)` remet 0 dans les notes vides. Pour une forêt, 0 devient simplement une catégorie « pas de réponse ».
- `train_test_split` met de côté 20 % de `train` pour vérifier. On ne touche pas à `test.csv`.
- La forêt aléatoire est un grand nombre d'arbres de décision qui votent.
- L'importance par permutation mélange une colonne au hasard et regarde de combien le modèle se dégrade. Si rien ne change, la colonne ne servait à rien.

*On doit voir (20 à 30 secondes de calcul) :* 96,3 % de bonnes réponses. En tête : voyage personnel (0,131), wifi (0,130), client non fidèle (0,053), embarquement en ligne (0,034), enregistrement (0,028).

*Ce qu'on en conclut :* les deux méthodes désignent le wifi et l'embarquement en ligne. On peut les recommander avec confiance. Le divertissement, deuxième au niveau 1, descend ici : il est donc moins sûr.

**Ensuite, sans code :** remplir le tableau « lié / actionnable / cause » de l'étape 2 (section 6) avec ces chiffres, puis écrire 3 à 5 recommandations.

```bash
git add notebooks/02_facteurs.ipynb figures/ results/
git commit -m "Facteurs : satisfaction par note, à profil égal, importance"
git push
```

---

### Étape 3 — Prédire les mécontents (`notebooks/03_modeles.ipynb`)

**D'abord, compléter `src/common.py`.** On ajoute ceci à la fin du fichier (une seule personne, les autres font `git pull` ensuite) :

```python
# Ce que la compagnie connaît à l'atterrissage (aucune note du questionnaire)
LANDING_COLS = [
	"Customer Type",
	"Age",
	"Type of Travel",
	"Class",
	"Flight Distance",
	"Departure Delay in Minutes",
	"Arrival Delay in Minutes",
]


def precision_top10(y_vrai, scores):
	"""Part de vrais insatisfaits parmi les 10 % de passagers les mieux classés."""
	n = int(len(scores) * 0.10)
	meilleurs = np.argsort(-np.asarray(scores), kind="stable")[:n]
	return np.asarray(y_vrai)[meilleurs].mean()


def benefice_pour_1000(precision):
	"""Bénéfice en euros quand on approche 100 passagers sur 1 000."""
	return 100 * (100 * precision - 40)
```

*Pourquoi dans `common.py` :* les notebooks 03 et 04 doivent utiliser exactement la même liste et la même mesure. Écrites une seule fois, elles ne peuvent pas diverger.

*Pourquoi cette liste :* ce sont les informations du dossier de réservation et du vol. Les 14 notes n'y sont pas, car le questionnaire est rempli après le vol. Le genre n'y est pas non plus : on montre plus bas qu'il n'apporte rien.

*Pourquoi `kind="stable"` :* quand deux passagers ont le même score, l'ordre reste toujours le même. Sans ça, deux lancements pourraient donner deux chiffres différents.

> Après avoir modifié `common.py`, il faut cliquer **Restart** dans les notebooks ouverts, sinon ils gardent l'ancienne version en mémoire.

**Cellule 3.1 : charger**

```python
import sys
sys.path.append("..")

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from src.common import load_train, LANDING_COLS, precision_top10, benefice_pour_1000, RACINE, SEED

df = load_train()
y = df["insatisfait"]
X = pd.get_dummies(df[LANDING_COLS], drop_first=True).astype(float)

(RACINE / "results").mkdir(exist_ok=True)
print(X.columns.tolist())
```

*Pourquoi :* `y` est ce qu'on veut deviner, `X` ce qu'on a le droit d'utiliser.

*On doit voir :* 8 colonnes : `Age`, `Flight Distance`, les deux retards, `Customer Type_disloyal Customer`, `Type of Travel_Personal Travel`, `Class_Eco`, `Class_Eco Plus`.

**Cellule 3.2 : la façon de comparer sans `test.csv`**

```python
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

def evaluer(modele, donnees):
    resultats = []
    for i_app, i_val in cv.split(donnees, y):
        modele.fit(donnees.iloc[i_app], y.iloc[i_app])
        scores = modele.predict_proba(donnees.iloc[i_val])[:, 1]
        resultats.append(precision_top10(y.iloc[i_val], scores))
    return np.array(resultats)
```

*Pourquoi :* c'est la validation croisée. On coupe `train` en 5 parts. Le modèle apprend sur 4 parts (`fit`), puis donne à chaque passager de la 5e un score de risque (`predict_proba`). On regarde si les 10 % les mieux classés sont vraiment mécontents. On recommence 5 fois en changeant la part mise de côté. On obtient 5 mesures : leur moyenne, et leur écart qui dit si le résultat est stable.

**Cellule 3.3 : les points de comparaison sans modèle**

```python
hasard = y.mean()

regle = []
for i_app, i_val in cv.split(X, y):
    scores = (df["Type of Travel"].iloc[i_val] == "Personal Travel").astype(int)
    regle.append(precision_top10(y.iloc[i_val], scores))
regle = np.array(regle)

print("Hasard :", round(hasard, 3))
print("Règle simple :", regle.mean().round(3))
```

*Pourquoi :* le sujet demande de montrer ce que le modèle apporte par rapport à la règle la plus simple. « Au hasard » = on approche n'importe qui. « Règle simple » = on approche des voyageurs personnels, sans aucun calcul.

*On doit voir :* hasard 0,567, règle simple 0,897.

**Cellule 3.4 : comparer trois modèles**

```python
modeles = {
    "Régression logistique": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Arbre de décision (4 niveaux)": DecisionTreeClassifier(max_depth=4, random_state=SEED),
    "Gradient boosting": HistGradientBoostingClassifier(random_state=SEED),
}

lignes = [
    {"stratégie": "Hasard", "précision": hasard, "écart": 0},
    {"stratégie": "Règle simple (voyage personnel)", "précision": regle.mean(), "écart": regle.std()},
]
for nom, modele in modeles.items():
    r = evaluer(modele, X)
    lignes.append({"stratégie": nom, "précision": r.mean(), "écart": r.std()})

tableau = pd.DataFrame(lignes)
tableau["bénéfice pour 1000"] = benefice_pour_1000(tableau["précision"]).round(0)
tableau["gain sur la règle simple"] = tableau["bénéfice pour 1000"] - tableau.loc[1, "bénéfice pour 1000"]

tableau.to_csv(RACINE / "results" / "03_comparaison.csv", index=False)
tableau.round(3)
```

*Pourquoi ces trois modèles :*
- **Régression logistique** : donne un poids à chaque information et les additionne. Simple à expliquer.
- **Arbre de décision** : une suite de questions oui/non. On peut le dessiner pour la directrice.
- **Gradient boosting** : des centaines de petits arbres. Souvent le meilleur, mais impossible à lire.

`make_pipeline(StandardScaler(), ...)` met toutes les colonnes à la même échelle avant la régression. Le `Pipeline` garantit que cette mise à l'échelle est apprise sur les 4 parts d'entraînement seulement.

*On doit voir :*

| Stratégie | Précision | Bénéfice pour 1 000 | Gain sur la règle simple |
|---|---|---|---|
| Hasard | 0,567 | 1 667 € | −3 298 € |
| Règle simple | 0,897 | 4 965 € | 0 € |
| Régression logistique | 0,937 | 5 368 € | +403 € |
| Arbre (4 niveaux) | 0,955 | 5 551 € | +586 € |
| Gradient boosting | 0,965 | 5 653 € | +688 € |

L'écart entre les 5 parts est partout inférieur à 0,01 : les résultats sont stables.

**Cellule 3.5 : lire l'arbre**

```python
arbre = DecisionTreeClassifier(max_depth=4, random_state=SEED).fit(X, y)
print(export_text(arbre, feature_names=X.columns.tolist()))
```

*Pourquoi :* la directrice doit comprendre ce que fait le modèle. `export_text` écrit l'arbre comme une suite de questions.

*On doit voir :* la première question est `Class_Eco`, la deuxième `Type of Travel_Personal Travel`, puis la fidélité, le retard à l'arrivée et l'âge.

**Cellule 3.6 : faut-il l'âge ? le genre ?**

```python
gb = HistGradientBoostingClassifier(random_state=SEED)

essais = {
    "modèle de base": X,
    "sans l'âge": X.drop(columns=["Age"]),
    "avec le genre": pd.get_dummies(df[LANDING_COLS + ["Gender"]], drop_first=True).astype(float),
}
for nom, donnees in essais.items():
    p = evaluer(gb, donnees).mean()
    print(nom, ":", round(p, 3), "->", round(benefice_pour_1000(p)), "€")
```

*Pourquoi :* la partie « protection des données » demande si chaque information est nécessaire. On mesure ce qu'on perd en retirant l'âge, et ce qu'on gagne en ajoutant le genre.

*On doit voir :* base 0,965 (5 653 €) ; sans l'âge 0,955 (5 553 €) ; avec le genre 0,965 (5 653 €). **Le genre n'apporte rien : on ne l'utilise pas. L'âge apporte 100 € pour 1 000 passagers** : c'est le chiffre à mettre en face de la question des mineurs.

**Cellule 3.7 : le coût des erreurs**

```python
p = tableau.loc[4, "précision"]   # ligne du modèle choisi
print("Sur 1 000 passagers, 100 approchés :")
print(round(100 * p), "vrais insatisfaits approchés")
print(round(100 * (1 - p)), "fausses alertes, soit", round(100 * (1 - p) * 40), "€ dépensés pour rien")
print(round(1000 * hasard - 100 * p), "insatisfaits non approchés")
```

*Pourquoi :* le sujet demande ce que coûtent les erreurs du modèle. Il y en a deux sortes : la fausse alerte (on approche un passager content, 40 € perdus) et l'oubli (un mécontent qu'on ne va pas voir).

*On doit voir (pour le gradient boosting) :* 97 vrais mécontents approchés, 3 fausses alertes (139 €), et **470 mécontents non approchés**. Ce dernier chiffre est le plus important à dire : ce n'est pas la faute du modèle, c'est la limite de « 1 passager sur 10 ».

**Ensuite, sans code : choisir le modèle.** Le gradient boosting rapporte 102 € de plus que l'arbre pour 1 000 passagers, mais on ne peut pas l'expliquer. L'arbre se lit en une page. C'est à vous de trancher et de le justifier : les deux choix se défendent.

```bash
git add src/common.py notebooks/03_modeles.ipynb results/
git commit -m "Modèles : points de comparaison, 3 modèles, coût des erreurs"
git push
```

---

### Étape 4 — Protection des données (pas de code)

On écrit directement dans le rapport, en répondant aux trois questions du sujet. Les consignes détaillées sont à l'étape 4 de la section 6. Les chiffres à reprendre des notebooks :

- 7 931 mineurs dans les données, mécontents à 83,6 % (cellule 1.7).
- Le genre n'améliore pas le modèle (cellule 3.6) : il n'a aucune raison d'être utilisé.
- L'âge apporte 100 € pour 1 000 passagers (cellule 3.6) : à peser face à la protection des mineurs.

---

### Étape 5 — Le contrôle final (`notebooks/04_evaluation_finale.ipynb`)

**À faire une seule fois, quand le modèle est choisi et que plus rien ne changera.** Ce code n'a volontairement pas été testé.

Première cellule, en **Markdown** (pas en Code) :

```
Ce notebook est le seul qui évalue le modèle sur test.csv.
Exécuté une seule fois, le [date et heure].
```

**Cellule 5.1 :**

```python
import sys
sys.path.append("..")

import json
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from src.common import load_train, load_test, LANDING_COLS, precision_top10, benefice_pour_1000, RACINE, SEED

train = load_train()
test = load_test()

X_train = pd.get_dummies(train[LANDING_COLS], drop_first=True).astype(float)
X_test = pd.get_dummies(test[LANDING_COLS], drop_first=True).astype(float)
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)
```

*Pourquoi :* on prépare `test` exactement comme `train`. `reindex` force les mêmes colonnes dans le même ordre.

**Cellule 5.2 :**

```python
modele = HistGradientBoostingClassifier(random_state=SEED)   # remplacer par le modèle choisi à l'étape 3
modele.fit(X_train, train["insatisfait"])
scores = modele.predict_proba(X_test)[:, 1]

p_modele = precision_top10(test["insatisfait"], scores)
p_regle = precision_top10(test["insatisfait"], (test["Type of Travel"] == "Personal Travel").astype(int))

resultat = {
    "precision_modele": round(float(p_modele), 4),
    "benefice_modele": round(float(benefice_pour_1000(p_modele))),
    "precision_regle_simple": round(float(p_regle), 4),
    "benefice_regle_simple": round(float(benefice_pour_1000(p_regle))),
}
with open(RACINE / "results" / "04_evaluation_finale.json", "w") as f:
    json.dump(resultat, f, indent=2)
print(resultat)
```

*Pourquoi :* le modèle apprend sur tout `train`, puis classe les passagers de `test` qu'il n'a jamais vus. On mesure aussi la règle simple sur `test`, pour que la comparaison finale soit honnête.

*On doit voir :* des chiffres proches de ceux de la validation croisée (cellule 3.4). **S'ils sont moins bons, on ne touche à rien** : on les rapporte tels quels et on commente l'écart.

```bash
git add notebooks/04_evaluation_finale.ipynb results/
git commit -m "Évaluation finale sur test.csv (exécutée une seule fois)"
git push
```

---

### Étape 6 — Le rapport

On suit le tableau de l'étape 6 (section 6). Chaque chiffre est recopié depuis un fichier de `results/` ou une sortie de notebook. Chaque image vient de `figures/`.

---

### Étape 7 — Vérifier que tout se relance

1. Dans chaque notebook de 01 à 03 : **Restart**, puis **Run All**. Aucune erreur ne doit apparaître. Le notebook 04 n'est pas relancé : il ne s'exécute qu'une fois.
2. Dans le terminal : `git status`. **Aucun fichier de `results/` ne doit apparaître comme modifié.** S'il n'y en a aucun, c'est la preuve que relancer le code donne les mêmes chiffres.
3. Noter les versions des bibliothèques : `pip freeze > requirements.txt`.
4. Compléter le README : qui a fait quoi, et l'ordre de lancement (01, 02, 03, puis 04).

---

### Étape 8 — L'oral

On suit l'étape 8 de la section 6. Les réponses aux questions probables sont dans ce guide :

| Question | Où est la réponse |
|---|---|
| Pourquoi pas les notes dans le modèle ? | Étape 3, liste `LANDING_COLS` |
| Comment choisir sans `test.csv` ? | Cellule 3.2, validation croisée |
| Que gagne-t-on sur la règle simple ? | Cellule 3.4, dernière colonne |
| Le wifi cause-t-il la satisfaction ? | Cellules 1.5, 2.4 et 2.5 |
| Que faites-vous des enfants ? | Cellules 1.7 et 3.6 |
| Pourquoi pas l'accuracy ? | Section 3, calcul économique |
