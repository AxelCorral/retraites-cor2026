# Soutenabilité des retraites — Maquette comptable reproductible (COR 2026)

Maquette comptable agrégée calculant le taux de cotisation d'équilibre du système
de retraite français par répartition sous les projections démographiques Insee 2026
(Insee Première n°2108, 08/06/2026).

> **Ce n'est PAS un modèle de projection au sens du COR.** La valeur ajoutée est la
> transparence et la reproductibilité : équation fermée, paramètres sourcés, tests
> de calage automatisés. Le COR est un benchmark de validation, pas un adversaire.

## Équation fondamentale

    tau*(t) = [ R(t) / A(t) ] × [ Pbar(t) / Wbar(t) ]

- `R/A` : ratio de dépendance économique (retraités / cotisants)
- `P/W` : pension moyenne relative (pension / salaire moyen)

## Structure du dépôt

```
config/hypotheses.yaml     Source unique de vérité — tous les paramètres, sourcés et datés
src/maquette.py            Équations fondamentales, testables unitairement
src/figures.py             Pipeline complet (4 figures académiques)
src/figures_social.py      Figures adaptées pour diffusion (LinkedIn/réseaux)
src/data_insee.py          Chargeurs pyramides IP2108 (5 scénarios)
tests/                     21 tests de calage (démographique + économique + compagnon)
figures/                   Figures générées (académiques)
figures/social/            Figures générées (diffusion)
docs/                      Mémoire PDF + inventaire données COR 2026
```

## Données sources (non versionnées)

`data/raw/` n'est pas versionné (données officielles non redistribuables).
Les fichiers sont téléchargeables depuis les URLs dans `config/hypotheses.yaml` :

- **IP2108** — [insee.fr/fr/statistiques/8990852](https://www.insee.fr/fr/statistiques/8990852)
  (population par âge fin × année × scénario, 1962–2070)
- **COR 2026** — [cor-retraites.fr/publications/rapport-annuel-2026](https://www.cor-retraites.fr/publications/rapport-annuel-2026)
  (données P1–P4 et synthèse)

## Lancer

```bash
pip install -r requirements.txt
python -m pytest tests/ -q          # 21 tests — doit être vert avant toute interprétation
python src/maquette.py              # trajectoire tau*(t) 2026–2070
python src/figures.py               # génère figures/ (4 figures académiques)
python src/figures_social.py        # génère figures/social/
```

## Résultats principaux (calage COR 2026)

| Indicateur | Valeur maquette | Cible COR 2026 |
|---|---|---|
| tau*(2026) | ~30,5 % | ~28 % effectif (écart = marge sécurité) |
| R/A (2026) | ~0,56 | 0,569 |
| R/A (2070) | ~0,77 | 0,766 |
| ratio 65+/20-64 (2026) | 40 | 40 (IP2108) |
| ratio 65+/20-64 (2040) | 49 | 49 (IP2108) |
| ratio 65+/20-64 (2070) | 62 | 62 (IP2108) |

Convergence COR : **±0,5 pt de PIB sur 2030–2040** (objectif atteint sur R/A).

## Scénarios

- **Démographiques** : central + fécondité basse/haute + migration basse/haute (IP2108)
- **Indexation** : Scénario L (prix, P/W décroissant) vs Scénario N (parité, P/W constant)
- **Levier âge** : décalage 0/+1/+2 an du profil d'activité/retraite

## Licences

- **Code** : MIT — voir [LICENSE](LICENSE)
- **Texte du mémoire et figures** : CC BY 4.0 — voir [LICENSE](LICENSE)
