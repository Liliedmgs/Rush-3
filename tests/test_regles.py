"""Les règles du projet (PLAN.md, section 2), vérifiées automatiquement."""
import ast
from pathlib import Path

from rush3.core.schema import LANDING_COLS, RATING_COLS

RACINE = Path(__file__).resolve().parents[1]
SRC = RACINE / "src" / "rush3"


def test_core_n_importe_que_core():
	for fichier in (SRC / "core").rglob("*.py"):
		for noeud in ast.walk(ast.parse(fichier.read_text(encoding="utf-8"))):
			if isinstance(noeud, ast.ImportFrom) and noeud.module and noeud.module.startswith("rush3."):
				assert noeud.module.startswith("rush3.core"), f"{fichier.name} importe {noeud.module}"


def test_seule_evaluation_finale_lit_test_csv():
	"""Règle 1 : test.csv n'est lu que par le test final."""
	autorises = {SRC / "core" / "donnees.py", SRC / "prediction" / "evaluation_finale.py"}
	for fichier in SRC.rglob("*.py"):
		if fichier not in autorises:
			texte = fichier.read_text(encoding="utf-8")
			assert "load_test" not in texte and "test.csv" not in texte, fichier
	for nb in (RACINE / "notebooks").glob("*.ipynb"):
		if nb.name != "04_evaluation_finale.ipynb":
			texte = nb.read_text(encoding="utf-8")
			assert "load_test" not in texte and "evaluer_sur_test" not in texte, nb.name


def test_prediction_sans_notes_du_questionnaire():
	"""Règle 2 : le modèle n'utilise que ce qu'on sait à l'atterrissage."""
	assert not set(LANDING_COLS) & set(RATING_COLS)
	assert "Gender" not in LANDING_COLS
	for fichier in (SRC / "prediction").rglob("*.py"):
		assert "RATING_COLS" not in fichier.read_text(encoding="utf-8"), fichier
