# Plan de travail — Rush 3 « Customer Satisfaction »

Ce document dit qui fait quoi, dans quel ordre, et pourquoi. Il est écrit pour être suivi pas à pas, même sans expérience en code. Cochez les cases `[ ]` → `[x]` au fur et à mesure.

> Remplacez **A**, **B**, **C** par vos prénoms dès le début (ici et dans le README).

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
├── data/
│   ├── train.csv
│   └── test.csv
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
- [ ] Créer les dossiers `data/`, `src/`, `notebooks/`, `figures/`, `results/`, `rapport/` et déplacer les deux CSV dans `data/`.
- [ ] Créer `requirements.txt` (pandas, numpy, scikit-learn, matplotlib, seaborn, jupyter) puis installer : `pip install -r requirements.txt`. Une fois que tout marche, noter les versions exactes avec `pip freeze` : deux versions différentes d'une bibliothèque peuvent donner des chiffres différents.
- [ ] **A** écrit `src/common.py` pendant que B et C regardent. Il contient :
  - `load_train()` : lit `data/train.csv`, supprime `Unnamed: 0` et `id`, crée une colonne `insatisfait` qui vaut 1 si `satisfaction` est « neutral or dissatisfied », sinon 0.
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

- [ ] **Établir la liste des variables connues à l'atterrissage** et la justifier (le sujet dit que c'est à nous de l'établir) :

  | Variable | Connue à l'atterrissage ? | Remarque |
  |---|---|---|
  | Classe, type de voyage, fidélité | oui | dossier de réservation |
  | Distance du vol | oui | |
  | Retard au départ, retard à l'arrivée | oui | très corrélés : en garder un seul ou les deux, à tester |
  | Âge | oui | question des mineurs → décider avec A |
  | Genre | oui | n'apporte presque rien (57,3 % contre 56,1 %) → l'exclure se défend bien |
  | Les 14 notes | **non** | questionnaire rempli après le vol |

- [ ] **Découper `train.csv` pour comparer les modèles**, puisque `test.csv` est interdit. On utilise la validation croisée à 5 blocs : on coupe les données en 5 parts, on entraîne sur 4, on mesure sur la 5e, et on recommence 5 fois en changeant la part mise de côté. On obtient 5 mesures, donc une moyenne et une idée de sa stabilité.
  ```python
  from sklearn.model_selection import StratifiedKFold
  cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
  ```
- [ ] **Écrire la mesure métier** (une seule fois, réutilisée partout) :
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
- [ ] **Les points de comparaison sans modèle** : approche au hasard, puis la règle simple (voyageurs personnels). Les mesurer avec la même validation croisée.
- [ ] **Modèle 1 : régression logistique.** Simple, et chaque variable reçoit un poids qu'on peut expliquer à la directrice.
- [ ] **Modèle 2 : arbre de décision peu profond** (3 ou 4 niveaux). Il se lit comme une suite de questions : « voyage personnel ? → classe Eco ? → … ».
- [ ] **Modèle 3 (si le temps le permet) : forêt aléatoire ou gradient boosting.** Souvent plus performant, mais c'est une boîte noire.
- [ ] Mettre le prétraitement (remplissage des valeurs manquantes, encodage des catégories) **dans un `Pipeline` scikit-learn**. Sinon le nettoyage « voit » les données de validation et les scores sont trop optimistes.
- [ ] Tableau comparatif : pour chaque stratégie, précision sur le top 10 %, bénéfice pour 1 000 passagers, et écart entre les 5 blocs.
- [ ] **Coût des erreurs**, en mots simples :
  - Fausse alerte (on approche un passager satisfait) : 40 € dépensés pour rien.
  - Oubli (un insatisfait pas approché) : 100 € de gain espéré manqués. Avec une capacité de 10 % et 56,7 % d'insatisfaits, la grande majorité sera forcément oubliée : le dire clairement.
- [ ] **Choisir le modèle à déployer** et l'argumenter sur trois critères : bénéfice, facilité d'explication, données personnelles nécessaires. Si un modèle complexe ne rapporte que quelques euros de plus que la règle simple, recommander le plus simple est une conclusion valable.
- [ ] Tester le modèle avec et sans l'âge, avec et sans le genre : combien perd-on ? Ce chiffre sert directement à A pour la partie protection des données.

### Étape 4 — Protection des données (A, jour 2)

But : dire à quelles conditions le signalement des passagers serait acceptable. Le sujet impose trois réponses.

- [ ] **Les conditions.** Les données ont été collectées pour mesurer la satisfaction ; signaler des passagers au personnel est un usage nouveau (RGPD, principe de limitation des finalités, art. 5 et 6.4). Points à traiter : sur quelle base légale (consentement ou intérêt légitime), information des passagers, droit de s'y opposer (art. 21), analyse d'impact avant le lancement (art. 35), durée de conservation, et le fait que la plupart des passagers signalés n'ont jamais répondu à un questionnaire.
- [ ] **Les enfants.** Les mineurs ont une protection renforcée (considérant 38). Proposer une règle nette, par exemple : aucun mineur n'est signalé individuellement ; s'il voyage accompagné, on s'adresse à l'adulte. Vérifier avec C ce que ça change au résultat.
- [ ] **Chaque variable du modèle**, dans un tableau : est-elle nécessaire ? acceptable ? Le principe est de n'utiliser que le strict nécessaire (minimisation). Une variable qui n'améliore pas le modèle n'a aucune raison d'y être : c'est l'argument pour le genre.
- [ ] **Ce que voit l'équipe au sol.** Proposer un écran concret : numéro de siège ou nom, et une mention neutre du type « attention prioritaire ». Pas de score, pas de motif, pas d'âge. Le personnel ne doit pas savoir *pourquoi* le passager est signalé.

Les numéros d'articles sont des points de départ : relisez le texte avant de les citer dans le rapport.

### Étape 5 — Évaluation finale sur `test.csv` (C, jour 2 après-midi)

À faire **une seule fois**, quand le modèle est définitivement choisi et que plus rien ne changera.

- [ ] Créer `04_evaluation_finale.ipynb`. En haut, une cellule de texte : « Ce notebook est le seul qui lit test.csv. Exécuté une fois, le [date et heure]. »
- [ ] Réentraîner le modèle choisi sur tout `train.csv`, l'appliquer à `test.csv`, calculer la précision sur le top 10 % et le bénéfice pour 1 000 passagers.
- [ ] Appliquer aussi la règle simple à `test.csv`, pour que la comparaison finale soit honnête.
- [ ] Enregistrer les chiffres dans `results/`.
- [ ] **Si le résultat déçoit, on ne retouche pas le modèle.** On rapporte le chiffre tel quel et on commente l'écart avec la validation croisée. Modifier le modèle après avoir vu le test, c'est exactement ce que le sujet interdit.
- [ ] Vérification : chercher `load_test` et `test.csv` dans tout le dépôt. Ils ne doivent apparaître que dans `common.py` (la définition) et le notebook 04.

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
