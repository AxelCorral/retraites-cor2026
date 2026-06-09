"""
data_insee.py — Chargement des donnees brutes de l'IP2108.

Separe la lecture des fichiers (ce module) de la logique de la maquette
(maquette.py). Toutes les fonctions ici sont en lecture seule sur data/raw/.
Source : Insee Premiere n2108, 08/06/2026.
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd


def charger_pyramide_age_fin(chemin: str | Path) -> pd.DataFrame:
    """
    Charge la pyramide des ages par age fin depuis la Figure 4 de l'IP2108.

    Retourne un DataFrame :
      - Index  : age entier (0..106), "106 ou plus" normalise a 106
      - Colonnes : [2026, 2070]
      - Valeurs : population totale (hommes + femmes), en individus
      - Scenario central uniquement (seul disponible dans cette figure)

    Source : ip2108.xlsx, feuille "Figure 4".
    Insee Premiere n2108, 08/06/2026.
    """
    df = pd.read_excel(chemin, sheet_name="Figure 4", header=None)

    # Lignes 4 a 110 : ages 0 a "106 ou plus"
    # (lignes 0-3 = en-tetes, 111+ = notes de lecture et champ)
    donnees = df.iloc[4:111].copy()
    donnees.columns = ["age", "h2026", "h2070", "f2026", "f2070"]

    # "106 ou plus" -> 106 ; impact negligeable (toujours dans les 65+)
    donnees["age"] = (
        pd.to_numeric(donnees["age"], errors="coerce").fillna(106).astype(int)
    )
    donnees = donnees.set_index("age")

    return pd.DataFrame({
        2026: donnees["h2026"] + donnees["f2026"],
        2070: donnees["h2070"] + donnees["f2070"],
    })
