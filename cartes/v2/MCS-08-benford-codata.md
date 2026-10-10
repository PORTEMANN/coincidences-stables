# CARTE MCS-08 — Loi de Benford × constantes physiques (CODATA)

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = constantes physiques (table CODATA, valeurs mesurées et
ajustées) ; B = loi de Benford (premier chiffre significatif,
p(d) = log₁₀(1 + 1/d), d = 1…9).
**Attente honnête** : **CS+ attendu**. Cette carte est la cible de calibration
de la machine (cf. CARTE-SEMANTIQUE-VERDICTS §domaines) : la loi de Benford
est établie empiriquement pour les tables de grandeurs physiques hétérogènes.
Si la machine ne la retrouve pas, la machine est aveugle — ce verdict-là aussi
serait publié. Aucune famille de ce domaine n'a été éprouvée dans le corpus :
aucun regard ailleurs à payer, seuil de base 3,0.

---

## 1. Énoncé de la coïncidence candidate

> La distribution des premiers chiffres significatifs des valeurs de la table
> CODATA suit la loi de Benford, au-delà du hasard structurel, et cette
> conformité survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| table | la table CODATA « toutes constantes » (édition figée, section 4) : une ligne = une grandeur, sa valeur numérique |
| premier chiffre | premier chiffre significatif de |valeur| (1…9 ; les valeurs nulles, s'il en existe, sont exclues et comptées) |
| p_obs | distribution empirique des premiers chiffres sur la table de la configuration |
| p_Ben | p_Ben(d) = log₁₀(1 + 1/d) |
| m (mesure) | m = −Σ_d |p_obs(d) − p_Ben(d)| (distance L1, signée : qualité croissante avec la conformité) |
| nul de complexité égale | loi plate : p(d) = 1/9 — même nombre de paramètres ajustés (zéro) |

## 3. Dictionnaire τ

    τ : table de constantes ↦ premiers chiffres significatifs ↦ m

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro.

## 4. Données et provenance (gelées)

- **CODATA 2022** : table ascii « all constants » (NIST,
  physics.nist.gov/cuu/Constants) — acquisition à l'ouverture, empreinte
  sha256 consignée au journal. Aucune ligne n'a été lue avant la rédaction.
- **Contre-données** : CODATA 2018, même format (déformation g1).
- La loi de Benford est publique et antérieure ; son transport aux tables
  CODATA est le contact testé ici — jamais mesuré par la machine ni le corpus.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | CODATA 2022 → CODATA 2018 | dépendance à l'édition de l'ajustement |
| g2 | retrait des constantes de définition exacte du SI 2019 (c, h, e, k, N_A, K_cd, Δν_Cs et grandeurs qui en découlent par définition — liste écrite dans le runner avant lecture de la table) | les chiffres « décidés » ne portent pas la loi |
| g3 | multiplication de toutes les valeurs par un facteur non décimal déclaré (conversion J → eV : 1 / 1,602176634e-19, exacte) | invariance d'échelle (hors puissances de 10) |
| g4 | base 10 → base 12 (p_Ben généralisée : log₁₂(1+1/d), d = 1…11) | la loi est-elle celle de la base ou du monde ? |
| g5 | une entrée sur deux (rang pair dans l'ordre de la table, déclaré) | dépendance à la densité d'échantillonnage |
| g6 | retrait d'une entrée au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (loi plate)** : 10 000 tables de même effectif dont les premiers
  chiffres sont tirés uniformément sur 1…9 ; distribution de m → μ_null, u.
- **N2 (mantisses permutées)** : permutation des premiers chiffres entre
  entrées de la table réelle, 10 000 fois (rapporté ; conserve la distribution
  observée — teste l'assignation, pas la loi).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | décalage cyclique des chiffres (d → d mod 9 + 1) sur la table réelle | m s'effondre vers N1 (|effet| ≥ 2 u) |
| c2 | table remplacée par des mantisses uniformes déclarées (chiffres plats) | m s'effondre vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée — seuil de base du moteur).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — premier CS+ de la machine ; la calibration réussit |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — et la machine est aveugle à une loi vraie |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Aucune famille essayée dans le corpus sur ce domaine. La loi de Benford est
connue ; l'objet de la carte n'est pas la découverte mais la **calibration**
de l'opérateur MCS sur une régularité vraie. Tables examinées avant gel : 0.

## 11. Critères d'arrêt

- CS+ → la machine a un étalon positif ; publié comme tel (calibration,
  pas découverte).
- CS− ou CSi → carte fermée (B3-FAIL) et **alarme méthodologique** publiée :
  toute la cartographie des fermetures perd sa valeur discriminante tant
  qu'aucune régularité vraie n'est retrouvée.
- CS0 → une seule refonte autorisée (MCS-08b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur une table synthétique de 300 grandeurs à mantisses tirées
selon Benford exact, la statistique doit donner Σ ≥ 3,0 et les deux contrôles
résoudre à |effet| ≥ 2 u ; sur une table à chiffres plats, CS− attendu ;
banc aveugle simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : ed656aa4e013bc7af8f1238314c4308cda70e4b226b9bae93f67ae485562d795
HORODATAGE   : 2026-10-10T20:25:35Z
```
