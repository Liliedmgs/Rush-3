"""Contrats JSON échangés entre les parties, dans results/.

Une partie n'importe pas le code d'une autre : elle lit le JSON que l'autre a écrit.
Chaque contrat liste ses clés obligatoires ; écrire ou lire un contrat incomplet échoue.
"""
import json

from rush3.core.config import RESULTS

CONTRATS = {
	# Écrit par prediction (notebook 03), lu par le rapport
	"03_comparaison_modeles": {
		"capacite", "variables", "strategies", "modele_choisi", "deploiement",
	},
	# Écrit par prediction (notebook 03), lu pour la partie protection des données
	"03_variables_sensibles": {
		"modele", "essais",
	},
	# Écrit par prediction (notebook 04, une seule fois), lu par le rapport
	"04_evaluation_finale": {
		"date_execution", "modele", "variables", "n_passagers", "capacite",
		"precision_modele", "precision_regle_simple", "taux_insatisfaits",
	},
}


def _verifier(nom, donnees):
	if nom not in CONTRATS:
		raise KeyError(f"Contrat inconnu : {nom}")
	manquantes = CONTRATS[nom] - set(donnees)
	if manquantes:
		raise ValueError(f"Contrat {nom} incomplet, clés manquantes : {sorted(manquantes)}")


def chemin(nom):
	return RESULTS / f"{nom}.json"


def ecrire_contrat(nom, donnees):
	_verifier(nom, donnees)
	RESULTS.mkdir(parents=True, exist_ok=True)
	with open(chemin(nom), "w", encoding="utf-8") as f:
		json.dump(donnees, f, indent=2, ensure_ascii=False)
		f.write("\n")


def lire_contrat(nom):
	with open(chemin(nom), encoding="utf-8") as f:
		donnees = json.load(f)
	_verifier(nom, donnees)
	return donnees
