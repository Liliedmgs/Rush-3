import numpy as np
import pandas as pd

from rush3.core.economie import benefice_pour_1000
from rush3.core.schema import LANDING_COLS
from rush3.prediction.metriques import precision_top
from rush3.prediction.modeles import MODELES, construire, regle_simple


def test_precision_top():
	y = np.array([1, 0, 1, 0, 0, 0, 0, 0, 0, 1] * 10)
	scores = np.arange(100)[::-1]          # les 10 premiers sont les mieux classés
	assert precision_top(y, scores) == y[:10].mean()


def test_precision_top_stable_a_egalite():
	y = np.array([1] * 10 + [0] * 90)
	assert precision_top(y, np.zeros(100)) == 1.0


def test_benefice_pour_1000():
	assert benefice_pour_1000(1.0) == 6000
	assert round(benefice_pour_1000(0.4)) == 0


def _passagers(n=60):
	rng = np.random.default_rng(0)
	return pd.DataFrame({
		"Customer Type": rng.choice(["Loyal Customer", "disloyal Customer"], n),
		"Age": rng.integers(7, 80, n),
		"Type of Travel": rng.choice(["Business travel", "Personal Travel"], n),
		"Class": rng.choice(["Business", "Eco", "Eco Plus"], n),
		"Flight Distance": rng.integers(100, 4000, n),
		"Departure Delay in Minutes": rng.integers(0, 100, n),
		"Arrival Delay in Minutes": rng.integers(0, 100, n).astype(float),
		"insatisfait": rng.integers(0, 2, n),
	})


def test_modeles_tolerent_une_categorie_inconnue():
	df = _passagers()
	nouveau = df.head(3).copy()
	nouveau["Class"] = "Première"
	for nom in MODELES:
		modele = construire(nom).fit(df[LANDING_COLS], df["insatisfait"])
		assert modele.predict_proba(nouveau[LANDING_COLS]).shape == (3, 2)


def test_regle_simple():
	df = _passagers()
	assert (regle_simple(df) == (df["Type of Travel"] == "Personal Travel")).all()
