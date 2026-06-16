"""
figures_social.py — Versions réseaux sociaux des 4 figures de la maquette.

Usage : python src/figures_social.py
Sorties dans figures/social/ :
  fig1_ciseaux_social.png
  fig2_fan_tauN_social.png
  fig3_frontiere_2070_social.png
  fig4_validation_RA_social.png

GARDE-FOU : ce module ne modifie aucun calcul ni aucune figure académique.
Il réutilise les fonctions de calcul de maquette.py, data_insee.py et
figures.py, et redéfinit uniquement le rendu graphique (mise en page,
tailles de police, simplifications visuelles).
"""

from __future__ import annotations
from pathlib import Path
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

RACINE = Path(__file__).parent.parent
sys.path.insert(0, str(RACINE / "src"))

from maquette import (                                          # noqa: E402
    charger_hypotheses, trajectoires_scenarios,
    profils_annee_decale, cotisants, retraites,
)
from data_insee import charger_pyramide_scenario               # noqa: E402
from figures import grille_RA, _pw_L                           # noqa: E402

REP_SOCIAL = RACINE / "figures" / "social"
REP_SOCIAL.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
#  Style commun réseaux sociaux
# ---------------------------------------------------------------------------
_STYLE_SOCIAL = {
    "font.family":       "sans-serif",
    "font.size":         20,
    "axes.titlesize":    20,
    "axes.labelsize":    19,
    "xtick.labelsize":   17,
    "ytick.labelsize":   17,
    "legend.fontsize":   16,
    "lines.linewidth":   3.0,
    "axes.spines.top":   False,
    "axes.spines.right": False,
}

_NOTE_SOURCE = (
    "Sources : INSEE IP2108 (08/06/2026), COR rapport annuel juin 2026. "
    "Projection conditionnelle — toutes choses égales par ailleurs."
)


def _sauvegarder(fig: plt.Figure, chemin: Path) -> None:
    fig.savefig(chemin, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {chemin.relative_to(RACINE)}")


# ---------------------------------------------------------------------------
#  Fig 1 — Ciseaux (social)
# ---------------------------------------------------------------------------

def fig1_ciseaux_social(df: pd.DataFrame, chemin: Path) -> None:
    """
    Ciseaux tau*(N) montant vs P/W(L) descendant — version réseaux sociaux.
    Labels directs aux extrémités, pas de légende classique.
    """
    with plt.rc_context(_STYLE_SOCIAL):
        fig, ax = plt.subplots(figsize=(8, 6.5))

        x   = df.index.values
        tN  = df["tau_N"].values * 100
        pwL = df["pw_L"].values * 100

        ax.plot(x, tN,  color="#C0392B", lw=3.2)
        ax.plot(x, pwL, color="#2176AE", lw=3.2)
        ax.fill_between(x, tN, pwL, alpha=0.07, color="grey")

        # Ligne de référence 40 %
        ax.axhline(40, color="#bbb", lw=1.0, ls="--", alpha=0.7)

        # Labels directs sur les courbes (remplacent la légende)
        idx55 = len(x) // 3
        ax.text(x[idx55], tN[idx55] - 2.5,
                r"Cotisation $\tau^*(N)$", color="#C0392B",
                fontsize=15, ha="center", fontweight="bold")
        ax.text(x[idx55], pwL[idx55] + 2.0,
                r"Pension $\bar{P}/\bar{W}(L)$", color="#2176AE",
                fontsize=15, ha="center", fontweight="bold")

        # Étiquettes aux 4 extrémités
        ax.text(2025.0, tN[0] - 0.5,
                f"{tN[0]:.1f} %", color="#C0392B",
                fontsize=17, va="top", ha="left", fontweight="bold")
        ax.text(2025.0, pwL[0] + 0.5,
                f"{pwL[0]:.1f} %", color="#2176AE",
                fontsize=17, va="bottom", ha="left", fontweight="bold")
        ax.text(2070.3, tN[-1] + 0.5,
                f"{tN[-1]:.1f} %", color="#C0392B",
                fontsize=17, va="bottom", ha="left", fontweight="bold")
        ax.text(2070.3, pwL[-1] - 0.5,
                f"{pwL[-1]:.1f} %", color="#2176AE",
                fontsize=17, va="top", ha="left", fontweight="bold")

        ax.set_xlim(2025, 2077)
        ax.set_ylim(24, 62)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
        ax.set_xlabel("Année")
        ax.set_ylabel("% du salaire brut moyen")
        ax.set_title(
            "Les ciseaux : cotisation monte, pension baisse\n"
            "Scénario central INSEE IP2108 (2026), activité projetée COR 2025",
            fontsize=17,
        )
        fig.text(0.01, 0.005, "Source : INSEE IP2108 (2026), COR 2026. "
                 "Projection conditionnelle.",
                 fontsize=9, color="#aaa")

        fig.tight_layout()
        _sauvegarder(fig, chemin)


# ---------------------------------------------------------------------------
#  Fig 2 — Faisceau tau*(N) avec enveloppe (social)
# ---------------------------------------------------------------------------

def fig2_fan_social(traj: dict[str, pd.DataFrame], chemin: Path) -> None:
    """
    Faisceau tau*(N) — courbe centrale en gras + enveloppe min/max des
    scénarios alternatifs en fill_between. Légende 2 entrées.
    """
    with plt.rc_context(_STYLE_SOCIAL):
        fig, ax = plt.subplots(figsize=(8, 6.5))

        df_c   = traj["central"]
        annees = df_c.index.values

        # Enveloppe min/max sur tous les scénarios non centraux
        alt = [df["tau_N"] for nom, df in traj.items() if nom != "central"]
        env_min = pd.concat(alt, axis=1).min(axis=1) * 100
        env_max = pd.concat(alt, axis=1).max(axis=1) * 100

        ax.fill_between(annees, env_min, env_max,
                        alpha=0.22, color="#888",
                        label="Fourchette des scénarios démographiques")
        ax.plot(annees, df_c["tau_N"] * 100,
                color="black", lw=3.8,
                label="Scénario central")

        ax.axhline(40, color="#bbb", lw=1.0, ls="--", alpha=0.7)
        ax.text(2071.5, 40, "40 %", va="center", fontsize=15, color="#999")

        ax.set_xlim(2025, 2077)
        ax.set_ylim(26, 47)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
        ax.set_xlabel("Année")
        ax.set_ylabel("% du salaire brut moyen")
        ax.set_title(
            r"Taux de cotisation d'équilibre $\tau^*(N)$"
            "\nSensibilité aux scénarios démographiques INSEE IP2108 (2026), "
            "activité projetée COR 2025",
            fontsize=16,
        )
        ax.legend(fontsize=15, framealpha=0.9, loc="upper left")
        fig.text(0.01, 0.005, "Source : INSEE IP2108 (2026), COR 2026. "
                 "Projection conditionnelle.",
                 fontsize=9, color="#aaa")

        fig.tight_layout()
        _sauvegarder(fig, chemin)


# ---------------------------------------------------------------------------
#  Fig 3 — Frontière d'équilibre 2070 (social)
# ---------------------------------------------------------------------------

def fig3_frontiere_social(
    grille: pd.DataFrame,
    hyp: dict,
    chemin: Path,
) -> None:
    """
    Frontière d'équilibre 2070 — version simplifiée réseaux sociaux.
    3 droites (décalages 0/1/2 ans), points de parité annotés en gros,
    point « Aujourd'hui 2026 ».
    """
    annee    = 2070
    pw_N     = hyp["pensions"]["ratio_pension_salaire_2026"]
    decalages = [0, 1, 2]
    pw_range  = [0.28, 0.63]   # légèrement élargi pour la lisibilité

    _STYLES = {
        0: {"color": "#1a1a2e", "lw": 2.8, "ls": "-"},
        1: {"color": "#4a5a9a", "lw": 2.5, "ls": "--"},
        2: {"color": "#8090c8", "lw": 2.5, "ls": ":"},
    }
    # Labels courts pour légende compacte : les tau*(N) sont annotés directement
    _LABELS = {0: "~64 ans (réforme 2023)", 1: "~65 ans", 2: "~66 ans"}

    with plt.rc_context(_STYLE_SOCIAL):
        fig, ax = plt.subplots(figsize=(8, 6.5))

        for d in decalages:
            ra  = grille.loc[annee, d]
            st  = _STYLES[d]
            col = st["color"]
            ax.plot(pw_range, [ra * v for v in pw_range],
                    label=_LABELS[d], **st)

            # Point carré de parité + annotation gros à droite de la ligne P/W(N)
            tau_pN = ra * pw_N
            ax.scatter([pw_N], [tau_pN], marker="s", s=150, color=col, zorder=6)
            ax.annotate(
                f"{tau_pN * 100:.1f} %",
                xy=(pw_N, tau_pN),
                xytext=(pw_N + 0.022, tau_pN),
                fontsize=16, color=col, fontweight="bold",
                ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=col, lw=1.2, alpha=0.5),
            )

        # Repère vertical P/W(N)
        ax.axvline(pw_N, color="#aaa", lw=1.0, ls="--", alpha=0.6)
        ax.text(pw_N - 0.003, 0.198,
                f"P/W parité = {pw_N:.0%}",
                ha="right", fontsize=12, color="#888", va="bottom")

        # Point « Aujourd'hui 2026 »
        b_2026    = hyp["calage_economique"]["cibles_2026"]
        tau_today = b_2026["ratio_RA"] * pw_N
        ax.scatter([pw_N], [tau_today], marker="o", s=130,
                   color="C3", zorder=7,
                   label=f"Aujourd'hui 2026  (τ* = {tau_today * 100:.1f} %)")
        ax.text(pw_N + 0.013, tau_today + 0.004,
                "2026", fontsize=13, color="C3")

        ax.set_xlim(*pw_range)
        ax.set_ylim(0.19, 0.445)   # ylim légèrement élargi pour les annotations
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
        ax.set_xlabel("Pension relative P/W  (% du salaire brut)")
        ax.set_ylabel("Cotisation d'équilibre τ*")
        ax.set_title(
            f"Frontière d'équilibre à l'horizon {annee}\n"
            "Levier âge de départ, scénario central INSEE IP2108 (2026)",
            fontsize=17,
        )
        # Légende compacte : labels courts, fontsize 12, petite boîte
        ax.legend(fontsize=12, framealpha=0.88, loc="upper left",
                  handlelength=2.0, borderpad=0.6, labelspacing=0.35)
        fig.text(0.01, 0.005, "Source : INSEE IP2108 (2026), COR 2026. "
                 "Projection conditionnelle.",
                 fontsize=9, color="#aaa")

        fig.tight_layout()
        _sauvegarder(fig, chemin)


# ---------------------------------------------------------------------------
#  Fig 4 — Validation R/A maquette vs COR 2026 (social) — pièce maîtresse
# ---------------------------------------------------------------------------

def fig4_validation_social(
    traj: dict[str, pd.DataFrame],
    chemin: Path,
) -> None:
    """
    Validation R/A maquette vs COR 2026 — version réseaux sociaux.
    Pièce maîtresse du carrousel : maquette noire épaisse, jalons COR gros
    points rouges annotés en grand, faisceau des scénarios très atténué.
    """
    COR_RA = {2026: 0.569, 2030: 0.571, 2040: 0.610, 2050: 0.650, 2070: 0.766}

    with plt.rc_context(_STYLE_SOCIAL):
        fig, ax = plt.subplots(figsize=(8, 6.5))

        # Faisceau scénarios alternatifs — très atténué, fond discret
        for nom, df in traj.items():
            if nom == "central":
                continue
            ax.plot(df.index, df["ratio_eco"],
                    color="#bbbbbb", lw=1.2, alpha=0.4)

        # Courbe maquette centrale — proéminente
        df_c = traj["central"]
        ax.plot(df_c.index, df_c["ratio_eco"],
                color="black", lw=4.0, zorder=5,
                label="Ma maquette (centrale)")

        # Jalons COR — gros points rouges
        cor_x = list(COR_RA.keys())
        cor_y = list(COR_RA.values())
        ax.scatter(cor_x, cor_y,
                   color="#C0392B", s=180, zorder=7,
                   label="COR 2026", marker="o")

        # Annotations jalons : offsets pour éviter chevauchement
        # 2026 et 2030 ont des R/A quasi-identiques : on sépare haut/bas
        _OFFSETS = {
            2026: (-5, -18),   # en-dessous (R/A 2026 ≈ R/A 2030)
            2030: ( 6,  10),   # au-dessus
            2040: ( 6,   8),
            2050: ( 6,   8),
            2070: (-10,  9),   # à gauche (bord droit du graphique)
        }
        for x, y in COR_RA.items():
            ox, oy = _OFFSETS.get(x, (6, 8))
            ax.annotate(
                f"{y:.3f}",
                xy=(x, y), xytext=(ox, oy),
                textcoords="offset points",
                fontsize=16, color="#C0392B", fontweight="bold",
            )

        ax.set_xlim(2025, 2072)
        ax.set_ylim(0.52, 0.83)
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.2f"))
        ax.set_xlabel("Année")
        ax.set_ylabel("Ratio retraités / cotisants")
        ax.set_title(
            "Ma maquette ouverte vs COR 2026 — écart ±2,4 %\n"
            "Ratio de dépendance économique, activité projetée COR 2025",
            fontsize=17,
        )
        ax.legend(fontsize=15, framealpha=0.9, loc="upper left")
        fig.text(
            0.01, 0.01,
            "COR 2026 : rapport annuel juin 2026, onglet Fig 2.3 P2. " + _NOTE_SOURCE,
            fontsize=10, color="#666",
        )

        fig.subplots_adjust(bottom=0.12, left=0.14, right=0.97, top=0.90)
        _sauvegarder(fig, chemin)


# ---------------------------------------------------------------------------
#  Pipeline principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    hyp = charger_hypotheses(RACINE / "config" / "hypotheses.yaml")
    d   = hyp["donnees"]

    chemins_xlsx = {
        "central":         RACINE / d["ip2108_central"],
        "fecondite_haute": RACINE / d["ip2108_fec_haute"],
        "fecondite_basse": RACINE / d["ip2108_fec_basse"],
        "migration_haute": RACINE / d["ip2108_smi_haut"],
        "migration_basse": RACINE / d["ip2108_smi_bas"],
    }

    print("Chargement des 5 pyramides démographiques (2026-2070)...")
    populations = {
        nom: charger_pyramide_scenario(chemin, nom)
        for nom, chemin in chemins_xlsx.items()
    }

    print("Calcul des trajectoires (activité projetée, régimes N et L)...")
    traj = trajectoires_scenarios(
        hyp, populations, scenario_activite="activite_projetee"
    )

    decalages = hyp["sensibilite"]["decalages_age_depart"]
    print("Calcul de la grille R/A (frontières d'équilibre, horizon 2070)...")
    grille = grille_RA(hyp, populations["central"], [2070], decalages)

    print("\nGénération des figures réseaux sociaux...")
    fig1_ciseaux_social(
        traj["central"],
        REP_SOCIAL / "fig1_ciseaux_social.png",
    )
    fig2_fan_social(
        traj,
        REP_SOCIAL / "fig2_fan_tauN_social.png",
    )
    fig3_frontiere_social(
        grille, hyp,
        REP_SOCIAL / "fig3_frontiere_2070_social.png",
    )
    fig4_validation_social(
        traj,
        REP_SOCIAL / "fig4_validation_RA_social.png",
    )

    print("\nPipeline terminé. Figures dans figures/social/")
