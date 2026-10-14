"""Chemins et graine aléatoire partagés par tout le projet.

Les dossiers sont ceux du dépôt actuel. Si l'organisation change, seul ce fichier change.
"""
from pathlib import Path

SEED = 42

# Racine du dépôt : src/rush3/core/config.py -> remonter de 3 dossiers
RACINE = Path(__file__).resolve().parents[3]

DATA_RAW = RACINE / "data_raw"
FIGURES = RACINE / "figures"
RESULTS = RACINE / "results"
