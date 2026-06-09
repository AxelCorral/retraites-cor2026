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
#  Brique 1bis — profils par age (discretisation bandes -> vecteur unitaire)
# -----------------------------------------------------------------------------
def profil_par_age(bandes: list[dict], taux_par_bande: dict) -> pd.Series:
    """
    Diffuse les taux par bande vers un vecteur par age unitaire (index 0..106).
    Ages non couverts par une bande : 0.
    """
    profil = pd.Series(0.0, index=range(107))
    for bande in bandes:
        t = taux_par_bande[bande["nom"]]
        for age in range(bande["min"], bande["max"] + 1):
            profil[age] = t
    return profil


def profils_annee(hyp: dict, annee: int) -> tuple[pd.Series, pd.Series]:
    """
    Retourne (alpha_a, rho_a) : taux d'activite et de retraite par age pour l'annee.

    Rampe lineaire entre profils 2026 et profils cibles (reforme 2023) :
        w(t) = clip((t - 2026) / (2030 - 2026), 0, 1)
    w=0 en 2026 (profil initial), w=1 a partir de 2030 (plein effet).

    PLACEHOLDER : valeurs numeriques provisoires, DREES/COR a sourcer.
    """
    m = hyp["modele"]
    bandes = m["bandes"]
    t0 = m["reforme_2023"]["annee_debut"]        # 2026
    t1 = m["reforme_2023"]["annee_plein_effet"]  # 2030
    w = min(1.0, max(0.0, (annee - t0) / (t1 - t0)))

    alpha_bandes = {
        nom: m["taux_activite_2026"][nom] * (1 - w) + m["taux_activite_cible"][nom] * w
        for nom in m["taux_activite_2026"]
    }
    rho_bandes = {
        nom: m["taux_retraite_2026"][nom] * (1 - w) + m["taux_retraite_cible"][nom] * w
        for nom in m["taux_retraite_2026"]
    }

    return profil_par_age(bandes, alpha_bandes), profil_par_age(bandes, rho_bandes)


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


def trajectoire(hyp: dict, pop_par_age: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule tau*(t) pour les annees disponibles en colonnes de pop_par_age.
    Utilise profils_annee() pour les taux d'activite et de retraite par age.

    NOTE : avec la Figure 4 de l'IP2108, seuls 2026 et 2070 sont disponibles.
    AVERTISSEMENT : taux d'activite/retraite PLACEHOLDER — ne pas interpreter.
    """
    base = 2026
    ratio_base = hyp["pensions"]["ratio_pension_salaire_2026"]
    regime = hyp["indexation"]["scenario_actif"]
    g = hyp["economie"]["croissance_productivite_reference"]

    annees_dispo = sorted(c for c in pop_par_age.columns if isinstance(c, (int, float)))

    lignes = []
    for an in annees_dispo:
        an = int(an)
        pop = pop_par_age[an]
        alpha_a, rho_a = profils_annee(hyp, an)
        A = cotisants(pop, alpha_a)
        R = retraites(pop, rho_a)
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
    from data_insee import charger_pyramide_age_fin  # src/ est dans sys.path[0]

    RACINE = Path(__file__).parent.parent
    hyp = charger_hypotheses(RACINE / "config" / "hypotheses.yaml")
    chemin_xlsx = RACINE / hyp["donnees"]["ip2108_xlsx"]

    print("=== TRAJECTOIRE tau*(t) — PLOMBERIE UNIQUEMENT ===")
    print("*** AVERTISSEMENT : taux activite/retraite = PLACEHOLDER    ***")
    print("*** Ces valeurs N'ont AUCUNE valeur scientifique.            ***")
    print("*** Ne pas interpreter avant sourcage DREES/COR.            ***")
    print()

    pop = charger_pyramide_age_fin(chemin_xlsx)
    df = trajectoire(hyp, pop)
    print(df.to_string())
