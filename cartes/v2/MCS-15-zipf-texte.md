# CARTE MCS-15 — Loi de Zipf × fréquences de mots (étalon de calibration II)

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = fréquences de mots dans un texte long (Project Gutenberg,
fichiers figés) ; B = la loi de Zipf **figée** : f(r) = f_tot / (H_k · r),
k = taille du vocabulaire de la configuration, exposant α = 1, **aucun
paramètre ajusté**.
**Attente honnête** : **CS+ attendu** — seconde cible de calibration de la
machine (cf. MCS-08, étalon Benford). La loi de Zipf est la régularité
empirique la plus célèbre de la linguistique quantitative ; la leçon de
MCS-14 est déclarée : une loi de rang **mal figée** meurt (Zipf α = 1 sur
les groupes d'espace : CSi) — ici la loi figée est dans son domaine
historique. Si la machine ne la retrouve pas, elle est aveugle — ce
verdict-là aussi serait publié. La fenêtre est complète (tous les rangs,
hapax compris — la déformation testera le cœur seul).

---

## 1. Énoncé de la coïncidence candidate

> Les fréquences des mots d'un texte long suivent la loi de rang figée
> f(r) = f_tot / (H_k · r) **au-delà de ce que produit le hasard structurel**
> (partitions uniformes des mêmes tokens dans le même vocabulaire), et cette
> forme survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| token | une occurrence de mot (suite de lettres, casse rabattue en canonique, apostrophes coupées — tokenisation déclarée) |
| vocabulaire | les k formes distinctes de la configuration |
| rang r | rang du mot par fréquence décroissante (1 = le plus fréquent) |
| loi figée | f_zipf(r) = f_tot / (H_k · r), H_k = Σ_{r=1..k} 1/r |
| écart | ε(r) = log₁₀(f_obs(r) + 1) − log₁₀(f_zipf(r) + 1) (le +1 est gelé) |
| m (mesure) | m = −log₁₀( RMS(ε) ) sur les k rangs |

## 3. Dictionnaire τ

    τ : texte ↦ tokens ↦ fréquences ↦ rangs ↦ m

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro.

## 4. Données et provenance (gelées)

- **Canonique** : Victor Hugo, *Les Misérables* (Project Gutenberg #135,
  fichier texte figé, français) — acquisition à l'ouverture, empreinte
  consignée. Aucune ligne lue avant la rédaction.
- **Contre-textes** : Victor Hugo, *Notre-Dame de Paris* (Gutenberg #2610,
  g1) ; Charles Dickens, *A Tale of Two Cities* (Gutenberg #98, anglais, g2).
  Si un identifiant ne correspond pas au texte déclaré, la substitution est
  vérifiée par le contenu et consignée.
- La loi de Zipf est publique et antérieure ; son transport à ces trois
  textes n'a jamais été mesuré par la machine.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | *Les Misérables* → *Notre-Dame de Paris* (même auteur) | dépendance au texte |
| g2 | français → anglais (*A Tale of Two Cities*) | dépendance à la langue |
| g3 | retrait des 10 mots de tête (mots-outils) | domination des rangs extrêmes |
| g4 | fenêtre déclarée : 1 000 premiers rangs seuls | cœur vs queue de distribution |
| g5 | exposant figé α = 1 → α = 1,1 (déclaré) | dépendance à l'exposant |
| g6 | casse non rabattue (majuscules distinctes, déclaré) | dépendance à la tokenisation |

## 6. Modèle nul

- **N1 (partitions uniformes)** : 10 000 partitions du même nombre de
  tokens dans le même vocabulaire (k cases uniformes) ; rangs recomputés,
  m recomputé → μ_null, u. (Nul de complexité égale : aucune loi, même
  nombre de tokens, même vocabulaire.)
- **N2 (rangs permutés)** : permutation des fréquences entre mots, 10 000
  fois (rapporté ; identité sur la loi de rang — documenté comme tel, il
  teste que la mesure est bien rang-ordonnée).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | rangs inversés (tri croissant : le hapax pris pour rang 1) | m s'effondre (|effet| ≥ 2 u) |
| c2 | tokens remplacés par un tirage uniforme du vocabulaire (partition déclarée) | m s'effondre vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (calibration, aucune famille éprouvée sur ce domaine
  par la machine — MCS-14 était une autre loi, un autre domaine).
- Diagnostics rapportés (hors Σ) : exposant α ajusté (hors mesure) pour
  chaque texte ; les 20 mots de tête avec leurs fréquences.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — second étalon réussi ; la machine reconnaît la loi dans son domaine |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — et la machine est aveugle à Zipf sur du texte |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Zipf n'a jamais été éprouvé par la machine sur du texte. Leçon déclarée de
MCS-14 (CSi, publié) : la même forme figée sur un autre domaine est morte
— la présente carte dit si la machine distingue le domaine où la loi vit
du domaine où elle meurt. Textes consultés avant gel : 0.

## 11. Critères d'arrêt

- CS+ → second étalon de calibration validé ; publié comme tel
  (calibration, pas découverte).
- CS− ou CSi → carte fermée (B3-FAIL) et **alarme méthodologique** publiée
  (la machine ne retrouve pas une régularité établie sur son propre terrain).
- CS0 → une seule refonte autorisée (MCS-15b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un texte synthétique planté sur la loi figée (α = 1 exact,
bruit 5 %, vocabulaire 30 000), la statistique doit donner Σ ≥ 3,0 et les
deux contrôles résoudre à |effet| ≥ 2 u ; sur une partition uniforme, CS−
attendu ; banc aveugle simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 8a718192f90de4f1072bb1e89e8e02934d34a3bd3f8e5d224a319d725c809f85
HORODATAGE   : 2026-10-11T12:39:10Z
```
