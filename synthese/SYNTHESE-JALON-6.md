# La Machine à Coïncidences Stables : douze verdicts, et ce qu'elle a mesuré du monde — et d'elle-même

**Synthèse publique — jalon 6 (11 octobre 2026)**
*Patrice Portemann, rédaction assistée. Tout ce qui est affirmé ici est
vérifiable : le dépôt public (github.com/PORTEMANN/coincidences-stables)
contient les cartes scellées, les actes de gel, les codes, les données
empreintées, les journaux chaînés et les résultats de chaque exécution.*

---

## 1. La question que la machine pose

Le monde regorge de coïncidences numériques. La constante de structure fine
vaut presque 1/137. Les masses des leptons vérifient une étrange formule au
tiers près. Les planètes suivent à peu près une progression géométrique. La
question n'est pas de savoir si ces coïncidences existent — elles existent.
La question est : **sont-elles stables** ? Tiennent-elles quand on change
l'édition des tables, l'unité, le sous-échantillon, la convention ? Ou
sont-elles des artefacts de la manière dont on les regarde ?

La Machine à Coïncidences Stables (MCS) est un opérateur qui répond à cette
question — et seulement à celle-là. Elle n'explique rien, ne découvre rien,
ne répare rien. Elle prend une correspondance candidate, écrite **avant** que
les données ne soient lues, et lui fait subir un groupe de déformations
légitimes. Si la correspondance survit à toutes les déformations au-delà du
hasard structurel, elle est déclarée stable (CS+). Sinon, elle est fermée
(CS−), inversée (CSi), suspendue pour impuissance du test (CS0), ou endormie
(CSp — mieux que le hasard, pas assez pour être stable).

## 2. Le protocole, en quatre gestes

Chaque carte (une correspondance candidate) suit le même chemin, sans
exception :

1. **Rédaction** — la carte est écrite entièrement *avant* toute lecture des
   données : la mesure, les déformations, les modèles nuls, les contrôles
   positifs (sabotages que le test doit savoir détecter), les seuils, les
   critères d'arrêt. L'attente honnête est déclarée.
2. **Démonstration de puissance** (règle 1.2) — sur des données
   *synthétiques* à vérité connue, la statistique doit prouver qu'elle sait
   voir : retrouver un signal planté, résoudre ses sabotages à 2 unités de
   nul. Une carte dont la statistique est aveugle n'est pas scellée.
3. **Gel** — la carte est scellée par empreinte SHA-256 sur son contenu
   pré-gel, dans un acte public chaîné aux actes précédents. Après le gel,
   plus personne — pas même l'opérateur — ne peut la modifier.
4. **Ouverture unique** — acquisition publique consignée, code figé et haché
   avant exécution, **une seule exécution**, verdict publié quel qu'il soit.
   Le hasard nécessaire (permutations, surrogates) vient d'un PRNG public
   dérivé des empreintes : toute personne peut rejouer chaque tirage.

Tout est chaîné : chaque journal est append-only, chaque record haché avec
le hachage du précédent, chaque campagne relie sa genèse à la tête de la
précédente. On ne peut rien effacer sans que la rupture soit visible.

## 3. Douze cartes

### Première campagne (v0.1, figée) — la machine apprend en tuant

| Carte | Correspondance | Verdict |
|-------|----------------|---------|
| MCS-01 | loi kZ × masses nucléaires (AME) | **CSi** — Σ = −6,93 : inversion stable |
| MCS-02 | invariants ASH × signaux (EEG, ECG, cellules, roulements) | **CSi** — Σ = −25,10 : inversion stable |
| MCS-03 | KO6/E8 × groupes finis de SU(2) | **CS0** — test impuissant (matériau insuffisant) |

Deux inversions : dans ces domaines, la réalité fait *pire* que le hasard —
les correspondances proposées ne sont pas seulement fausses, elles sont
anti-stables. Et un premier CS0 : la machine a refusé de trancher faute de
pouvoir. Cette campagne a révélé un défaut du moteur v0.1 (un contrôle
positif « muet » par convention de signe) — corrigé dans la v2.0, scellée à
son tour.

### Seconde campagne (v2.0) — les correspondances du corpus lui-même

| Carte | Correspondance | Verdict |
|-------|----------------|---------|
| MCS-04 | zoo particulaire × tempérament égal (2^{1/12}) | **CS−** — mieux que le hasard, non spécifique au pas près |
| MCS-05 | agrégation centroïde EEG (imagerie motrice) | **CS0** — mesure sous le nul, test impuissant |
| MCS-06 | loi des bifurcations v2 (dérivabilité × complexité) | **CS−** — tendance vraie, sous le seuil |
| MCS-07 | économie de l'information (frontière r₁₂ × succès) | **CS−** — portée par les points-frontière eux-mêmes |

Quatre fermetures ou suspensions, chacune instructive : la loi harmonique
n'est pas une coïncidence *globale* (les pesées locales du corpus restent
ce qu'elles sont) ; l'EEG est fermé une quatrième fois ; la loi des
bifurcations montre une tendance réelle mais insuffisante ; et l'inversion
mesurée à la frontière r₁₂ ne généralise pas hors de ses propres témoins.

### La calibration — la preuve que la machine sait dire oui

| Carte | Correspondance | Verdict |
|-------|----------------|---------|
| MCS-08 | loi de Benford × constantes CODATA | **CS+** — Σ = 5,24 |

Une régularité *connue vraie*, soumise au même protocole : la machine la
retrouve, sous toutes les déformations — y compris en **base 12**, ce qui
prouve que la loi détectée est celle du monde, pas de la notation. Ce CS+
est un étalon : sans lui, les fermetures ne prouvaient rien — peut-être la
machine était-elle simplement aveugle. Désormais, chaque CS− a une valeur
discriminante démontrée.

### Les lois historiques et contemporaines

| Carte | Correspondance | Verdict |
|-------|----------------|---------|
| MCS-09 | Titius-Bode (1772, figée) × demi-grands axes | **CSp** — Σ = 2,40 : la carte dort |
| MCS-10 | relation d'accélération radiale × 175 galaxies SPARC | **CS+** — Σ = 19,28 |
| MCS-11 | formule de Koide (1982, figée) × leptons chargés | **CS+** — Σ = 10,64 |
| MCS-12 | BBN à un paramètre × quatre éléments légers | **CSp** — Σ = 2,08 : la carte dort |

Trois issues exemplaires :

- **Titius-Bode** : la loi de 1772, jamais réajustée, bat les séquences
  aléatoires sous toutes les déformations — sans atteindre le seuil. Le
  diagnostic de cohortes raconte l'histoire exacte : 3,3 % d'écart sur le
  monde connu en 1772, 27 % sur les découvertes ultérieures (Uranus et
  Cérès prédites, Neptune et Pluton rompues). Une curiosité mesurée, pas
  une loi.
- **RAR** : la première confirmation non triviale. La relation
  d'accélération radiale est extraordinairement stable (Σ = 19,28) — et le
  diagnostic gelé mesure en même temps son envers : sur la composante
  gazeuse, la seule cinématographiquement indépendante, la relation meurt.
  La machine dit les deux choses à la fois, publiquement.
- **Koide** : la plus étrange. La formule de 1982 vaut 2/3 à 3,3
  millionièmes près, stable sous deux autorités de mesure, quatre éditions,
  les incertitudes et les unités. Un triplet hiérarchique aléatoire
  n'approche jamais 2/3 à cette précision. La machine mesure
  « exceptionnel » — et refuse de dire « vrai » : la formule a été trouvée
  sur ces trois masses (circularité payée au seuil), n = 3, et aucune
  explication n'est revendiquée.
- **BBN** : trois accords superbes (deutérium à 0,002 dex, hélium-4 à
  0,004, hélium-3 à 0,04) et une rupture mesurée — le lithium, à 0,468 dex,
  publié au diagnostic. Sans le lithium, la carte vole (z = 7,2) ; avec lui,
  elle dort. La structure exacte du « problème du lithium » : une tension
  par élément, pas un effondrement.

## 4. Ce que la carte du monde dit, à douze points

1. Les correspondances numériques précises entre domaines éloignés meurent
   presque toutes au même endroit : la déformation qui change l'échelle, le
   pas ou l'ancre. Le monde contient des régularités grossières — des
   réseaux précis cachés, non, dans ce qui a été testé.
2. Il existe de vraies coïncidences stables : une loi de distribution de
   chiffres (Benford), une relation dynamique des galaxies (RAR), une
   formule rationnelle inexpliquée (Koide). Elles ne se ressemblent pas ;
   la machine les reconnaît toutes.
3. Entre confirmer et fermer, il y a *dormir* : Titius-Bode et la BBN sont
   meilleures que le hasard et insuffisantes pour être stables — mesurées,
   publiées, ni revendiquées ni enterrées.
4. Les frontières les plus instructives trouvées à ce jour sont internes :
   la limite du dérivable (r₁₂), la non-indépendance cinématique de la RAR,
   la fragilité n = 3 de Koide. La machine éclaire d'abord les limites —
   siennes et celles des lois qu'elle éprouve.

## 5. Ce que la machine a mesuré d'elle-même

L'honnêteté du dispositif n'est pas affirmée, elle est documentée :

- **deux CS0 informatifs** (MCS-03, MCS-05) : la machine a refusé de
  trancher quand le test ne pouvait pas voir — le second détecté par la
  règle signe-robuste de la v2.0, là où la v0.1 aurait rendu un faux verdict ;
- **un défaut de conception publié** (MCS-06) : la carte scellée incluait
  un tirage du nul dans son propre minimum — exécuté tel quel, publié tel
  quel, la leçon est inscrite dans la règle 1.2 pour les cartes futures ;
- **un erratum invalidant une exécution** (MCS-09) : un identifiant
  d'empreinte mal recopié rendait les tirages du PRNG public irrejouables —
  exécution invalidée, code corrigé, ré-exécution unique, verdict identique,
  tout est dans le journal chaîné ;
- **cinq corrections de parsing consignées** (MCS-05, MCS-10, MCS-11) :
  chacune avant résultat, chacune un record du journal — on ne verra jamais
  une correction après coup : la chaîne l'interdit ;
- **trois déviations d'acquisition déclarées** (JPL SSD injoignable pour
  MCS-09 ; la revue PDG n'adoptant pas de valeur ³He pour MCS-12 ;
  les prédictions BBN lues dans la source citée de la revue).

## 6. Ce que la machine ne fait pas

Elle ne découvre pas : toute loi testée est écrite avant les données, par
quelqu'un d'autre ou par le corpus. Elle n'interprète pas : le statut
physique de la RAR (MOND, matière noire, tautologie), la signification de
la formule de Koide, l'origine du problème du lithium sont hors de sa
portée — elle le dit, à chaque fois, dans le verdict. Elle ne répare pas :
une carte fermée est définitive ; une carte suspendue n'a droit qu'à une
seule refonte, déclarée. Son utilité est ailleurs : elle sépare, avec un
protocole public et rejouable, ce qui tient de ce qui ne tient pas — et
elle le prouve en publiant ses propres échecs avec les mêmes empreintes que
ses réussites.

## 7. La suite

Le registre des candidats reste ouvert : résonances orbitales des systèmes
planétaires multiples (données NASA Exoplanet Archive), distribution des
groupes d'espace cristallographiques (COD), loi de Zipf comme second étalon
de calibration, refontes uniques autorisées pour MCS-03b et MCS-05b. Chaque
carte future ajoutera un point à la cartographie sémantique — jamais ne
révisera un point existant.

---

*Jalon 6 — synthèse publique. Cet article ne mesure rien de nouveau ; il
lit douze mesures déjà scellées, exécutées et publiées. Les empreintes de
toutes les sources citées figurent dans les journaux du dépôt. La machine
continue de produire des verdicts — la plupart seront des fermetures, et
c'est très bien ainsi : c'est ce qui donne son prix à chaque CS+.*
