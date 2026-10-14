"""Le contrôle final sur test.csv : le SEUL code du dépôt qui lit test.csv.

À lancer une seule fois, quand le modèle est choisi et que plus rien ne changera.
Si les chiffres sont moins bons qu'en validation croisée, on ne touche à rien.
"""
from datetime import datetime

from rush3.core.contrats import ecrire_contrat
from rush3.core.donnees import load_test, load_train
from rush3.core.schema import CIBLE, LANDING_COLS
from rush3.prediction.metriques import CAPACITE, precision_top
from rush3.prediction.modeles import MODELE_CHOISI, construire, regle_simple


def evaluer_sur_test():
	train = load_train()
	test = load_test()

	modele = construire(MODELE_CHOISI)
	modele.fit(train[LANDING_COLS], train[CIBLE])
	scores = modele.predict_proba(test[LANDING_COLS])[:, 1]

	resultat = {
		"date_execution": datetime.now().isoformat(timespec="minutes"),
		"modele": MODELE_CHOISI,
		"variables": LANDING_COLS,
		"n_passagers": len(test),
		"capacite": CAPACITE,
		"precision_modele": round(precision_top(test[CIBLE], scores), 4),
		"precision_regle_simple": round(precision_top(test[CIBLE], regle_simple(test)), 4),
		"taux_insatisfaits": round(float(test[CIBLE].mean()), 4),
	}
	ecrire_contrat("04_evaluation_finale", resultat)
	return resultat
