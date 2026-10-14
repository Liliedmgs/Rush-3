import json

import numpy as np
import pandas as pd
import pytest

from rush3.core import contrats
from rush3.core.donnees import nettoyer
from rush3.core.schema import RATING_COLS


def _brut():
	ligne = {"Unnamed: 0": 0, "id": 1, "satisfaction": "neutral or dissatisfied",
		"Departure Delay in Minutes": 12, "Arrival Delay in Minutes": np.nan}
	ligne.update({note: 3 for note in RATING_COLS})
	ligne["Inflight wifi service"] = 0
	return pd.DataFrame([ligne, {**ligne, "satisfaction": "satisfied", "Arrival Delay in Minutes": 5}])


def test_nettoyer():
	df = nettoyer(_brut())
	assert "id" not in df and "Unnamed: 0" not in df and "satisfaction" not in df
	assert df["insatisfait"].tolist() == [1, 0]
	assert df["Inflight wifi service"].isna().all()
	assert df["Arrival Delay in Minutes"].tolist() == [12, 5]


def test_contrat_incomplet_refuse(tmp_path, monkeypatch):
	monkeypatch.setattr(contrats, "RESULTS", tmp_path)
	with pytest.raises(ValueError):
		contrats.ecrire_contrat("03_variables_sensibles", {"modele": "x"})
	with pytest.raises(KeyError):
		contrats.ecrire_contrat("inconnu", {})


def test_contrat_aller_retour(tmp_path, monkeypatch):
	monkeypatch.setattr(contrats, "RESULTS", tmp_path)
	donnees = {"modele": "x", "essais": [{"nom": "a", "precision_moyenne": 0.9}]}
	contrats.ecrire_contrat("03_variables_sensibles", donnees)
	assert json.loads((tmp_path / "03_variables_sensibles.json").read_text()) == donnees
	assert contrats.lire_contrat("03_variables_sensibles") == donnees
