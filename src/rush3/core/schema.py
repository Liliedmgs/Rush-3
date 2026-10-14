"""Noms des colonnes : qui a le droit d'utiliser quoi."""

CIBLE = "insatisfait"

# Les 14 notes du questionnaire, remplies APRÈS le vol.
# Autorisées pour expliquer la satisfaction, interdites dans le modèle de prédiction.
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

# Ce que la compagnie connaît à l'atterrissage : dossier de réservation et vol.
# Pas de note du questionnaire, pas de genre (il n'améliore pas le modèle, cf. notebook 03).
LANDING_COLS = [
	"Customer Type",
	"Age",
	"Type of Travel",
	"Class",
	"Flight Distance",
	"Departure Delay in Minutes",
	"Arrival Delay in Minutes",
]

LANDING_CATEGORIELLES = ["Customer Type", "Type of Travel", "Class"]
LANDING_NUMERIQUES = [c for c in LANDING_COLS if c not in LANDING_CATEGORIELLES]
