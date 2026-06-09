# Soutenabilité des retraites — Maquette comptable reproductible

Maquette comptable agrégée (PAS un modèle de projection au sens COR) calculant
le taux de cotisation d'équilibre du système de retraite français par répartition
sous les projections démographiques Insee 2026 (Insee Première n°2108, 08/06/2026).

## Équation fondamentale
    tau*(t) = [ R(t)/A(t) ] x [ Pbar(t)/Wbar(t) ]

## Structure
- config/hypotheses.yaml   -> TOUS les paramètres, sourcés (source unique de vérité)
- src/maquette.py          -> équations pures, testables
- tests/test_calage.py     -> tests fondateurs (40/49/62) — doivent passer avant toute conclusion
- data/raw/                -> fichiers sources Insee/COR/DREES, horodatés, jamais modifiés

## Lancer
    pip install pyyaml pytest pandas
    python -m pytest tests/ -q
    python src/maquette.py

## Prochaines étapes
1. Télécharger ip2108.xlsx + Insee Résultats compagnon (pop. par âge fin x scénario)
2. Remplacer les PLACEHOLDER de hypotheses.yaml par les valeurs COR/DREES
3. Activer le test 2070 (62) après chargement de la pyramide détaillée
4. Brancher trajectoire() sur les vraies données -> première courbe tau*(t)
