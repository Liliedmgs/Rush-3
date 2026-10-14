"""Comparer les stratégies sur train.csv seulement, par validation croisée à 5 blocs."""
import numpy as np
from sklearn.model_selection import StratifiedKFold

from rush3.core.config import SEED
from rush3.core.schema import CIBLE, LANDING_CATEGORIELLES, LANDING_NUMERIQUES
from rush3.prediction.metriques import precision_top
from rush3.prediction.modeles import (
	DEPLOIEMENT_CATEGORIELLES,
	DEPLOIEMENT_NUMERIQUES,
	MODELE_CHOISI,
	MODELES,
	construire,
	exclure_mineurs,
	regle_simple,
)

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


def evaluer_deploiement(df):
	"""Version testée (7 informations), version déployée (sans l'âge) et règle simple,
	avec et sans la règle « aucun mineur signalé »."""
	versions = {
		"Arbre testé (7 informations)": (LANDING_NUMERIQUES, LANDING_CATEGORIELLES),
		"Arbre déployé (sans l'âge)": (DEPLOIEMENT_NUMERIQUES, DEPLOIEMENT_CATEGORIELLES),
		"Règle simple (voyage personnel)": None,
	}
	resultats = []
	for version, variables in versions.items():
		tous, sans_mineurs = [], []
		for i_app, i_val in _blocs(df):
			val = df.iloc[i_val]
			if variables is None:
				scores = regle_simple(val).astype(float)
			else:
				num, cat = variables
				colonnes = list(num) + list(cat)
				modele = construire(MODELE_CHOISI, num, cat)
				modele.fit(df[colonnes].iloc[i_app], df[CIBLE].iloc[i_app])
				scores = modele.predict_proba(val[colonnes])[:, 1]
			tous.append(precision_top(val[CIBLE], scores))
			sans_mineurs.append(precision_top(val[CIBLE], exclure_mineurs(val, scores)))
		resultats.append({
			"nom": version,
			"precision_moyenne": round(float(np.mean(tous)), 4),
			"precision_sans_mineurs": round(float(np.mean(sans_mineurs)), 4),
		})
	return resultats
