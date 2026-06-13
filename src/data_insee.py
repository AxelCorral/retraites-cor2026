"""
data_insee.py — Chargement des donnees brutes de l'IP2108.

Separe la lecture des fichiers (ce module) de la logique de la maquette
(maquette.py). Toutes les fonctions ici sont en lecture seule sur data/raw/.
Source : Insee Premiere n2108, 08/06/2026.
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd


def charger_pyramide_scenario(chemin: str | Path, scenario: str) -> pd.DataFrame:
    """
    Charge la pyramide des ages par age fin depuis un fichier Excel du compagnon IP2108.

    chemin   : chemin vers le fichier Excel (un fichier = un scenario)
    scenario : libelle documentaire du scenario (ex: "central", "fecondite_basse")

    Retourne un DataFrame :
      - Index   : age entier (0..106), age terminal "105+" normalise a 106
      - Colonnes : annees 2026..2070 (int)
      - Valeurs  : population totale (H+F), en individus

    Structure de l'onglet 'population' :
      - Ligne 0  : titre
      - Ligne 1  : "Age au 1er janvier" | 1962 | 1963 | ... | 2070
      - Lignes 2..107 : ages 0..104 + "105+"
      - Ligne 108 : "Total" (exclu)

    Source : Insee Resultats compagnon IP2108,
             https://www.insee.fr/fr/statistiques/8990852 (central)
             https://www.insee.fr/fr/statistiques/8990856 (scenarios alternatifs)

    Note : "105+" normalise a 106 (coherent avec charger_pyramide_age_fin qui normalise
           "106 ou plus" a 106). Pop(105+) = Pop(105) + Pop(106+) : ecart negligeable
           car ces ages ne contribuent ni a A(t) ni significativement a R(t).
    """
    raw = pd.read_excel(Path(chemin), sheet_name="population", header=None)

    # Identifier les colonnes des annees 2026-2070 dans la ligne d'en-tete
    header_row = raw.iloc[1]
    col_map = {}  # annee (int) -> position colonne dans raw
    for pos in range(1, len(header_row)):
        val = header_row.iloc[pos]
        if pd.notna(val):
            try:
                annee = int(val)
                if 2026 <= annee <= 2070:
                    col_map[annee] = pos
            except (ValueError, TypeError):
                pass

    annees = sorted(col_map)
    positions = [col_map[a] for a in annees]

    # Lignes 2..107 : ages 0..104 (105 lignes) + "105+" (1 ligne) = 106 lignes
    age_rows = raw.iloc[2:108, [0] + positions].copy()
    age_rows.columns = ["age"] + annees

    # "105+" -> 106 (meme convention que charger_pyramide_age_fin pour "106 ou plus")
    age_rows["age"] = (
        pd.to_numeric(age_rows["age"], errors="coerce").fillna(106).astype(int)
    )

    return age_rows.set_index("age")


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
