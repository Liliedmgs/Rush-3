"""La mesure de performance : précision sur les passagers qu'on peut approcher."""
import numpy as np

# On ne peut approcher que 10 % des passagers
CAPACITE = 0.10


def precision_top(y_vrai, scores, capacite=CAPACITE):
	"""Part de vrais insatisfaits parmi les `capacite` % de passagers les mieux classés.

	kind="stable" : à score égal, l'ordre est toujours le même, donc le chiffre aussi.
	"""
	n = int(len(scores) * capacite)
	meilleurs = np.argsort(-np.asarray(scores), kind="stable")[:n]
	return float(np.asarray(y_vrai)[meilleurs].mean())
