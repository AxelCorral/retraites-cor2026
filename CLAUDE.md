# CLAUDE.md — Règles du projet « Soutenabilité des retraites »

Ce fichier fixe le cap méthodologique du projet. **Le lire avant toute action.**
Il prime sur toute intuition contraire. En cas de doute sur une règle, demander.

---

## 1. Nature du projet (ne jamais l'oublier)

Ceci est une **maquette comptable agrégée**, calculant le taux de cotisation
d'équilibre du système de retraite français par répartition sous les projections
démographiques Insee 2026 (Insee Première n°2108, 08/06/2026).

**Ce n'est PAS un modèle de projection des retraites au sens du COR.** Le COR
repose sur des microsimulations sur cas-types et carrières individuelles, qui ne
sont PAS reproduites ici. Ne jamais nommer cet objet « modèle de projection des
retraites ». Toujours dire « maquette comptable agrégée ».

La valeur ajoutée du projet est la **transparence et la reproductibilité**, pas
l'inédit. Le COR est un **benchmark de validation**, jamais un adversaire.

## 2. Équation fondamentale

    tau*(t) = [ R(t) / A(t) ] x [ Pbar(t) / Wbar(t) ]

- `R/A`  : ratio de dépendance ÉCONOMIQUE (retraités / cotisants)
- `P/W`  : pension moyenne relative (pension moyenne / salaire moyen)

## 3. Règles dures (non négociables)

1. **Aucune conclusion tant que les tests de calage ne passent pas.**
   Le code doit reproduire les chiffres officiels IP2108 (scénario central) :
   ratio 65+/20-64 = 40 (2026), 49 (2040), 62 (2070).
   Lancer `pytest tests/ -q` après chaque changement de logique.

2. **`config/hypotheses.yaml` est la source unique de vérité.**
   Tout paramètre vit là, sourcé et daté. Ne JAMAIS coder un nombre en dur
   dans `src/`. Si un paramètre manque, l'ajouter au YAML, pas au code.

3. **Tout `PLACEHOLDER` doit être remplacé par une valeur sourcée (COR/DREES)
   AVANT toute interprétation.** Un résultat calculé sur des PLACEHOLDER n'a
   aucune valeur scientifique et ne doit jamais être présenté comme un résultat.

4. **`data/raw/` est en lecture seule conceptuellement.** Les fichiers sources
   (Insee, COR, DREES) y sont déposés horodatés et JAMAIS modifiés. Tout
   traitement produit des fichiers dérivés ailleurs (`data/processed/`).

5. **Distinction projection / prédiction, partout.** Une projection
   conditionnelle (« si les tendances se prolongeaient ») n'est PAS une
   prédiction. L'exercice est « toutes choses égales par ailleurs » : il ignore
   volontairement ajustements comportementaux et réformes futures.

## 4. Décisions de cadrage (verrouillées)

- **Périmètre** : système entier, convention macro agrégée (esprit COR).
- **Problématique** : hybride « P2-cœur » — frontière d'iso-équilibre centrale ;
  seuil critique en lecture subordonnée ; sensibilité démographique en robustesse.
- **Scénarios Insee 2026** : central + fécondité basse (1,20) / haute (1,70)
  + migration basse (+70 000) / haute (+230 000).
- **Deux régimes d'indexation polaires** (incompatibles, traités séparément) :
  - Scénario L (législation constante) : indexation prix → P/W dérive à la baisse.
  - Scénario N (parité de niveau de vie) : P/W fixe (contrefactuel).
- **Le seuil 50 % est une LECTURE illustrative, pas la thèse.** Toujours présenter
  la sensibilité au seuil (45/50/55 %).

## 5. Validation

- Convergence cible avec le COR : **±0,5 point de PIB sur 2030-2040.**
  Un écart plus grand = signal de bug ou d'hypothèse divergente à identifier,
  pas un résultat à publier.
- Le calcul du ratio démographique est le test unitaire fondateur. S'il dévie,
  tout le reste est suspect.

## 6. Données : privilégier les sources stables

Pour un projet qui mise sur la reproductibilité, **une URL officielle vers un
fichier téléchargeable horodaté vaut toujours mieux qu'un scraper fragile.**
Éviter le scraping (risques de blocage type Cloudflare). Sources prioritaires :
xlsx de l'IP 2108, Insee Résultats compagnon, annexes COR en open data, panorama
DREES « Les retraités et les retraites ».

## 7. Style et langue

- Tout le rendu destiné au mémoire est en **français**, ton **neutre et
  quantitatif** (ce n'est pas un pamphlet ; les conclusions découlent des chiffres).
- Code commenté en français, noms de variables explicites.
- Citer systématiquement les sources (Insee, COR, DREES) avec millésime.

## 8. Boucle de travail recommandée

1. Modifier `hypotheses.yaml` ou `src/`
2. `pytest tests/ -q`
3. Vérifier le calage (40/49/62) avant toute interprétation
4. Commit git atomique avec message clair
5. Ne conclure qu'une fois PLACEHOLDER remplacés et tests verts

## 9. Commandes utiles

    pip install pyyaml pytest pandas matplotlib openpyxl
    python -m pytest tests/ -q          # tests de calage
    python src/maquette.py              # trajectoire v0
