"""Chargement et nettoyage, identiques pour train et test."""
import numpy as np
import pandas as pd

from rush3.core.config import DATA_RAW
from rush3.core.schema import CIBLE, RATING_COLS


def nettoyer(df):
	"""Applique les règles de nettoyage décidées sur train.csv."""
	df = df.copy()

	# 1. Colonnes inutiles : ce sont des numéros de ligne
	df = df.drop(columns=["Unnamed: 0", "id"])

	# 2. Cible en 1/0 : 1 = insatisfait, 0 = satisfait
	df[CIBLE] = (df["satisfaction"] == "neutral or dissatisfied").astype(int)
	df = df.drop(columns=["satisfaction"])

	# 3. Un 0 dans une note veut dire "pas de réponse", pas "très mauvais"
	df[RATING_COLS] = df[RATING_COLS].replace(0, np.nan)

	# 4. Retard à l'arrivée manquant : on prend le retard au départ
	df["Arrival Delay in Minutes"] = df["Arrival Delay in Minutes"].fillna(
		df["Departure Delay in Minutes"]
	)

	return df


def load_train_brut():
	"""train.csv tel quel, pour montrer l'avant/après nettoyage."""
	return pd.read_csv(DATA_RAW / "train.csv")


def load_train():
	"""Charge et nettoie les données d'entraînement."""
	return nettoyer(load_train_brut())


def load_test():
	"""À N'APPELER QUE DANS rush3.prediction.evaluation_finale (vérifié par les tests)."""
	return nettoyer(pd.read_csv(DATA_RAW / "test.csv"))
