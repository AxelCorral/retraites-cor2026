"""
figures.py — Pipeline figures et tables de la maquette de soutenabilite.

Usage : python src/figures.py
Sorties horodatees dans figures/ :
  fig1_ciseaux_YYYYMMDD.png   — tau*(N) vs P/W(L), scenario central (figure-these)
  fig2_fan_tauN_YYYYMMDD.png  — faisceau tau*(N), 5 scenarios demographiques

Tables imprimees en console :
  - Seuil-cotisation : annees franchissement tau*(N) >= {35, 40, 45, 50}%
  - Seuil-pension    : annees franchissement P/W(L) <= {50, 45, 40}%
  - Validation COR   : R/A et P/W aux jalons 2026 / 2040 / 2070
"""

from __future__ import annotations
from pathlib import Path
from datetime import date
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # backend non-interactif pour generation PNG
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

RACINE = Path(__file__).parent.parent
sys.path.insert(0, str(RACINE / "src"))

from maquette import charger_hypotheses, trajectoires_scenarios  # noqa: E402
from data_insee import charger_pyramide_scenario               # noqa: E402

HORODATAGE  = date.today().strftime("%Y%m%d")
REP_FIGURES = RACINE / "figures"
REP_FIGURES.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family":       "sans-serif",
    "font.size":         10,
    "axes.titlesize":    10,
    "axes.labelsize":    9,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.dpi":        150,
})


# ---------------------------------------------------------------------------
#  Utilitaires analyse
# ---------------------------------------------------------------------------

def _annee_franchissement(series: pd.Series, seuil: float, sens: str) -> int | None:
    """
    Premiere annee ou series franchit seuil dans le sens indique.
    sens = "hausse" (val >= seuil) | "baisse" (val <= seuil).
    Retourne None si le seuil n'est pas atteint sur la periode.
    """
    for annee, val in series.items():
        if sens == "hausse" and val >= seuil:
            return int(annee)
        if sens == "baisse" and val <= seuil:
            return int(annee)
    return None


def _fmt_annee(a: int | None) -> str:
    return str(a) if a is not None else "> 2070"


def table_seuils_tau(
    traj: dict[str, pd.DataFrame],
    seuils: list[float],
) -> pd.DataFrame:
    """
    Seuil-cotisation : premiere annee tau*(N) >= seuil, par scenario demographique.
    Assiette : salaire brut (convention COR : cotisations retraite / masse salariale brute).
    """
    lignes = []
    for nom, df in traj.items():
        row: dict = {"scenario": nom}
        for s in seuils:
            row[f">= {int(s*100)} %"] = _fmt_annee(_annee_franchissement(df["tau_N"], s, "hausse"))
        lignes.append(row)
    return pd.DataFrame(lignes).set_index("scenario")


def table_seuils_pw(
    traj: dict[str, pd.DataFrame],
    seuils: list[float],
) -> pd.DataFrame:
    """
    Seuil-pension (scenario L) : premiere annee P/W <= seuil, par scenario.
    """
    lignes = []
    for nom, df in traj.items():
        row: dict = {"scenario": nom}
        for s in seuils:
            row[f"<= {int(s*100)} %"] = _fmt_annee(_annee_franchissement(df["pw_L"], s, "baisse"))
        lignes.append(row)
    return pd.DataFrame(lignes).set_index("scenario")


def table_validation_cor(
    traj: dict[str, pd.DataFrame],
    hyp: dict,
) -> pd.DataFrame:
    """
    Compare le modele aux benchmarks COR aux jalons 2026, 2040, 2070.
    Benchmarks source : COR rapport annuel juin 2025 ; hypotheses.yaml calage_economique.
    Limite : comparaison depenses % PIB non disponible (part_salaires_dans_PIB = PLACEHOLDER).
    """
    b_2026 = hyp["calage_economique"]["cibles_2026"]
    b_2070 = hyp["calage_economique"]["benchmarks_COR_2070"]

    COR = {
        2026: {"ra": b_2026["ratio_RA"],
               "pw": hyp["pensions"]["ratio_pension_salaire_2026"]},
        2040: {"ra": None, "pw": None},
        2070: {"ra": b_2070["ratio_RA"],
               "pw": b_2070.get("pw_L_g007")},
    }

    df_c = traj["central"]
    lignes = []
    for an, ref in COR.items():
        if an not in df_c.index:
            continue
        ra  = df_c.loc[an, "ratio_eco"]
        pw  = df_c.loc[an, "pw_L"]

        def fmt_ecart(mod, r):
            if r is None:
                return "—"
            return f"{(mod / r - 1) * 100:+.1f} %"

        lignes.append({
            "Annee":       an,
            "R/A modele":  f"{ra:.3f}",
            "R/A COR":     f"{ref['ra']:.3f}" if ref["ra"] else "n.d.",
            "Ecart R/A":   fmt_ecart(ra, ref["ra"]),
            "P/W(L)":      f"{pw:.3f}",
            "P/W COR ref": f"{ref['pw']:.3f}" if ref["pw"] else "n.d.",
            "Ecart P/W":   fmt_ecart(pw, ref["pw"]),
        })
    return pd.DataFrame(lignes).set_index("Annee")


# ---------------------------------------------------------------------------
#  Figures
# ---------------------------------------------------------------------------

_NOMS = {
    "central":          "Central",
    "fecondite_haute":  "Fecondite haute (ICF 1,70)",
    "fecondite_basse":  "Fecondite basse (ICF 1,20)",
    "migration_haute":  "Migration haute (+230 k/an)",
    "migration_basse":  "Migration basse (+70 k/an)",
}

_STYLES_FAN = {
    "central":          {"color": "black",   "lw": 2.5, "ls": "-",  "zorder": 5},
    "fecondite_haute":  {"color": "#D4813B", "lw": 1.5, "ls": "--", "zorder": 3},
    "fecondite_basse":  {"color": "#D4813B", "lw": 1.5, "ls": ":",  "zorder": 3},
    "migration_haute":  {"color": "#2176AE", "lw": 1.5, "ls": "--", "zorder": 4},
    "migration_basse":  {"color": "#2176AE", "lw": 1.5, "ls": ":",  "zorder": 4},
}

_NOTE_SOURCE = (
    "Projection conditionnelle (toutes choses egales par ailleurs). "
    "Sources : hypotheses demographiques INSEE IP2108 (08/06/2026), "
    "hypotheses economiques COR rapport annuel juin 2025."
)


def fig_ciseaux(df: pd.DataFrame, chemin: Path) -> None:
    """
    Fig.1 — tau*(N) montant vs P/W(L) descendant, scenario central.

    La figure illustre le trade-off fondamental du systeme par repartition :
    sous le scenario N (parite), le taux de cotisation d'equilibre augmente ;
    sous le scenario L (legislation constante), la pension relative se degrade.
    Les deux courbes forment un 'ciseau' qui s'ecarte progressivement.
    """
    fig, ax = plt.subplots(figsize=(8.5, 5))

    x   = df.index.values
    tN  = df["tau_N"].values * 100
    pwL = df["pw_L"].values * 100

    ax.plot(x, tN,  color="#C0392B", lw=2.2,
            label=r"$\tau^*(N)$ — cotisation d'equilibre (parite pensions)")
    ax.plot(x, pwL, color="#2176AE", lw=2.2,
            label=r"$\bar{P}/\bar{W}(L)$ — pension relative (legislation constante)")
    ax.fill_between(x, tN, pwL, alpha=0.06, color="grey")

    # Seuils de lecture illustratifs (sensibilite 45/50 %, non normatifs)
    for s in (40, 45, 50):
        ax.axhline(s, color="#999", lw=0.7, ls="--", alpha=0.55)
        ax.text(2071.3, s, f"{s} %", va="center", fontsize=8, color="#888")

    ax.set_xlim(2025, 2072)
    ax.set_ylim(25, 62)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
    ax.set_xlabel("Annee")
    ax.set_ylabel("% du salaire brut moyen")
    ax.set_title(
        u"Taux de cotisation d'equilibre et pension relative — scenario central\n"
        u"INSEE IP2108 (2026), activite projetee COR 2025",
    )
    ax.legend(fontsize=9, framealpha=0.9, loc="upper center")
    ax.text(0.01, -0.13, _NOTE_SOURCE,
            transform=ax.transAxes, fontsize=7, color="#666")

    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(chemin, dpi=150)
    plt.close(fig)
    print(f"  Fig.1 -> {chemin.name}")


def fig_fan_tau_N(traj: dict[str, pd.DataFrame], chemin: Path) -> None:
    """
    Fig.2 — Faisceau tau*(N) sur les 5 scenarios demographiques.

    Note pedagogique codee ici (Tache A.2) :
    La fecondite ne mord sur tau* qu'apres ~2048 : un enfant ne en 2028 cotise
    vers 2050-2052 seulement. Avant 2048, les scenarios fecondite haute/basse
    sont quasi-superposes. La migration, en revanche, modifie le stock de
    cotisants des l'annee suivante : l'ecart migration haute/basse est visible
    des 2030. La figure devrait montrer : fecondite B/H confondues avant ~2045,
    migration B/H ecartees des 2030.
    """
    fig, ax = plt.subplots(figsize=(9, 5.5))

    for nom, df in traj.items():
        st = _STYLES_FAN.get(nom, {"color": "grey", "lw": 1.0, "ls": "-", "zorder": 2})
        ax.plot(df.index, df["tau_N"] * 100,
                label=_NOMS.get(nom, nom), **st)

    for s, ls in ((35, "--"), (40, ":"), (45, "--")):
        ax.axhline(s, color="#999", lw=0.7, ls=ls, alpha=0.55)
        ax.text(2071.3, s, f"{s} %", va="center", fontsize=7.5, color="#888")

    ax.set_xlim(2025, 2072)
    ax.set_ylim(26, 47)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
    ax.set_xlabel("Annee")
    ax.set_ylabel("% du salaire brut moyen")
    ax.set_title(
        u"Taux de cotisation d'equilibre $\\tau^*(N)$ — sensibilite aux scenarios demographiques\n"
        u"INSEE IP2108 (2026), activite projetee COR 2025",
    )
    ax.legend(fontsize=8.5, framealpha=0.9, loc="upper left")
    ax.text(0.01, -0.13, _NOTE_SOURCE,
            transform=ax.transAxes, fontsize=7, color="#666")

    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(chemin, dpi=150)
    plt.close(fig)
    print(f"  Fig.2 -> {chemin.name}")


# ---------------------------------------------------------------------------
#  Pipeline principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    hyp = charger_hypotheses(RACINE / "config" / "hypotheses.yaml")
    d   = hyp["donnees"]

    chemins = {
        "central":         RACINE / d["ip2108_central"],
        "fecondite_haute": RACINE / d["ip2108_fec_haute"],
        "fecondite_basse": RACINE / d["ip2108_fec_basse"],
        "migration_haute": RACINE / d["ip2108_smi_haut"],
        "migration_basse": RACINE / d["ip2108_smi_bas"],
    }

    print("Chargement des 5 pyramides demographiques (2026-2070)...")
    populations = {
        nom: charger_pyramide_scenario(chemin, nom)
        for nom, chemin in chemins.items()
    }

    print("Calcul des trajectoires (activite_projetee, regimes N et L)...")
    traj = trajectoires_scenarios(hyp, populations, scenario_activite="activite_projetee")

    # -----------------------------------------------------------------------
    #  Tache B — Seuils
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("SEUIL-COTISATION : premiere annee tau*(N) >= seuil")
    print("Assiette : salaire BRUT (convention COR)")
    print("0.50 attendu non franchi d'ici 2070 — c'est un resultat")
    print("=" * 70)
    t_tau = table_seuils_tau(traj, [0.35, 0.40, 0.45, 0.50])
    print(t_tau.to_string())

    print()
    print("=" * 70)
    print("SEUIL-PENSION (scenario L) : premiere annee P/W <= seuil")
    print("Sensibilite au seuil : lire 45/50 % comme bornes, pas comme valeur unique")
    print("=" * 70)
    t_pw = table_seuils_pw(traj, [0.50, 0.45, 0.40])
    print(t_pw.to_string())

    # -----------------------------------------------------------------------
    #  Tache C7 — Validation COR
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("VALIDATION COR — jalons 2026 / 2040 / 2070")
    print("Cible CLAUDE.md S5 : convergence +/-0.5 pt PIB sur 2030-2040")
    print("(comparaison pts PIB suspendue : part_salaires_dans_PIB = PLACEHOLDER)")
    print("=" * 70)
    t_cor = table_validation_cor(traj, hyp)
    print(t_cor.to_string())

    # -----------------------------------------------------------------------
    #  Pedagogie temporelle : verification fecondite vs migration
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("PEDAGOGIE TEMPORELLE — fecondite vs migration (ecart sur tau_N)")
    print("Attendu : fecondite H/B ~ 0 avant 2045 ; migration H/B visible des 2030")
    print("=" * 70)
    print(f"  {'Annee':>6}  {'|fec_H - fec_B|':>17}  {'|mig_H - mig_B|':>17}")
    print("  " + "-" * 48)
    for an in [2030, 2040, 2045, 2050, 2060, 2070]:
        def _get(sc, a):
            return traj[sc].loc[a, "tau_N"] if a in traj[sc].index else float("nan")
        fh, fb = _get("fecondite_haute", an), _get("fecondite_basse", an)
        mh, mb = _get("migration_haute", an), _get("migration_basse", an)
        print(f"  {an:>6}  {abs(fh - fb)*100:>16.3f} %  {abs(mh - mb)*100:>16.3f} %")

    # -----------------------------------------------------------------------
    #  Figures
    # -----------------------------------------------------------------------
    print()
    print("Generation des figures...")
    df_c = traj["central"]
    fig_ciseaux(df_c,   REP_FIGURES / f"fig1_ciseaux_{HORODATAGE}.png")
    fig_fan_tau_N(traj, REP_FIGURES / f"fig2_fan_tauN_{HORODATAGE}.png")
    print("Pipeline termine.")
