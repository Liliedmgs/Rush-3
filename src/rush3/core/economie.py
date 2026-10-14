"""Le calcul économique de la directrice (PLAN.md, section 3), partagé par les trois."""

COUT_APPROCHE = 40          # € dépensés à chaque passager approché
PERTE_CLIENT = 600          # € perdus quand un insatisfait ne revient pas
PART_QUI_PART = 1 / 3       # 1 insatisfait sur 3 ne revient pas
PART_RECUPEREE = 1 / 2      # l'approche en récupère la moitié

# Gain espéré quand on approche un vrai insatisfait : 600 × 1/3 × 1/2 = 100 €
GAIN_VRAI_INSATISFAIT = PERTE_CLIENT * PART_QUI_PART * PART_RECUPEREE


def benefice_par_approche(precision):
	"""Bénéfice moyen d'une approche, selon la part de vrais insatisfaits approchés."""
	return GAIN_VRAI_INSATISFAIT * precision - COUT_APPROCHE


def benefice_pour_1000(precision, capacite=0.10):
	"""Bénéfice en euros quand on approche capacite × 1 000 passagers sur 1 000."""
	return 1000 * capacite * benefice_par_approche(precision)


def cout_des_erreurs(precision, taux_insatisfaits, capacite=0.10, n=1000):
	"""Ce que donnent les approches sur n passagers : bons choix, fausses alertes, oublis."""
	approches = n * capacite
	fausses_alertes = approches * (1 - precision)
	return {
		"approches": approches,
		"vrais_insatisfaits_approches": approches * precision,
		"fausses_alertes": fausses_alertes,
		"cout_fausses_alertes": fausses_alertes * COUT_APPROCHE,
		"insatisfaits_oublies": n * taux_insatisfaits - approches * precision,
	}
