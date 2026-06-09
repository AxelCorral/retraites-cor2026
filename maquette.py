"""
maquette.py — Maquette comptable agregee de soutenabilite du systeme
              de retraite par repartition francais.

ATTENTION : ceci est une MAQUETTE COMPTABLE AGREGEE, pas un modele de
projection des retraites au sens du COR (qui repose sur des microsimulations
sur cas-types). Sa vocation est la TRANSPARENCE et la REPRODUCTIBILITE :
refaire un calcul d'equilibre explicite, sur les projections Insee 2026.

Equation fondamentale du systeme par repartition pur :

    tau*(t) * Wbar(t) * A(t)  =  Pbar(t) * R(t)

d'ou le taux de cotisation d'equilibre :

    tau*(t) = [R(t) / A(t)] * [Pbar(t) / Wbar(t)]
            = (ratio de dependance economique) * (pension moyenne relative)

Distinction fondamentale rappelee partout : une PROJECTION conditionnelle
("si les tendances se prolongeaient") n'est PAS une PREDICTION.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml
import pandas as pd


# -----------------------------------------------------------------------------
#  Chargement des hypotheses
# -----------------------------------------------------------------------------
def charger_hypotheses(chemin: str | Path) -> dict:
    """Charge le fichier d'hypotheses centralise. Source unique de verite."""
    with open(chemin, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# -----------------------------------------------------------------------------
#  Brique 1 — ratio de dependance demographique (test de calage)
# -----------------------------------------------------------------------------
def ratio_dependance_demo(pop_par_age: pd.DataFrame, annee: int) -> float:
    """
    65+ / 20-64, pour 100. Sert de TEST UNITAIRE FONDATEUR :
    doit reproduire 40 (2026), 49 (2040), 62 (2070) du scenario central.

    pop_par_age : DataFrame indexe par age (0..106+), colonne = population
                  totale a l'annee donnee (hommes + femmes), en personnes.
    """
    pop = pop_par_age[annee] if annee in pop_par_age.columns else pop_par_age
    p_20_64 = pop.loc[20:64].sum()
    p_65p = pop.loc[65:].sum()
    return p_65p / p_20_64 * 100.0


# -----------------------------------------------------------------------------
#  Brique 2 — passage demographique -> economique
# -----------------------------------------------------------------------------
def cotisants(pop_par_age: pd.Series, taux_emploi_par_age: pd.Series) -> float:
    """A(t) : nombre de cotisants = somme(pop_age * taux_emploi_age)."""
    ages = pop_par_age.index.intersection(taux_emploi_par_age.index)
    return float((pop_par_age.loc[ages] * taux_emploi_par_age.loc[ages]).sum())


def retraites(pop_par_age: pd.Series, taux_retraite_par_age: pd.Series) -> float:
    """R(t) : nombre de retraites = somme(pop_age * taux_retraite_age)."""
    ages = pop_par_age.index.intersection(taux_retraite_par_age.index)
    return float((pop_par_age.loc[ages] * taux_retraite_par_age.loc[ages]).sum())


# -----------------------------------------------------------------------------
#  Brique 3 — pension moyenne relative selon le regime d'indexation
# -----------------------------------------------------------------------------
def pension_relative(annee: int, annee_base: int, ratio_base: float,
                     regime: str, productivite: float) -> float:
    """
    Pbar(t)/Wbar(t).

    Scenario N (parite) : constant = ratio_base (contrefactuel, choix politique).
    Scenario L (legislation constante) : pensions indexees sur les prix,
        salaires croissant a la productivite g => le ratio derive a la baisse.
        Approximation stylisee : ratio(t) = ratio_base * (1+g)^-(t - base).
        (v0 simplifiee ; a raffiner avec effet noria : renouvellement du stock
         de pensions par des liquidations a niveau plus eleve.)
    """
    if regime == "N":
        return ratio_base
    elif regime == "L":
        return ratio_base * (1.0 + productivite) ** (-(annee - annee_base))
    raise ValueError(f"Regime d'indexation inconnu : {regime!r}")


# -----------------------------------------------------------------------------
#  Brique 4 — taux de cotisation d'equilibre
# -----------------------------------------------------------------------------
def tau_equilibre(R: float, A: float, ratio_pension_salaire: float) -> float:
    """tau*(t) = (R/A) * (Pbar/Wbar)."""
    if A <= 0:
        raise ValueError("Nombre de cotisants nul ou negatif.")
    return (R / A) * ratio_pension_salaire


# -----------------------------------------------------------------------------
#  Orchestration v0 (scenario central, parite) — squelette
# -----------------------------------------------------------------------------
@dataclass
class ResultatAnnee:
    annee: int
    ratio_demo: float
    ratio_eco: float
    pension_relative: float
    tau_etoile: float


def trajectoire(hyp: dict, pop_par_age: pd.DataFrame,
                taux_emploi: pd.Series, taux_retraite: pd.Series,
                annees: range) -> pd.DataFrame:
    """
    Calcule la trajectoire de tau*(t). v0 = scenario central.
    pop_par_age : DataFrame [age x annee], population totale.
    """
    base = 2026
    ratio_base = hyp["pensions"]["ratio_pension_salaire_2026"]
    regime = hyp["indexation"]["scenario_actif"]
    g = hyp["economie"]["croissance_productivite_reference"]

    lignes = []
    for an in annees:
        pop = pop_par_age[an]
        A = cotisants(pop, taux_emploi)
        R = retraites(pop, taux_retraite)
        pr = pension_relative(an, base, ratio_base, regime, g)
        lignes.append(ResultatAnnee(
            annee=an,
            ratio_demo=ratio_dependance_demo(pop_par_age, an),
            ratio_eco=R / A,
            pension_relative=pr,
            tau_etoile=tau_equilibre(R, A, pr),
        ))
    return pd.DataFrame([l.__dict__ for l in lignes]).set_index("annee")


if __name__ == "__main__":
    hyp = charger_hypotheses(Path(__file__).parent.parent / "config" / "hypotheses.yaml")
    print("Hypotheses chargees. Perimetre :", hyp["meta"]["perimetre"])
    print("Regime d'indexation actif :", hyp["indexation"]["scenario_actif"])
    print("\n>>> Prochaine etape : charger data/raw/ip2108_pop_age.* et")
    print(">>> faire passer tests/test_calage.py (40/49/62) avant tout.")
