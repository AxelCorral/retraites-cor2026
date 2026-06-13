"""
test_companion.py — Coherence compagnon IP2108 / Figure 4 + calage 2040.

1. Le scenario central du compagnon reproduit EXACTEMENT la Figure 4 pour 2026
   et 2070 (population totale, ratio de dependance, ages individuels 0..104).
2. Le ratio de dependance 65+/20-64 vaut 40 (2026), 49 (2040), 62 (2070)
   sur le compagnon central (annees intermediaires desormais disponibles).

Rappel terminal : le compagnon groupe en "105+" (normalise -> 106) tandis que
la Figure 4 groupe en "106 ou plus" (normalise -> 106). Les tranches 20-64 et
65-104 sont identiques dans les deux sources : les totaux et ratios doivent
etre exactement egaux.
"""

import sys
from pathlib import Path
import pytest

RACINE = Path(__file__).parent.parent
sys.path.insert(0, str(RACINE / "src"))

from maquette import charger_hypotheses, ratio_dependance_demo  # noqa: E402
from data_insee import charger_pyramide_age_fin, charger_pyramide_scenario  # noqa: E402

HYP = charger_hypotheses(RACINE / "config" / "hypotheses.yaml")
TOL = HYP["calage"]["tolerance"]

PYRAMIDE_F4  = RACINE / HYP["donnees"]["ip2108_xlsx"]
CENTRAL_PATH = RACINE / HYP["donnees"]["ip2108_central"]

_DEUX_FICHIERS = pytest.mark.skipif(
    not CENTRAL_PATH.exists() or not PYRAMIDE_F4.exists(),
    reason="Fichier compagnon ou Figure 4 absent",
)
_CENTRAL_SEUL = pytest.mark.skipif(
    not CENTRAL_PATH.exists(),
    reason=f"Fichier absent : {CENTRAL_PATH}",
)


# --- Coherence compagnon vs Figure 4 ----------------------------------------

@_DEUX_FICHIERS
@pytest.mark.parametrize("annee", [2026, 2070])
def test_companion_coherence_figure4(annee):
    """Pop totale et ratio de dependance identiques entre compagnon et Figure 4."""
    pop_f4 = charger_pyramide_age_fin(PYRAMIDE_F4)
    pop_c  = charger_pyramide_scenario(CENTRAL_PATH, "central")

    # Population totale : exactement egale
    # (groupage terminal different : "105+" vs "106 ou plus", mais meme population)
    total_f4 = pop_f4[annee].sum()
    total_c  = pop_c[annee].sum()
    assert total_f4 == pytest.approx(total_c, rel=1e-5), (
        f"Pop totale {annee} : Figure4={total_f4:,.0f}  Compagnon={total_c:,.0f}"
    )

    # Ratio de dependance : identique (tranches 20-64 et 65-104 non affectees)
    rd_f4 = ratio_dependance_demo(pop_f4, annee)
    rd_c  = ratio_dependance_demo(pop_c, annee)
    assert abs(rd_f4 - rd_c) < 0.05, (
        f"Ratio demo {annee} : Figure4={rd_f4:.3f}  Compagnon={rd_c:.3f}"
    )


@_DEUX_FICHIERS
@pytest.mark.parametrize("annee", [2026, 2070])
def test_companion_ages_individuels(annee):
    """Ages 0..104 : valeurs identiques entre compagnon et Figure 4."""
    pop_f4 = charger_pyramide_age_fin(PYRAMIDE_F4)
    pop_c  = charger_pyramide_scenario(CENTRAL_PATH, "central")

    for age in [0, 5, 20, 40, 65, 80, 100]:
        assert pop_c.loc[age, annee] == pytest.approx(pop_f4.loc[age, annee], rel=1e-4), (
            f"Pop age {age}, {annee} : Figure4={pop_f4.loc[age, annee]:,.0f}"
            f"  Compagnon={pop_c.loc[age, annee]:,.0f}"
        )


# --- Calage demographique sur compagnon (annees intermediaires) --------------

@_CENTRAL_SEUL
@pytest.mark.parametrize("annee,attendu", [(2026, 40), (2040, 49), (2070, 62)])
def test_ratio_dependance_compagnon(annee, attendu):
    """Ratio 65+/20-64 sur compagnon central = 40/49/62 (IP2108, scenario central)."""
    pop_c  = charger_pyramide_scenario(CENTRAL_PATH, "central")
    obtenu = ratio_dependance_demo(pop_c, annee)
    assert abs(obtenu - attendu) <= TOL, (
        f"{annee} : ratio={obtenu:.2f}, attendu~{attendu} (tol={TOL})"
    )
