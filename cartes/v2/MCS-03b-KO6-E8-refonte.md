# CARTE MCS-03b — KO-6 / triples spectraux ↔ 2I ⊂ E₈ (REFONTE UNIQUE)

**Statut** : REFONTE — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Refonte de** : MCS-03 (gelée 2026-10-09, ouverte au jalon 4 : **CS0**,
Σ = −1,95 — les trois contrôles muets : Spearman sur 15 paires quantile-
rangées ne résolvait pas les sabotages ponctuels ; suspension publiée).
**Moteur** : v2.0 (règle signe-robuste : un contrôle est muet si
|effet| < 2 u quelle que soit sa direction).
**Domaines** : A = géométrie non commutative (KO-6, A_F = ℂ ⊕ ℍ ⊕ M₃(ℂ)) ;
B = théorie des groupes (sous-groupes finis de SU(2), E₈).
**Attente honnête** : identique à MCS-03 : CS− attendu — la production
propre d'un CS− reste le succès de la carte. La refonte corrige la cécité,
pas la question : elle mesure la même correspondance avec une statistique
qui a du pouvoir.

---

## 1. Ce que la refonte change — et ne change pas

**Inchangé** : la correspondance candidate (un invariant combinatoire C
commun aux conditions KO-6 et à la chaîne 2I ⊂ E₈), les données
(énumérations mathématiques), les familles de comparaison, le verdict
attendu, les critères d'arrêt.

**Changé (l'opérateur)** : MCS-03 mesurait la corrélation de Spearman entre
les vecteurs C des deux familles **restreinte aux objets minimaux et
quantile-rangée** — 15 paires : aucun sabotage ponctuel n'y est lisible.
La refonte :

- énumère les familles **complètes** (toutes les algèbres réelles
  involutives de dimension ≤ 32 ; les groupes Z_n pour n = 2…120, les
  dihédraux binaires 2D_k pour k = 2…60, et 2T, 2O, 2I — ~180 groupes) ;
- la mesure m est la corrélation de Spearman sur l'appariement par rang
  quantile des familles complètes (≥ 150 paires — les sabotages y sont
  résolubles, voir la démonstration de puissance, règle 1.2).

## 2. Lexique gelé (identique à MCS-03, avec l'opérateur corrigé)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| triple KO-6 minimal | A_F = ℂ ⊕ ℍ ⊕ M₃(ℂ) avec les axiomes de Connes en KO-6 |
| chaîne icosienne | 2I ⊂ SU(2), |2I| = 120, plongement H₄ ⊂ E₈ (Moody–Patera) |
| invariant C | pour une algèbre finie A de dimensions d'irréductibles d_p : C(A) = nombre de couples (p, q), p ≤ q, avec d_p·d_q ≤ dim(A) et (p == q ou d_p == d_q) — la règle d'ordre 1 gelée de MCS-03, inchangée |
| famille ALG complète | toutes les algèbres réelles involutives de dimension ≤ 32 (énumération de MCS-03, code réutilisé) |
| famille GRP complète | Z_n (n = 2…120), 2D_k (k = 2…60), 2T, 2O, 2I |
| m (mesure) | Spearman sur l'appariement par rang quantile des vecteurs C des familles complètes |

## 3. Dictionnaire τ

    τ : conditions KO-6 ↦ C sur les algèbres finies réelles
        ↔ C sur les sous-groupes finis de SU(2)

τ est MCS-03 avec l'opérateur corrigé. Toute modification après le gel =
nouvelle carte, nouveau numéro.

## 4. Données et provenance

Identiques à MCS-03 (énumérations mathématiques exhaustives fixées par
référence ; le code publié de MCS-03 est réutilisé — empreinte consignée).
Aucun calcul nouveau n'a servi à écrire la refonte.

## 5. Groupe de déformations légitimes 𝒢 (inchangé)

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | E₈ → E₇ / E₆ | la coïncidence serait-elle « tout grand groupe marche » ? |
| g2 | 2I → Z₁₂₀ (même ordre) | comptage d'ordre pur ? |
| g3 | seuil de C : dim(A) → 2·dim(A) | fragilité à la convention |
| g4 | KO-6 → KO-2 | dimension mod 8 interchangeable ? |
| g5 | algèbres réelles → complexes | dépendance au corps |
| g6 | plongement H₄ ⊂ E₈ alternatif | unicité de la chaîne |

## 6. Modèle nul

- **N1 (algèbres aléatoires)** : 10 000 familles d'algèbres aléatoires de
  même distribution de dimensions ; distribution de m.
- **N2 (comptage d'ordre)** : la structure est détruite (identique à MCS-03).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | casser 2I → I (ordre 60) dans la chaîne | m doit chuter (|effet| ≥ 2 u) |
| c2 | intervertir les maxima de C entre familles | m doit chuter (|effet| ≥ 2 u) |
| c3 | retirer la règle d'ordre 1 de C | si m ne change pas : C est vide (|effet| ≥ 2 u attendu) |

Règle v2.0 : c1, c2 ou c3 vraiment muet (|effet| < 2 u, signe-robuste) →
**CS0** — et la refonte a échoué à réparer le banc (publié comme tel).

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,4** (gelé à MCS-03, conservé : la refonte n'ouvre pas le
  seuil). Seuil CS0 : règle v2.0 (signe-robuste).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,4 | CS+ (surprise majeure ; relecture externe exigée, gelé à MCS-03) |
| 2 ≤ Σ < 3,4 | CSp |
| −2 < Σ < 2 | **CS− — verdict attendu ; sa production propre est le succès** |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 — le banc est toujours aveugle |

## 10. Regard ailleurs (déclaration préalable de la refonte)

Regard de MCS-03 conservé (2 variantes enterrées ; 3 invariants candidats
avant C) **+ la suspension de MCS-03 elle-même (CS0, publiée)** : la
restriction aux objets minimaux est mesurée comme la cause de la cécité —
la refonte la retire, déclaré. C'est l'unique refonte autorisée : aucune
MCS-03c n'existera.

## 11. Critères d'arrêt

- CS− ou CSi : publication B3-FAIL, fermeture définitive de la ligne
  KO-6 ↔ E₈ dans le corpus (gelé à MCS-03, confirmé ici).
- CS0 : le banc reste aveugle après sa seule refonte — la ligne est close
  comme **inappréciable** par la machine (verdict plus fort qu'une
  suspension : publié comme tel).
- CS+ : réplication par un tiers exigée (gelé à MCS-03).

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur les familles complètes, la statistique doit résoudre les
trois contrôles à |effet| ≥ 2 u — la condition qui manquait à MCS-03.
Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : null
HORODATAGE   : null
```

---

## EPILOGUE (publié à la rédaction — la règle 1.2 a fait son office)

**La carte n'a pas été scellée** : la démonstration de puissance a échoué.
Sur les familles complètes (346 algèbres, 181 groupes), les trois contrôles
restent muets : c1 = 0,00 u ; c2 = 0,15 u ; c3 = −1,69 u. L'opérateur
alternatif par ancres (min-quantile de C(A_F) et C(2I) dans leurs familles),
exploré et consigné, échoue aussi (c1 = 0,16 u) — et révèle pire : les ancres
ne sont même pas en tête de leurs familles (19e et 8e percentiles) :
l'énoncé « les mêmes contraintes sélectionnent les deux » est faux dans le
matériau. La suspension MCS-03 (CS0) devient une **clôture par
inappréciable** : la ligne KO-6 ↔ E₈ n'est ni confirmable ni réfutable par
la machine sur ce matériau. Journal : `journal/JALON-MCS03B.jsonl`.
