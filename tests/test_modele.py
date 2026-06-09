"""
test_modele.py — Tests de mecanique du passage demographique -> economique.

Verifie la diffusion des profils par age et la rampe de la reforme 2023.
Aucune assertion de valeur sur tau* : les taux sont PLACEHOLDER, non interpretables.
"""

import sys
from pathlib import Path
import pytest

RACINE = Path(__file__).parent.parent
sys.path.insert(0, str(RACINE / "src"))

from maquette import (  # noqa: E402
    charger_hypotheses, profil_par_age, profils_annee, trajectoire,
)
from data_insee import charger_pyramide_age_fin  # noqa: E402

HYP = charger_hypotheses(RACINE / "config" / "hypotheses.yaml")
PYRAMIDE_PATH = RACINE / HYP["donnees"]["ip2108_xlsx"]


# --- profil_par_age ----------------------------------------------------------

def test_profil_par_age_diffusion():
    """Un age representatif de chaque bande recoit le bon taux ; hors plage = 0."""
    bandes = HYP["modele"]["bandes"]
    taux = HYP["modele"]["taux_activite_2026"]
    profil = profil_par_age(bandes, taux)

    cas = [
        (22, "20-24"), (40, "25-54"), (57, "55-59"), (60, "60-61"),
        (62, "62-63"), (65, "64-66"), (68, "67-69"), (80, "70+"),
    ]
    for age, bande in cas:
        assert profil[age] == pytest.approx(taux[bande]), f"age={age} bande={bande}"
    assert profil[15] == 0.0  # hors plage couverte


# --- profils_annee (rampe) ---------------------------------------------------

def test_profils_annee_w0_en_2026():
    """En 2026 : w=0, profil = profil_2026 exactement."""
    m = HYP["modele"]
    alpha_a, rho_a = profils_annee(HYP, 2026)
    assert alpha_a[65] == pytest.approx(m["taux_activite_2026"]["64-66"])
    assert rho_a[62]   == pytest.approx(m["taux_retraite_2026"]["62-63"])


def test_profils_annee_w1_en_2030_et_apres():
    """En 2030 et au-dela : w=1, profil = profil_cible exactement."""
    m = HYP["modele"]
    for annee in (2030, 2040, 2070):
        alpha_a, rho_a = profils_annee(HYP, annee)
        assert alpha_a[65] == pytest.approx(m["taux_activite_cible"]["64-66"]), f"annee={annee}"
        assert rho_a[62]   == pytest.approx(m["taux_retraite_cible"]["62-63"]), f"annee={annee}"


def test_profils_annee_interpolation_2028():
    """En 2028 (w=0.5) : interpolation lineaire entre profil_2026 et cible."""
    m = HYP["modele"]
    w = 0.5  # (2028 - 2026) / (2030 - 2026)
    attendu_alpha = (m["taux_activite_2026"]["64-66"] * (1 - w)
                     + m["taux_activite_cible"]["64-66"] * w)
    attendu_rho   = (m["taux_retraite_2026"]["62-63"] * (1 - w)
                     + m["taux_retraite_cible"]["62-63"] * w)
    alpha_a, rho_a = profils_annee(HYP, 2028)
    assert alpha_a[65] == pytest.approx(attendu_alpha)
    assert rho_a[62]   == pytest.approx(attendu_rho)


# --- Plomberie (A, R, tau* dans plages plausibles) --------------------------

@pytest.mark.skipif(
    not PYRAMIDE_PATH.exists(),
    reason=f"Fichier absent : {PYRAMIDE_PATH}",
)
def test_trajectoire_plomberie():
    """A>0, R>0, 0<tau*<1 pour chaque annee. Test de plomberie, pas d'interpretation."""
    pop = charger_pyramide_age_fin(PYRAMIDE_PATH)
    df = trajectoire(HYP, pop)

    assert len(df) > 0, "Aucune annee calculee"
    for annee, row in df.iterrows():
        assert row["ratio_eco"] > 0,         f"R/A <= 0 en {annee}"
        assert 0 < row["tau_etoile"] < 1,    f"tau*={row['tau_etoile']:.3f} hors [0,1] en {annee}"
