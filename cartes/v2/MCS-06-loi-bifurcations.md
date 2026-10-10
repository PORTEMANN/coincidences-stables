# CARTE MCS-06 — Loi des bifurcations v2 : dérivabilité × complexité × type

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = questions classificatoires du tableau périodique ;
B = dérivabilité mesurée par discriminant dérivé (corpus).
**Attente honnête** : la loi des bifurcations (v2) est une conjecture
catégorie II du corpus. La carte la soumet à falsification complète.

---

## 1. Énoncé de la coïncidence candidate

Le corpus (bifurcations/, conjecture v2 datée) propose :

> Pour une bifurcation **physique** (instabilité de configuration), la
> dérivabilité décroît quand croît la complexité ; pour une bifurcation
> **conventionnelle** (choix de frontière de classement), la dérivabilité est
> libre quelle que soit la complexité.

La carte teste si cette séparation à deux axes tient sur un ensemble figé de
bifurcations, au-delà du hasard structurel, et survit aux déformations de 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| bifurcation | une question classificatoire du tableau périodique de la liste figée (section 4) |
| type | physique (instabilité de configuration) ou conventionnel (choix de classement) — déclaré par bifurcation, avant toute mesure |
| complexité | Z_eff = numéro atomique du point de bifurcation (proxy déclaré, mesuré comme insuffisant seul par le corpus — P-F3 réfutée ; utilisé ici comme composante déclarée, pas comme loi) |
| dérivabilité D | score de la batterie figée de la question (0 à 5), mesuré à l'exécution ou cité du corpus pour les verdicts déjà publiés |
| m (mesure) | m = −ρ_phys, où ρ_phys est la corrélation de Spearman (D, Z_eff) sur les bifurcations **physiques** seules (qualité croissante avec la décroissance de la dérivabilité) ; l'axe conventionnel n'entre pas dans m — il est testé en contrôle c3 |

## 3. Dictionnaire τ

    τ : bifurcations figées ↦ (type, Z_eff, D mesuré) ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Ensemble figé** : 20 bifurcations déclarées dans le runner (avec type et
  Z_eff), dont 5 déjà mesurées et publiées dans le corpus (P-He, P-LaLr,
  P-CrCu 3d, P-CrCu 4d, P-CrCu 5d — déclarées) et 15 nouvelles mesurées à
  l'exécution (déclarées : métalloïdes B/Si, tête des gaz nobles, H alcalin
  ou halogène, Zn/Cd/Hg bloc d, Be/Mg vs Ca, tête des lanthanides, coinage
  Cu/Ag/Au, et suites déclarées — liste exacte dans le runner). Composition :
  14 physiques + 6 conventionnelles.
- **Batterie figée** : 5 tests de propriétés dérivés par question (structure
  électronique mesurée vs règle dérivée), zéro paramètre ajusté.
- Aucune mesure nouvelle n'a servi à écrire la carte ; les 5 verdicts du
  corpus sont cités au regard ailleurs.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | Z_eff → Z_eff·(1+γ) (correction relativiste déclarée, γ = Z²/137²) | proxy de complexité |
| g2 | retrait des 5 verdicts du corpus (7 nouvelles seules) | dépendance au matériau publié |
| g3 | retrait de He (le point le plus extrême) | domination d'un point |
| g4 | seuil ρ : −0,7 → −0,6 | sensibilité au seuil |
| g5 | batterie 5 → 3 tests (sous-ensemble déclaré) | dépendance à la batterie |
| g6 | permutation des types (physique/conventionnel) | la loi tient-elle au type ? |

## 6. Modèle nul

- **N1 (types permutés)** : 10 000 permutations des étiquettes de type ;
  distribution de m.
- **N2 (D aléatoires)** : 10 000 ensembles de D uniformes sur {0..5} ;
  distribution de m.
- **N3 (ordre aléatoire)** : m sous permutation des Z_eff.

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | dérivabilités D permutées entre bifurcations physiques | m s'effondre vers N1 (|effet| ≥ 2 u) |
| c2 | D remplacés par leurs rangs retournés | ρ_phys s'inverse (|effet| ≥ 2 u) |
| c3 | axe conventionnel rapporté : |ρ_conv| doit rester < 0,5 | si |ρ_conv| ≥ 0,5 : la séparation v2 est réfutée (rapporté, pas un déclencheur CS0) |

c1 ou c2 vraiment muet → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 ; Σ = min sur {g1…g6}.
- Regard ailleurs : la loi est une conjecture catégorie II déjà publiée
  (v1 + addendum v2, P-F3 réfutée publiée). Seuil CS+ : **3,0** + correction :
  **3,1** (deux formes déjà écrites dans le corpus).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,1 | CS+ |
| 2 ≤ Σ < 3,1 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La loi a deux formes écrites (v1, v2) ; P-F3 réfutée (indice scalaire
impossible) ; 5 verdicts publiés du corpus inclus dans l'ensemble figé
(déclarés). La question mesurée par la carte — la séparation à deux axes
sous déformations — n'a pas été mesurée par le corpus.

## 11. Critères d'arrêt

- CS− ou CSi → la loi des bifurcations v2 est close comme correspondance
  mesurée (la conjecture reste une conjecture, étiquetée).
- CS0 → une seule refonte autorisée (MCS-06b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un ensemble synthétique de 20 bifurcations (14 physiques
plantées décroissantes, 6 conventionnelles libres), la statistique doit
résoudre c1 et c2 à |effet| ≥ 2 u et donner Σ ≥ 3,1 ; sur un ensemble sans
structure de type, CS− attendu. Si la démonstration montre que l'ensemble gelé
ne résout pas les contrôles, la carte n'est PAS scellée (la règle 1.2 fait
son office).

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 46f1c95083d8472b64779b6b7202a3fb15cc4c2ffb27737b1aba507657370ee8
HORODATAGE   : 2026-10-10T18:31:16Z
```
