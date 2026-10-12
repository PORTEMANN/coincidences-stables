# CARTE MCS-24 — Tarif de Bekenstein-Hawking × le porteur réparé (nul réel)

**Statut** : CANDIDAT — Jalon 1 v2 (rédaction, aucun calcul de mesure)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = la densité d'entropie des horizons η = 1/(4ℏG)
(Bekenstein-Hawking ; constantes CODATA déjà dans la maison — MCS-08/16,
déclaré) ; B = le contenu spectral RÉPARÉ du corpus : le porteur
PORTEUR-KO6-A3b-DIM5 (T5/T6 : mesuré, certifié) — N_F = dim H_F = 5, le
plus proche entier du N_req = 3π/2 de la chaîne gelée.
**Attente honnête** : la leçon de MCS-23 est déclarée : une question à un
nombre avec cadran (f₂, Λ) a un plafond de pouvoir — mais le nul est
cette fois l'espace RÉEL des triplets vérifiés du banc (pas la fenêtre de
proxys), dont la distribution de tailles est mesurée et dominée par les
grandes tailles ; le porteur assoit le plus proche entier. Attente :
CSp possible, plafond mesuré à la démo.
**Regard ailleurs (déclaration préalable)** : MCS-23 (non scellée) est lue
et déclarée — la présente carte n'est PAS une itération : le contenu est
nouveau (réparé : T5 a changé l'objet) et le nul est nouveau (réel) ;
l'erratum du dépôt spectral-triple-minimality et les chantiers T5–T11
sont lus et déclarés. La relation structurelle (1/G_ind ∝ f₂Λ²N_eff — un
cadran toujours ajustable) est déclarée : la carte mesure
l'exceptionnalité à cadran gelé, pas une loi.

---

## 1. Énoncé de la coïncidence candidate

> Le contenu mesuré du porteur réparé (N_F = 5) assoit le tarif des
> horizons η = 1/(4ℏG) à cadran gelé (chaîne MCS-23 : 1/G_ind =
> (2/3π)·N_eff·f₂·Λ², f₂ = 1, Λ = M_P non réduite) **plus près** que les
> contenus réels de même fenêtre — l'espace des triplets nus vérifiés du
> banc — et cette proximité survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| contenu | un triplet nu vérifié du banc (T5, machine des orbites) de taille n ∈ [2 ; 7] (fenêtre déclarée — mesurée dans le corpus par T1) ; N_eff = n |
| chaîne du tarif | celle de MCS-23, citée gelée : 1/G_ind = (2/3π)·N_eff·f₂·Λ² ; f₂ = 1 ; Λ = M_P = 1,2209×10¹⁹ GeV (non réduite, canonique) ; N_req = 3π/2 ≈ 4,712 |
| écart | δ = log₁₀(N_eff/N_req) (signé) |
| m (mesure) | m = −|δ| (qualité croissante avec la proximité du tarif) |
| nul réel | la distribution de δ sur les triplets nus vérifiés de la fenêtre, PONDÉRÉE par le compte mesuré de chaque taille (la mesure naturelle de l'espace — déclarée) |

## 3. Dictionnaire τ

    τ : triplet nu vérifié ↦ sa taille ↦ l'écart au tarif ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Constantes** : G_N (CODATA 2022, fichier donnees/mcs08_allascii_2022.txt
  déjà acquis — MCS-08/16, empreintes reconsignées au runner) ; M_P gelée
  dans le runner (convention déclarée).
- **Contenu déclaré du corpus** : le porteur réparé (N_F = 5 — mesuré aux
  verdicts T5/T6/T7, déclaré) ; triplet vérifié C4 (N_F = 4 — erratum
  du dépôt, déclaré).
- **Nul** : comptes de triplets nus vérifiés par taille, calculés par la
  machine des orbites de T5 (filiation déclarée), fenêtre
  n ∈ [2 ; 7] — calculés à l'exécution (déclaré), jamais avant le gel.
- Aucune acquisition externe nouvelle.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | Λ = M_P → M̄_P = M_P/√(8π) (réduite) | dépendance à la convention de cadran |
| g2 | G_N CODATA 2022 → 2018 | dépendance à l'édition |
| g3 | fenêtre du nul n ≤ 7 → n ≤ 8 | dépendance à la fenêtre |
| g4 | contenu porteur (N_F = 5) → triplet vérifié C4 (N_F = 4 — l'autre contenu réel du corpus) | dépendance au contenu déclaré |
| g5 | le porteur amputé de son nœud ℂ (N_F = 4, déclaré — le nœud M₂ seul) | sensibilité au nœud spectateur |
| g6 | pondération du nul : par comptes mesurés → uniforme par taille | dépendance à la mesure du nul |

## 6. Modèle nul

- **N1 (le nul réel)** : la distribution de δ sur les triplets nus vérifiés
  de la fenêtre, pondérée par les comptes mesurés ; μ_null, u exacts
  (calculés, pas tirés).
- **N2 (tailles permutées)** : les tailles de la fenêtre permutées entre
  contenus (rapporté — documenté).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | contenu déplacé : N_F × 8 (déclaré) | m se dégrade (|effet| ≥ 2 u) |
| c2 | contenu remplacé par une taille tirée du nul pondéré (PRNG public ChaCha20) | m tombe vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée sur ce domaine).
- Diagnostics rapportés (hors Σ) : δ canonique en dex ; le rang du porteur
  dans le nul réel (p = fraction au moins aussi proche) ; les comptes du
  nul par taille — publiés.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — le porteur réparé encaisse au bon taux, au-delà du nul réel |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — la proximité était combinatoire |
| Σ ≤ −2 | CSi — le hasard de la fenêtre fait mieux |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

MCS-23 (non scellée) lue et déclarée — sa leçon est dans la conception de
la présente carte (nul réel au lieu de proxys) sans être une itération :
le contenu a changé (réparation T5) et le nul a changé (réel). Les
verdicts T5–T11 du corpus sont lus et déclarés. La structure du cadran
(f₂, Λ toujours ajustables) est déclarée : la carte mesure
l'exceptionnalité à cadran gelé. Aucun calcul du nul réel n'a été fait
avant cette carte.

## 11. Critères d'arrêt

- CS+ → le porteur réparé est exceptionnellement au tarif ; le diagnostic
  publie son rang dans le nul réel.
- CS− ou CSi → B3-FAIL publié : la proximité était combinatoire — la
  question du tarif attend une loi sans cadran ou une seconde ancre
  mesurée (déclaré comme frontière du programme).
- CS0 → une seule refonte autorisée (MCS-24b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un contenu synthétique planté au plus proche entier du
tarif (N_F = 5), la statistique doit donner Σ ≥ 3,0 et les deux contrôles
résoudre à |effet| ≥ 2 u ; sur une taille tirée du nul, CS− attendu ;
banc aveugle simulé → CS0. Hachée dans l'acte de gel. Le nul de la démo
est le nul réel calculé (fenêtre n ≤ 7 — la démo mesure la puissance sur
l'espace réel, déclaré).

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 5ab3ca699aa49ca21047726b656a47e1c586d2c94c48c48eb61de194085bb1db
HORODATAGE   : 2026-10-12T09:35:17Z
```
