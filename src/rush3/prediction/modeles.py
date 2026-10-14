"""Les stratégies comparées : sans modèle, puis trois modèles."""
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from rush3.core.config import SEED
from rush3.core.schema import LANDING_CATEGORIELLES, LANDING_NUMERIQUES

# Modèle déployé, utilisé par le test final. À trancher par l'équipe (voir notebook 03) :
# l'arbre se lit en une page, le gradient boosting rapporte un peu plus mais ne s'explique pas.
MODELE_CHOISI = "Arbre de décision (4 niveaux)"


def regle_simple(df):
	"""Score sans modèle : 1 pour un voyage personnel, 0 sinon."""
	return (df["Type of Travel"] == "Personal Travel").astype(int).to_numpy()


def _preparation(numeriques, categorielles, standardiser):
	"""Encodage des catégories (et mise à l'échelle) appris dans le Pipeline,
	donc seulement sur les données d'apprentissage de chaque bloc."""
	return ColumnTransformer(
		[
			("num", StandardScaler() if standardiser else "passthrough", numeriques),
			("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categorielles),
		],
		verbose_feature_names_out=False,
	)


def construire(nom, numeriques=LANDING_NUMERIQUES, categorielles=LANDING_CATEGORIELLES):
	"""Pipeline complet (préparation + modèle) pour un des modèles du catalogue."""
	estimateurs = {
		"Régression logistique": (LogisticRegression(max_iter=1000), True),
		"Arbre de décision (4 niveaux)": (DecisionTreeClassifier(max_depth=4, random_state=SEED), False),
		"Gradient boosting": (HistGradientBoostingClassifier(random_state=SEED), False),
	}
	estimateur, standardiser = estimateurs[nom]
	return Pipeline([
		("preparation", _preparation(list(numeriques), list(categorielles), standardiser)),
		("modele", estimateur),
	])


MODELES = ["Régression logistique", "Arbre de décision (4 niveaux)", "Gradient boosting"]
