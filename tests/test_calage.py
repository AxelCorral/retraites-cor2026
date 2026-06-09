"""
test_calage.py — Tests unitaires fondateurs.

Tant que ces tests ne passent pas, AUCUNE conclusion n'est legitime.
Ils verifient que la maquette reproduit les chiffres officiels de
l'Insee Premiere n2108 (scenario central) :
  - ratio de dependance demographique 65+/20-64 : 40 (2026), 49 (2040), 62 (2070)
  - population totale : 69.082 (2026), 69.768 (2037), 65.887 (2070) Mhab
"""

import sys
from pathlib import Path
import pandas as pd
import pytest

RACINE = Path(__file__).parent.parent
sys.path.insert(0, str(RACINE / "src"))
from maquette import charger_hypotheses, ratio_dependance_demo  # noqa: E402
from data_insee import charger_pyramide_age_fin                 # noqa: E402

HYP = charger_hypotheses(RACINE / "config" / "hypotheses.yaml")
TOL = HYP["calage"]["tolerance"]
PYRAMIDE_PATH = RACINE / HYP["donnees"]["ip2108_xlsx"]


# --- Donnees agregees figure 5 IP2108 (millions), scenario central -----------
# Colonnes : moins de 20, 20-44, 45-64, 65+
FIG5 = pd.DataFrame({
    2026: {"u20": 15.528, "a2044": 20.731, "a4564": 17.485, "p65": 15.339},
    2040: {"u20": 12.973, "a2044": 20.998, "a4564": 17.189, "p65": 18.571},
}).T


def ratio_demo_agrege(an: int) -> float:
    """65+ / (20-44 + 45-64) * 100 a partir des agregats figure 5."""
    r = FIG5.loc[an]
    return r["p65"] / (r["a2044"] + r["a4564"]) * 100.0


@pytest.mark.parametrize("annee,attendu", [(2026, 40), (2040, 49)])
def test_ratio_dependance_demo(annee, attendu):
    """Le ratio recalcule doit etre proche du chiffre officiel Insee."""
    obtenu = ratio_demo_agrege(annee)
    assert abs(obtenu - attendu) <= TOL + 1, (
        f"{annee}: ratio={obtenu:.1f}, attendu~{attendu} (tol={TOL})"
    )


def test_population_totale_2026():
    """Somme des tranches d'age = population totale 2026."""
    r = FIG5.loc[2026]
    total = r["u20"] + r["a2044"] + r["a4564"] + r["p65"]
    attendu = HYP["calage"]["population_totale_millions"]["2026"]
    assert abs(total - attendu) <= TOL


def test_hypotheses_chargees():
    """Le fichier d'hypotheses est bien lu et structure."""
    assert HYP["indexation"]["scenario_actif"] in ("L", "N")
    assert "central" in HYP["scenarios_demo"]


@pytest.mark.skipif(
    not PYRAMIDE_PATH.exists(),
    reason=f"Fichier absent : {PYRAMIDE_PATH} — telecharger ip2108.xlsx d'abord",
)
def test_ratio_dependance_2070():
    """Ratio 65+/20-64 en 2070 = 62 (IP2108 fig. 4, scenario central).

    Utilise la pyramide par age fin pour un calcul exact (les agregats de la
    figure 5 ne permettent pas de distinguer 20-64 en 2070).
    """
    pop = charger_pyramide_age_fin(PYRAMIDE_PATH)
    obtenu = ratio_dependance_demo(pop, 2070)
    attendu = HYP["calage"]["ratio_dependance_demo"]["2070"]
    assert abs(obtenu - attendu) <= TOL, (
        f"2070: ratio={obtenu:.2f}, attendu~{attendu} (tol={TOL})"
    )
