"""Fonctions partagées par tous les notebooks : chargement et nettoyage."""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42

# Dossier racine du dépôt (le parent de src/)
RACINE = Path(__file__).resolve().parent.parent

RATING_COLS = [
	"Inflight wifi service",
	"Departure/Arrival time convenient",
	"Ease of Online booking",
	"Gate location",
	"Food and drink",
	"Online boarding",
	"Seat comfort",
	"Inflight entertainment",
	"On-board service",
	"Leg room service",
	"Baggage handling",
	"Checkin service",
	"Inflight service",
	"Cleanliness",
]


def nettoyer(df):
	"""Applique les règles de nettoyage décidées sur train.csv."""
	df = df.copy()

	# 1. Colonnes inutiles : ce sont des numéros de ligne
	df = df.drop(columns=["Unnamed: 0", "id"])

	# 2. Cible en 1/0 : 1 = insatisfait, 0 = satisfait
	df["insatisfait"] = (df["satisfaction"] == "neutral or dissatisfied").astype(int)
	df = df.drop(columns=["satisfaction"])

	# 3. Un 0 dans une note veut dire "pas de réponse", pas "très mauvais"
	df[RATING_COLS] = df[RATING_COLS].replace(0, np.nan)

	# 4. Retard à l'arrivée manquant : on prend le retard au départ
	df["Arrival Delay in Minutes"] = df["Arrival Delay in Minutes"].fillna(
		df["Departure Delay in Minutes"]
	)

	return df


def load_train():
	"""Charge et nettoie les données d'entraînement."""
	return nettoyer(pd.read_csv(RACINE / "data_raw" / "train.csv"))


def load_test():
	"""A N'APPELER QUE DANS notebooks/04_evaluation_finale.ipynb."""
	return nettoyer(pd.read_csv(RACINE / "data_raw" / "test.csv"))
