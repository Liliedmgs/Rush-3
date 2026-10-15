"""Fonctions partagées par tous les notebooks : chargement et nettoyage.

Les définitions sont dans le paquet rush3 (src/rush3/core/), installé par
`pip install -r requirements.txt`. Ce fichier les réexporte pour que les
notebooks existants (`from src.common import ...`) continuent de marcher.
"""
from rush3.core.config import RACINE, SEED
from rush3.core.donnees import load_test, load_train, nettoyer
from rush3.core.economie import benefice_pour_1000
from rush3.core.schema import LANDING_COLS, RATING_COLS
from rush3.prediction.metriques import precision_top as precision_top10
