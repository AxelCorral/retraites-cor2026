# Inventaire COR juin 2026 — Lecture seule

**Session** : 2026-06-13. Scope : comprendre et localiser, INTERDIT d'intégrer au modèle ou de re-calibrer.
**Source principale** : Rapport annuel du COR, juin 2026 (260 p.) + 5 fichiers Excel de données.

---

## 1. Fichiers téléchargés (data/raw/cor2026/)

| Fichier | Taille | Contenu |
|---------|--------|---------|
| `cor2026_rapport.pdf` | 5 632 Ko, 260 p. | Rapport complet |
| `cor2026_synthese.pdf` | 776 Ko | Synthèse 4 p. |
| `cor2026_donnees_P1.xlsx` | 499 Ko | Données Partie 1 (hypothèses) |
| `cor2026_donnees_P2.xlsx` | 719 Ko | Données Partie 2 (résultats financiers) |
| `cor2026_donnees_P3.xlsx` | 3 059 Ko | Données Partie 3 (objectifs de long terme) |
| `cor2026_donnees_P4.xlsx` | 242 Ko | Données Partie 4 (âges de départ) |
| `cor2026_donnees_synthese.xlsx` | 286 Ko | Indicateurs récapitulatifs |

**Note** : `cor2026_donnees_P3.xlsx` contient du XML invalide (PrintTitles #N/A) — openpyxl ne peut pas le lire directement. Lecture possible via zipfile pour les noms d'onglets, ou xlrd/pandas avec engine openpyxl en mode tolérant.

---

## 2. Cartographie des onglets clés

### cor2026_donnees_synthese.xlsx

| Onglet | Indicateur | Concept |
|--------|-----------|---------|
| `Dépenses en %` | Dépenses du système de retraite en % du PIB | Sc. Ref 2026-2070 |
| `Ressources en %` | Ressources en % du PIB | Sc. Ref 2026-2070 |
| `Solde en %` | Solde (dépenses − ressources) en % du PIB | Métadonnées datent COR 2025, valeurs cohérentes avec COR 2026 |
| `Solde dépenses ressources` | Tableau récap. (dépenses + ressources + solde) | Sc. Ref, COR 2026 confirmé |
| `Âge conjoncturel` | Âge moyen de départ à la retraite | Observé + projeté (tous scénarios) |
| `Niveau de vie relatif` | Niveau de vie moyen retraités / ensemble pop. | COR + projection modèle Destinie |
| `Sensibilité` | Écarts dépenses et solde selon hypothèses économiques/démographiques | 2045 et 2070 |
| `Effet PIB` | Effets des 4 leviers sur PIB/emploi/solde | Tableau 2.10 résumé |

### cor2026_donnees_P2.xlsx (résultats financiers)

| Onglet | Contenu |
|--------|---------|
| `Fig 2.3` | Pension relative (2.2a) + rapport cotisants/retraités (2.2b), obs + Sc. Ref 2026-2070 |
| `Tab 2.2` | Structure des ressources 2025 (en Md€ et %) |
| `Tab 2.5` | Décomposition écarts dépenses COR 2026 vs COR 2025 (2030, 2045, 2070) |
| `Tab 2.10` | Tableau leviers macroéconomiques (DG Trésor / I-MIP / OFCE) |
| `Tab 2.11` | Tax gap — ajustement immédiat nécessaire (5/20/25/45 ans) |

### cor2026_donnees_P4.xlsx (âges de départ)

| Onglet | Contenu |
|--------|---------|
| `Fig 4.1` | Taux d'emploi des 55-69 ans par tranche d'âge, obs + projections |
| `Fig. 4.5` | Âge moyen de départ par génération (obs + projeté, modèle Trajectoire) |
| `Fig 4.6` | Taux de retraités et de nouveaux retraités par âge, 2024 |

---

## 3. Hypothèses COR 2026 — changements vs COR 2025

### Démographie (Partie 1)
- **Nouveau** : projections **IP2108** (Insee Première n°2108, 08/06/2026)
  - ICF : **1,45** enfant/femme à partir de 2028 (vs 1,80 dans COR 2025)
  - Migration nette : **+150 000**/an (vs +70 000 dans COR 2025)
  - Espérance de vie : poursuite des gains tendanciels (identique)

### Mesures réglementaires (Partie 1, ch. 2)
- **LFSS 2026** : suspension partielle de la réforme 2023 à partir de septembre 2026
  - Génér. 1964-1968 : âge d'ouverture des droits maintenu à 63 ans (au lieu de monter vers 64)
  - L'âge de 64 ans ne s'applique qu'à partir de la génération **1969** (vs 1968 initialement)
- **Hypothèse Agirc-Arrco** : revalorisation des points révisée à la hausse sur la période de projection (impact +0,26 pt PIB sur les dépenses en 2070)

### Hypothèses économiques
- Productivité : 0,7 %/an à partir de 2040 (scénario de référence) — inchangé
- Chômage : 7,0 % à partir de 2040 — inchangé

---

## 4. Résultats financiers COR 2026 (scénario de référence)

Convention : EPR (contributions d'équilibre évoluent pour solder les régimes chaque année).
Champ : ensemble des régimes légalement obligatoires, y compris FSV, hors RAFP.

### Indicateurs clés aux jalons

| Année | Dépenses %PIB | Ressources %PIB | Solde %PIB |
|-------|:------------:|:---------------:|:----------:|
| 2026  | 14,13 %      | 13,96 %         | −0,16 %    |
| 2030  | 14,07 %      | 13,87 %         | −0,20 %    |
| 2040  | 14,00 %      | 13,43 %         | −0,61 %    |
| 2050  | 14,42 %      | 13,13 %         | −1,00 %    |
| 2060  | 14,70 %      | 12,98 %         | −1,72 %    |
| 2070  | 15,30 %      | 12,91 %         | −2,39 %    |

Source : `cor2026_donnees_synthese.xlsx`, onglets `Dépenses en %`, `Ressources en %`, `Solde dépenses ressources`.

### Rapport démographique (cotisants/retraités) — Fig 2.3 P2

| Année | Cotisants/retraités | R/A (inverse) |
|-------|:-----------------:|:-------------:|
| 2026  | 1,759             | 0,569         |
| 2030  | 1,750             | 0,571         |
| 2040  | 1,640             | 0,610         |
| 2050  | 1,539             | 0,650         |
| 2070  | 1,305             | 0,766         |

Source : `cor2026_donnees_P2.xlsx`, onglet `Fig 2.3`, série "2.2b".

### Pension relative (pension moy. / revenu brut d'activité moyen) — Fig 2.3 P2

| Année | P/W Sc. Ref COR 2026 |
|-------|:-------------------:|
| 2026  | 55,0 %              |
| 2030  | 55,2 %              |
| 2040  | 51,6 %              |
| 2050  | 49,7 %              |
| 2070  | 45,3 %              |

Source : `cor2026_donnees_P2.xlsx`, onglet `Fig 2.3`, série "2.2a".
**Note** : concept ≠ scénario L de la maquette. Le COR 2026 inclut la revalorisation Agirc-Arrco projetée ; ce n'est pas une indexation prix pure.

### Âge conjoncturel de départ à la retraite

| Année | Âge moyen (ans) | Statut |
|-------|:---------------:|--------|
| 2024  | 63,13           | Observé |
| 2026  | 63,44           | Projeté |
| 2030  | 64,08           | Projeté |
| 2040  | 64,51           | Projeté |
| 2070  | 64,63           | Projeté |

Source : `cor2026_donnees_synthese.xlsx`, onglet `Âge conjoncturel`. Modèles Ancêtre et Trajectoire (DREES).
L'âge se stabilise autour de **64,6 ans** à partir des générations nées dans les années 1975 (p. 215 rapport).

### Niveau de vie relatif des retraités

| Repère | Valeur |
|--------|--------|
| 2023 (obs) | ~100,2 % |
| 2040 (proj) | ~96,3 % |
| 2070 (proj) | ~90,3 % |

Source : `cor2026_donnees_synthese.xlsx`, onglet `Niveau de vie relatif`. Modèle Destinie (INSEE).

---

## 5. Tableau 2.10 — Effets macroéconomiques des leviers d'ajustement

Source : p. 123-125 du rapport (SG COR d'après DG Trésor, I-MIP/CepreHANK, OFCE/EmeRaude).
Calibrage : 0,2 pt PIB = 6 Md€ ex ante. Écart au compte central.

| Mesure | Horizon | PIB (%) | Emploi (milliers) | Solde primaire APU (pts PIB) |
|--------|---------|:-------:|:-----------------:|:-----------------------------:|
| **Modération pensions 6 Md€** | 2 ans | −0,1 à −0,2 | −10 à −20 | +0,1 |
| | 10 ans | −0,1 à −0,2 | −10 à −25 | +0,1 |
| | 20 ans | −0,1 | −5 à −10 | +0,1 |
| **Hausse cotis. employeurs 6 Md€** | 2 ans | −0,1 | −25 à −50 | +0,1 |
| | 10 ans | −0,1 à −0,3 | −20 à −75 | 0 à +0,1 |
| | 20 ans | −0,1 à −0,3 | −15 à −80 | 0 à +0,1 |
| **Hausse cotis. salariés 6 Md€** | 2 ans | −0,1 à −0,2 | −15 à −30 | +0,1 |
| | 10 ans | −0,1 à −0,2 | −20 à −70 | +0,1 |
| | 20 ans | −0,1 à −0,3 | −15 à −80 | +0,05 à +0,1 |
| **+1 an AOD** | 2 ans | +0,1 à +0,5 | +50 à +140 | +0,05 à +0,4 |
| | 10 ans | +0,5 à +0,7 | +160 à +250 | +0,3 à +0,6 |
| | 20 ans | +0,1 à +0,8 | +200 à +240 | +0,3 à +0,65 |

**Conclusion qualitative** (p. 123) : «Trois des quatre leviers étudiés — baisse relative des pensions, hausse des cotisations salariales et hausse des cotisations employeurs — présentent un caractère **récessif**. Seul le recul de l'âge de départ à la retraite apparaît, dans les modèles étudiés, comme **expansionniste** pour garantir la soutenabilité.»

Données localisées : `cor2026_donnees_synthese.xlsx`, onglet `Effet PIB` ; et `cor2026_donnees_P2.xlsx`, onglet `Tab 2.10`.

---

## 6. Scénario d'ajustement par l'âge seul (p. 126 rapport)

Pour équilibrer structurellement le système chaque année jusqu'en 2070 par le seul levier de l'âge :

| Année | Âge moyen requis | Écart vs spontané |
|-------|:----------------:|:-----------------:|
| 2030  | 64,2 ans         | +0,3 an           |
| 2045  | 65,6 ans         | +1,2 an           |
| 2070  | **67,6 ans**     | +3,0 ans          |

L'âge «spontané» sous législation constante se stabilise autour de **64,6 ans** à partir des générations ~1975.
Confirme la valeur attendue ~67,6 ans à 2070 utilisée dans la cartographie de la maquette.

---

## 7. Écarts COR 2026 vs COR 2025 (Tab 2.5 P2)

Décomposition de la **hausse des dépenses** en part de PIB en 2070 entre COR 2026 et COR 2025 :

| Facteur | 2030 | 2045 | 2070 |
|---------|:----:|:----:|:----:|
| **Écart total dépenses** | +0,11 | +0,003 | **+1,12** pt PIB |
| Dont démographie nette | −0,10 | −0,34 | +0,36 |
| — Fécondité (plus basse : 1,45 vs 1,80) | −0,002 | +0,10 | **+1,51** |
| — Migration (plus élevée : +150k vs +70k) | −0,08 | −0,35 | **−0,96** |
| — Espérance de vie | −0,02 | −0,10 | −0,19 |
| Dont hypothèses économiques | +0,16 | +0,05 | +0,06 |
| Dont LFSS 2026 (suspension réforme) | +0,06 | +0,03 | +0,07 |
| Dont revalorisation Agirc-Arrco | 0 | +0,07 | **+0,26** |

Lecture : la révision démographique (fécondité fortement abaissée, migration relevée) dégrade de +1,12 pt PIB les dépenses projetées à 2070. La migration atténue partiellement cet effet (−0,96 pt), mais la fécondité dommine (+1,51 pt).

---

## 8. Parties du rapport à retenir pour le mémoire

| Section PDF | Pages | Pertinence |
|-------------|-------|-----------|
| Partie 1, ch. 1 | 31-56 | Hypothèses démographiques IP2108 (détail) |
| Partie 2, ch. 6 | 121-128 | **Leviers d'ajustement et leurs effets macro** ← cœur |
| Partie 2, ch. 5 | 109-120 | Sensibilité aux hypothèses |
| Partie 3, ch. 2 | 143-158 | Niveau de vie des retraités, pension relative |
| Partie 4, ch. 2 | 215-222 | **Âges de départ par génération** ← cœur |
| Annexe 1 | 223-224 | Notes méthodologiques DG Trésor / I-MIP / OFCE |

---

## 9. Ce que la maquette peut et ne peut pas revendiquer comme original

### Peut valider par rapport au COR 2026
- **R/A 2026** : maquette 0,555 vs COR 0,569 → écart −2,5 % (acceptable, source IP2108 commune)
- **R/A 2070** : maquette 0,761 vs COR 0,766 → écart −0,7 % (excellent après correction immigration)
- **P/W 2070 scénario L** : maquette 0,383 vs COR référence 0,453 — écart important : le COR n'est PAS en indexation prix pure (inclut revalorisation Agirc-Arrco partielle) ; les deux concepts sont légitimes mais distincts

### Ne peut pas prétendre être original face au COR 2026
- Le tableau des leviers (Tableau 2.10) est entièrement produit par DG Trésor / I-MIP / OFCE
- L'âge de 67,6 ans à 2070 pour l'équilibre par l'âge seul est un résultat COR (p. 126)
- Les projections de dépenses %PIB (15,30 % en 2070) sont celles du COR
- La sensibilité aux scénarios démographiques est documentée dans le COR (Partie 2, ch. 5 et Tableau de sensibilité synthèse)

### Valeur ajoutée de la maquette face au COR 2026
- **Transparence** : équation explicite tau* = R/A × P/W, reproductible par tout lecteur
- **Décomposition** : sépare nettement le canal démographique (R/A) du canal économique (P/W)
- **Frontière d'équilibre** : cartographie dans l'espace (P/W, âge départ) — le COR calcule des trajectoires, pas de frontière iso-tau*
- **Scénarios démographiques** en éventail (5 scénarios IP2108) — le COR les traite en sensibilité, la maquette en multivarié systématique

---

## 10. À ne pas faire avant sourçage complémentaire

- **`part_salaires_dans_PIB = 0,57` (PLACEHOLDER)** : bloque la comparaison dépenses %PIB
  - Cible COR 2026 : 15,30 % en 2070 (Dépenses %PIB)
  - Maquette actuelle sans part_salaires sourcée : impossible à convertir en pts PIB
  - Source à utiliser : INSEE Comptes nationaux base 2020, tableau des emplois-ressources (TER), ligne D.1 / PIB aux prix courants

---

*Document produit le 2026-06-13. Session de lecture uniquement — aucun fichier src/ ni tests/ modifié.*
