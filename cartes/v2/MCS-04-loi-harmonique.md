# CARTE MCS-04 — Loi harmonique du zoo particulaire × masses mesurées

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = masses des particules (PDG) ; B = tempérament égal
(échelle musicale, δ = 2^{1/12}).
**Attente honnête** : carte mixte attendue — le corpus a déjà pesé la loi par
contact (mvcg, tiroir LOI-HARMONIQUE : S+ sur μ, Z, charm ; P sur up, strange,
bottom). La carte teste autre chose : la **stabilité globale** de la
correspondance sous déformations, pas les pesées locales.

---

## 1. Énoncé de la coïncidence candidate

Le corpus propose une loi harmonique sur le zoo particulaire :

    m_n = m_p · δ^n,    δ = 2^{1/12}

c'est-à-dire que les rapports de masses tombent sur le réseau du tempérament
égal (douze demi-tons par octave). La carte teste si les masses mesurées du
zoo se placent sur ce réseau **au-delà de ce que produit le hasard structurel**,
et si cette éventuelle stabilité survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| zoo | la liste figée des particules de la carte (section 4) : masses PDG 2024 |
| indice harmonique | n(m) = 12·log₂(m / m_p) pour une masse m du zoo |
| résidu | r(m) = n(m) − round(n(m)) (distance signée au demi-ton le plus proche, en demi-tons) |
| m (mesure) | −log₁₀( RMS(r) ) sur le zoo de la configuration, qualité croissante avec la précision |
| nul de complexité égale | loi à 0 paramètre : réseau δ' fixé a priori sans réajustement |
| réseau décalé | même δ, phases décalées d'un demi demi-ton (contrôle c1) |

## 3. Dictionnaire τ

    τ : masses du zoo (PDG 2024) ↦ indices harmoniques n(m) ↦ résidus au réseau δ

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro, nouveau regard ailleurs.

## 4. Données et provenance (gelées)

- **Masses** : table PDG 2024 (Live, figée datée dans le runner avec son
  empreinte) — liste du zoo dans le runner (particules à masses mesurées :
  leptons e/μ/τ, quarks u/d/s/c/b/t, bosons W/Z/H, proton, neutron) ;
  m_p = masse du proton PDG 2024.
- **Contre-données** : PDG 2022 (déformation g3) — mêmes particules.
- Aucune donnée de test n'a servi à écrire la candidate (anti-circularité,
  manifeste §8). La loi est écrite dans le corpus depuis des années ;
  son transport aux masses est déclaré au regard ailleurs (section 10).

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | ancre m_p → m_e | dépendance à l'ancre |
| g2 | retrait des quarks (leptons + bosons + nucléons seuls) | la loi tient-elle hors des quarks ? |
| g3 | PDG 2024 → PDG 2022 | dépendance à la version de la table |
| g4 | retrait des bosons | secteurs |
| g5 | δ = 2^{1/12} → δ' ∈ {2^{1/11}, 2^{1/13}} | dépendance au pas du réseau |
| g6 | retrait d'une particule au hasard (amorti par PRNG public) | sensibilité locale |

## 6. Modèle nul

- **N1 (réseau aléatoire)** : 10 000 réseaux δ' tirés uniformément dans
  [2^{1/13}, 2^{1/11}] ; distribution de m sur le zoo réel → μ_null, u.
- **N2 (masses aléatoires)** : 10 000 zoos de masses uniformes en log sur
  [m_e, m_t] ; m du réseau δ sur chacun → distribution nulle.
- **N3 (permutation)** : permutation des masses entre particules, 10 000 fois.

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | réseau décalé d'un demi demi-ton (phase +1/24 d'octave) | dégradation forte de m (|effet| ≥ 2 u attendu) |
| c2 | masses remplacées par un bruit log-uniforme déclaré | m s'effondre vers N2 |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g.
- Σ = min sur {g1…g6}.
- Regard ailleurs : la loi a déjà été pesée par contact dans mvcg
  (LOI-HARMONIQUE : 15 contacts, S+ sur μ/Z/charm, P sur quarks, dettes
  nommées — publié). Cette carte est un opérateur différent (Σ sous
  déformations), déclaré. Seuil CS+ : 3,0 + correction regard ailleurs :
  seuil porté à **3,1** (une famille de formes déjà éprouvée dans le corpus).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,1 | CS+ (surprise ; publication avec relecture externe) |
| 2 ≤ Σ < 3,1 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet (|effet| < 2 u) | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La loi m = m_p·2^{n/12} est la candidate centrale du corpus depuis le tiroir
LOI-HARMONIQUE de mvcg (déjà pesée par contact : verdicts mixtes publiés —
S+ sur μ, Z, charm ; P sur up, strange, bottom ; dettes nommées). Cette
carte-ci est une mesure **globale sous déformations** — opérateur distinct.
Familles essayées avant gel : 1 (celle-ci). Sous-ensembles examinés avant
gel : les pesées mvcg par contact (déclarées).

## 11. Critères d'arrêt

- CS− ou CSi → carte fermée, publication B3-FAIL ; la loi harmonique comme
  correspondance globale est close (les pesées locales de mvcg restent ce
  qu'elles sont).
- CS0 → une seule refonte autorisée (MCS-04b), nouveau regard ailleurs déclaré.
- CSp → aucune revendication ; la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un zoo **synthétique** planté sur le réseau (masses tirées sur
δ^n exactement à 0,1 % près), la statistique doit donner Σ ≥ 3,1 et les deux
contrôles doivent résoudre à |effet| ≥ 2 u ; sur un zoo synthétique hors
réseau (log-uniforme), CS− attendu ; banc aveugle simulé → CS0. Hachée dans
l'acte de scellement.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 3cda0e155f11451263ee8ec1f7f1a9cd84c617e6a0e4eedc6a15b91b445b10b9
HORODATAGE   : 2026-10-10T18:31:16Z
```
