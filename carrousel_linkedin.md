# Carrousel LinkedIn — contenu slide par slide

But : vitrine portfolio. Langage clair (zéro jargon en surface), une idée par slide, cadrage méthode/reproductibilité (neutre). Format conseillé : document PDF 1080×1080 ou 1080×1350, 7 slides.

---

## Slide 1 — Accroche
**Le Conseil d'orientation des retraites a publié son rapport 2026 le 11 juin.**
Trois jours plus tard, je l'avais reconstruit — en open source.

*(visuel : titre sobre, ton nom, fond épuré ; pas de figure)*

---

## Slide 2 — La question
« Le système de retraite va-t-il s'effondrer ? »

C'est mal posé. Mon analyse montre qu'il n'existe pas de date d'effondrement : tout dépend de **qui paie l'ajustement** — les actifs, les retraités, ou l'âge de départ.

*(visuel : les trois leviers, schéma simple)*

---

## Slide 3 — Résultat 1 : les ciseaux
**À loi inchangée, les cotisations restent stables… mais les pensions décrochent.**

La pension moyenne passerait de 55 % à environ 40 % du salaire moyen d'ici 2070.
La pression démographique n'est pas absente — elle est absorbée par le niveau de vie relatif des retraités.

*(visuel : Figure 2 — les ciseaux)*

---

## Slide 4 — Résultat 2 : le prix de la parité
**Pour maintenir les pensions au niveau des salaires, il faudrait +11 points de cotisations** (jusqu'à ~42 %).

Mais reculer l'âge effectif de départ de deux ans efface près de la moitié de cette hausse. L'âge est le levier qui desserre l'arbitrage.

*(visuel : Figure 4 — frontières d'équilibre)*

---

## Slide 5 — La validation
**Mon modèle ouvert reproduit les chiffres officiels du COR à ±2,4 % sur 44 ans** (−0,6 % en 2070).

Sans aucun réglage sur les résultats du COR : les hypothèses sont des entrées documentées, le reste est calculé.

*(visuel : Figure 1 — validation R/A maquette vs COR)*

---

## Slide 6 — La nuance que tout le monde rate
**La baisse de la natalité ne menace pas l'équilibre avant ~2048.**

Un enfant né en 2028 ne cotise pas avant 2050. Le choc des deux prochaines décennies est déjà inscrit dans la pyramide des âges — il ne dépend pas de la fécondité.

*(visuel : Figure 3 — faisceau démographique)*

---

## Slide 7 — Le point + appel à l'action
Ce projet n'est pas une opinion sur les retraites.

C'est une démonstration : un diagnostic de finances publiques produit par une institution spécialisée peut être **reconstruit en transparence, rejoué et audité par n'importe qui.**

Pipeline Python, hypothèses explicites, tests de calage — tout est open source.
**→ Code et mémoire complet : github.com/axelcorral/retraites-cor2026**

*(visuel : capture du dépôt / logo Python + GitHub)*
