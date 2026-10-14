"""Comparer les stratégies sur train.csv seulement, par validation croisée à 5 blocs."""
import numpy as np
from sklearn.model_selection import StratifiedKFold

from rush3.core.config import SEED
from rush3.core.schema import CIBLE, LANDING_CATEGORIELLES, LANDING_NUMERIQUES
from rush3.prediction.metriques import precision_top
from rush3.prediction.modeles import MODELES, construire, regle_simple

N_BLOCS = 5


def _blocs(df):
	cv = StratifiedKFold(n_splits=N_BLOCS, shuffle=True, random_state=SEED)
	return cv.split(df, df[CIBLE])


def evaluer_modele(df, nom, numeriques=LANDING_NUMERIQUES, categorielles=LANDING_CATEGORIELLES):
	"""Précision sur le top 10 % de chaque bloc de validation, pour un modèle du catalogue."""
	colonnes = list(numeriques) + list(categorielles)
	resultats = []
	for i_app, i_val in _blocs(df):
		modele = construire(nom, numeriques, categorielles)
		modele.fit(df[colonnes].iloc[i_app], df[CIBLE].iloc[i_app])
		scores = modele.predict_proba(df[colonnes].iloc[i_val])[:, 1]
		resultats.append(precision_top(df[CIBLE].iloc[i_val], scores))
	return np.array(resultats)


def evaluer_regle(df, regle):
	"""Même découpage, pour une stratégie sans apprentissage (hasard, règle simple)."""
	return np.array([
		precision_top(df[CIBLE].iloc[i_val], regle(df.iloc[i_val]))
		for _, i_val in _blocs(df)
	])


def evaluer_hasard(df):
	"""Approcher au hasard : la précision attendue est le taux d'insatisfaits du bloc."""
	return np.array([df[CIBLE].iloc[i_val].mean() for _, i_val in _blocs(df)])


def comparer(df):
	"""Toutes les stratégies, du plus simple au plus complexe."""
	strategies = {
		"Hasard": evaluer_hasard(df),
		"Règle simple (voyage personnel)": evaluer_regle(df, regle_simple),
	}
	for nom in MODELES:
		strategies[nom] = evaluer_modele(df, nom)
	return [
		{
			"nom": nom,
			"precision_moyenne": round(float(r.mean()), 4),
			"ecart_type": round(float(r.std()), 4),
			"precisions_par_bloc": [round(float(x), 4) for x in r],
		}
		for nom, r in strategies.items()
	]


def essais_variables_sensibles(df, nom):
	"""Ce que coûte le retrait de l'âge, ce qu'apporte l'ajout du genre."""
	sans_age = [c for c in LANDING_NUMERIQUES if c != "Age"]
	essais = {
		"modèle de base": (LANDING_NUMERIQUES, LANDING_CATEGORIELLES),
		"sans l'âge": (sans_age, LANDING_CATEGORIELLES),
		"avec le genre": (LANDING_NUMERIQUES, LANDING_CATEGORIELLES + ["Gender"]),
	}
	return [
		{"nom": essai, "precision_moyenne": round(float(evaluer_modele(df, nom, num, cat).mean()), 4)}
		for essai, (num, cat) in essais.items()
	]
