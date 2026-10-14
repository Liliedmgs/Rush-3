# Partie C : prédire les passagers mécontents

# 4. Qui approcher à l'atterrissage

## 4.1 La question et la bonne mesure

La compagnie veut approcher, dès l'atterrissage, les passagers qui risquent d'être mécontents. Elle ne peut en approcher que 10 %, soit 100 passagers sur 1 000. Il faut donc classer les passagers du plus au moins à risque, et approcher les 100 premiers.

Chaque approche coûte 40 €. Un mécontent sur trois ne revient pas (600 € perdus) et l'approche en récupère la moitié : approcher un vrai mécontent rapporte donc 100 €. Le bénéfice pour 1 000 passagers est :

**bénéfice = 100 × (100 × précision − 40)**

où la précision est la part de vrais mécontents parmi les 100 passagers approchés. L'approche est rentable dès 40 % de précision, et le maximum possible est de 6 000 €.

La bonne mesure n'est donc pas le pourcentage de bonnes réponses sur tous les passagers, mais **la précision sur les 10 % les mieux classés**, convertie en euros.

## 4.2 Ce que le modèle a le droit d'utiliser

Les modèles ont été comparés avec ce que la compagnie connaît au moment où l'avion atterrit :

| Information | D'où elle vient |
|---|---|
| Client fidèle ou non | programme de fidélité |
| Âge | dossier de réservation |
| Motif du voyage (affaires ou personnel) | déclaré à la réservation |
| Classe | billet |
| Distance du vol | vol |
| Retards au départ et à l'arrivée | mesurés par la compagnie |

Les 14 notes de service sont exclues : le questionnaire est rempli après le vol, et la plupart des passagers n'y répondent jamais. Le genre est exclu aussi : il n'améliore pas le modèle (section 4.4). La version déployée du modèle retenu n'utilise pas non plus l'âge (section 4.4).

## 4.3 Comparer sans tricher

Le fichier de test a été mis de côté jusqu'à la toute fin. Pour comparer les stratégies, le fichier d'analyse a été coupé en 5 parts : on apprend sur 4, on mesure sur la 5e, et on recommence 5 fois. Chaque chiffre ci-dessous est la moyenne de ces 5 mesures. L'écart entre les 5 parts est partout inférieur à 0,01 : les résultats sont stables.

Deux stratégies sans modèle servent de points de comparaison : approcher au hasard, et la règle simple « approcher les voyageurs personnels ».

| Stratégie | Précision sur les 10 % approchés | Bénéfice pour 1 000 passagers | Gain sur la règle simple |
|---|---|---|---|
| Au hasard | 56,7 % | 1 667 € | −3 298 € |
| Règle simple : voyageurs personnels | 89,7 % | 4 965 € | 0 € |
| Régression logistique | 93,7 % | 5 367 € | +402 € |
| Arbre de décision (4 niveaux) | 95,5 % | 5 551 € | +586 € |
| Gradient boosting | 96,5 % | 5 653 € | +688 € |

![Bénéfice de chaque stratégie](../figures/03_benefice_par_strategie.png)

La règle simple, sans aucun calcul, fait déjà presque tout le travail : elle atteint 4 965 € sur 6 000 € possibles. Les modèles ne se disputent que les 1 035 € restants. Le meilleur en récupère 688 €, soit environ 14 % de bénéfice en plus.

## 4.4 Faut-il l'âge ? le genre ?

Le principe de minimisation impose de n'utiliser une donnée personnelle que si elle sert. Chaque modèle a donc été mesuré avec et sans l'âge, et avec le genre en plus.

| Version | Arbre de décision (retenu) | Gradient boosting |
|---|---|---|
| Les 7 informations | 95,5 % · 5 551 € | 96,5 % · 5 653 € |
| Sans l'âge | 95,6 % · 5 563 € | 95,5 % · 5 553 € |
| Avec le genre | 95,5 % · 5 551 € | 96,5 % · 5 653 € |

Précision sur les 10 % approchés et bénéfice pour 1 000 passagers, validation croisée sur le fichier d'analyse.

- **Le genre n'apporte rien**, avec les deux modèles : il n'est pas utilisé.
- **L'âge n'apporte rien à l'arbre retenu** : sans lui, l'arbre fait aussi bien sur 3 des 5 parts et légèrement mieux sur les 2 autres (+12 € pour 1 000 passagers, un écart inférieur à la variation normale entre les parts). Il n'est utile qu'au gradient boosting (100 € pour 1 000 passagers).
**Décision : l'arbre est déployé sans l'âge.** Une donnée personnelle qui n'améliore pas le résultat ne doit pas être utilisée (minimisation). L'âge reste lu pour une seule chose : appliquer la règle « aucun mineur n'est signalé » (section 6.3).

| Version (validation croisée) | Tous les passagers | Aucun mineur signalé |
|---|---|---|
| Arbre testé (7 informations) | 95,5 % · 5 551 € | 95,2 % · 5 521 € |
| **Arbre déployé (sans l'âge)** | **95,6 % · 5 563 €** | **94,9 % · 5 494 €** |
| Règle simple (voyage personnel) | 89,7 % · 4 965 € | 89,9 % · 4 991 € |

Avec la règle des mineurs, la version déployée rapporte 5 494 € pour 1 000 passagers, soit 503 € de plus que la règle simple dans les mêmes conditions. Exclure les mineurs coûte 69 € à l'arbre sans l'âge (30 € à l'arbre avec l'âge) : c'est le prix de la protection des enfants, à peine plus de 1 % du gain.

Le contrôle final (section 4.7) a été fait avant cette décision, avec l'arbre à 7 informations. Il n'a pas été refait, car le fichier de test ne s'utilise qu'une fois.

## 4.5 Ce que coûtent les erreurs

Sur 1 000 passagers, avec l'arbre de décision, 100 sont approchés :

- **96 sont de vrais mécontents** : l'approche est utile.
- **4 sont des fausses alertes** : des passagers satisfaits approchés pour rien, soit 180 € dépensés sans retour.
- **471 mécontents ne sont pas approchés.** Ce n'est pas une faute du modèle : sur 1 000 passagers, 567 sont mécontents, et on ne peut en approcher que 100. Approcher plus de monde resterait rentable tant que la précision dépasse 40 %, mais cela demande plus de personnel.

Les fausses alertes coûtent peu ; l'oubli est la vraie limite, et il vient de la capacité, pas du modèle.

## 4.6 Le modèle retenu

Trois critères : le bénéfice, la facilité à l'expliquer, et les données personnelles nécessaires.

| | Règle simple | Arbre de décision | Gradient boosting |
|---|---|---|---|
| Bénéfice pour 1 000 passagers | 4 965 € | 5 551 € | 5 653 € |
| Facile à expliquer | oui | oui, en une page | non |
| Données nécessaires | motif du voyage | 6 informations, sans l'âge | 7 informations |

**Nous retenons l'arbre de décision.** Il rapporte 586 € de plus que la règle simple pour 1 000 passagers, et seulement 102 € de moins que le gradient boosting. Surtout, il se lit comme une suite de questions que la directrice et les équipes au sol peuvent comprendre et contester :

1. Le passager voyage-t-il en Eco ?
2. Voyage-t-il pour un motif personnel ?
3. Est-il client fidèle ?
4. Son vol est-il arrivé avec plus de 5 minutes de retard ?

Un voyageur personnel est presque toujours classé à risque, quelle que soit sa classe. Un voyageur d'affaires fidèle en Business est presque toujours satisfait. Entre les deux, c'est le retard à l'arrivée et la fidélité qui font la différence.

## 4.7 Le résultat final sur le fichier de test

Le modèle a été appris sur tout le fichier d'analyse, puis appliqué une seule fois aux 25 976 passagers du fichier de test, jamais vus jusque-là (56,1 % de mécontents). Ce contrôle a été fait avec l'arbre à 7 informations, âge compris, avant la décision de déployer la version sans l'âge ; sur le fichier d'analyse, les deux versions font jeu égal (95,5 % et 95,6 %).

| Stratégie | Précision (validation) | Précision (test) | Bénéfice sur le test pour 1 000 passagers |
|---|---|---|---|
| Arbre de décision | 95,5 % | 96,1 % | 5 611 € |
| Règle simple : voyageurs personnels | 89,7 % | 90,3 % | 5 034 € |

Les chiffres du test sont très proches de ceux de la validation, et même légèrement meilleurs : le modèle n'a pas appris par cœur le fichier d'analyse, il se généralise à de nouveaux passagers. L'arbre rapporte 577 € de plus que la règle simple pour 1 000 passagers, comme prévu en validation (586 €).

Sur 1 000 passagers de test, 100 approchés : 96 vrais mécontents, 4 fausses alertes (156 €), et 465 mécontents non approchés faute de capacité.

## 4.8 Les limites

- Le modèle apprend sur les passagers qui ont répondu à l'enquête, mais il sera appliqué à tous. S'ils sont différents, la précision réelle sera différente.
- La catégorie « neutre ou insatisfait » regroupe des passagers neutres et des passagers vraiment déçus : tous ne justifient pas une approche.
- Les chiffres économiques (40 €, 1 sur 3, la moitié) sont ceux de la directrice. S'ils changent, le classement des stratégies reste le même, mais les montants changent.
- Le gain d'un modèle sur la règle simple est réel mais modeste. Si la compagnie veut commencer vite et simplement, la règle « voyageurs personnels » est déjà très rentable.
