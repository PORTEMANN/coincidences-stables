# Invariance, principe variationnel et équations d'Einstein

*Version texte intégrale (extraction du PDF). Artefact canonique : le PDF
`INVARIANCE-EINSTEIN-2026-10-09.pdf` (sha256
`5f320316bcd0d1b50d79b5c9db4781c6d83462d49bcb1c236695f995bad0bbac`), déposé
hors dépôt par son auteur ; le canal de dépôt de ce chantier est texte seul.*

---

Invariance, principe variationnel et équations
d’Einstein
Une lecture effective : covariance, contraintes, entropie et information géométrique
Synthèse théorique
9 octobre 2026
Résumé
Cette note formalise une chaîne d’arguments reliant invariance, principe variationnel et
équations d’Einstein. Le point de départ n’est pas une hypothèse substantialiste sur la gra-
vité, mais une exigence négative : aucune structure absolue non mesurable ne doit entrer
dans la loi. Sous les conditions de covariance générale, d’absence de champ additionnel
et de dérivées au plus secondes, le théorème de Lovelock impose la forme Gµν + Λgµν en
dimension quatre. Le principe variationnel est ensuite traité comme un problème bulk–
bord : l’action d’Einstein–Hilbert exige les termes de Gibbons–Hawking–York et une
classe de conditions initiales contraintes. La forme δ(E −TI ) = 0 est enfin analysée
comme équation d’état thermodynamique locale plutôt que comme dogme fondamental,
dans le prolongement de Jacobson, d’Unruh et de l’action spectrale. La généralisation
informationnelle admissible est alors une théorie effective des champs : elle renormalise
les constantes, ajoute des opérateurs de courbure supérieure et doit déclarer un régime
où son absence la réfuterait.
Table des matières
1 Position du problème 2
2 Invariance, covariance et contraintes 2
3 Principe variationnel et conditions au bord 3
4 Unicité d’Einstein–Hilbert et coût des extensions 3
5 Thermodynamique locale et δ(E −TS ) = 0 4
6 F onctionnelle informationnelle effective 4
7 Décomposition conforme et problème de l’échelle 5
8 Discussion : stabilité, évolutivité et réfutabilité 5
1

1 Position du problème
La question théorique peut être formulée ainsi : quelle est la part de nécessité et la part de
convention dans les équations d’Einstein ? La réponse défendue ici est que la forme
Gµν + Λgµν = 8πGT µν (1)
est moins une hypothèse sur une « force gravitationnelle » qu’un point de fermeture imposé
par des contraintes d’invariance, de dérivabilité et de cohérence. Trois niveaux doivent être
distingués.
Invariance. Les lois ne doivent dépendre ni d’un système de coordonnées, ni d’une métrique
de fond, ni d’une foliation temporelle privilégiée. Cette exigence est négative : elle interdit
les structures absolues non mesurables.
V ariation. Les équations doivent suivre d’une action dont la classe de conditions au bord
est déclarée. En relativité générale, δS = 0 n’a de sens qu’avec les termes de bord et les
contraintes qui rendent le problème aux valeurs initiales bien posé.
Effectivité. Toute extension informationnelle ou thermodynamique doit d’abord réappa-
raître comme renormalisation des constantes et comme opérateurs de dimension supérieure,
contrôlés par les tests du Système solaire et de Cavendish.
Principe 1 (Minimalité invariante). N’introduire ni champ additionnel, ni dérivée d’ordre
supérieur, ni structure de fond, tant qu’une donnée mesurable ne l’exige pas. Lorsqu’un tel
élément est ajouté, il doit être daté, motivé et assorti du régime où son absence le réfuterait.
2 Invariance, covariance et contraintes
Soit (M,g ) une variété lorentzienne de dimension quatre et ψ un secteur de matière. La cova-
riance générale impose que les lois soient des relations entre objets géométriques intrinsèques,
covariantes sous l’action des difféomorphismes :
ϕ :M →M, g ↦→ϕ∗g, ψ ↦→ϕ∗ψ. (2)
Cette invariance n’est pas une symétrie physique au sens où deux états distincts seraient iden-
tifiés par une transformation mesurable ; c’est une redondance de description. Sa conséquence
profonde est que certaines variables apparentes ne sont pas dynamiques.
Dans la décomposition d’Arnowitt–Deser–Misner, la métrique se réécrit en termes de lapse
N , de shift N i et de métrique spatiale hij 1. Les équations d’Einstein se scindent alors en
quatre contraintes et six équations d’évolution. Le lapse et le shift ne décrivent pas des
degrés de liberté propres : ils sont des multiplicateurs de Lagrange associés aux contraintes
hamiltonienne et d’impulsion. Le temps coordonné ne s’écoule pas dans les équations ; il
paramètre une jauge.
L’invariance par difféomorphismes produit aussi les identités de Noether adaptées à une jauge.
Du côté géométrique, l’identité de Bianchi contractée est
∇µGµν = 0. (3)
Du côté matière, l’invariance deSm jointe aux équations du mouvement de la matière implique
∇µT µν = 0. (4)
2

L’équation ( 1) est donc une fermeture mutuelle : le membre géométrique est identiquement
sans divergence, et le membre matériel doit l’être par ses propres lois. Toute modification de la
gravité doit préserver cette fermeture ou expliquer explicitement où passe la non-conservation
apparente.
Remarque 1. Les identités (3) et (4) ne sont pas des lois de conservation ordinaires au sens
global. En présence de symétries de Killing, elles donnent des charges conservées ; sans telles
symétries, elles expriment la cohérence locale entre géométrie et matière.
3 Principe variationnel et conditions au bord
L’action gravitationnelle minimale est l’action d’Einstein–Hilbert :
SEH [g] = 1
16πG
∫
M
d4x √−g (R − 2Λ). (5)
Sa variation contient des dérivées secondes de δg µν. Après intégration par parties, le terme de
volume donne le tenseur d’Einstein, mais il reste un terme de bord. Pour obtenir un problème
variationnel bien posé lorsque la métrique induite hab est fixée sur ∂M , il faut ajouter le terme
de Gibbons–Hawking–York 2,3 :
SGHY = 1
8πG
∫
∂M
d3x
√
|h|K. (6)
Le principe variationnel correct n’est donc pas seulement δSEH = 0, mais
δ (SEH +SGHY +Sm) = 0 (7)
dans une classe de variations compatible avec les conditions au bord déclarées. Selon le
problème, ces conditions peuvent être de Dirichlet pour hab, asymptotiquement plates avec
charges ADM, ou adaptées à un horizon.
Cette structure bulk–bord a une conséquence conceptuelle : la loi gravitationnelle ne se réduit
pas à une équation locale d’évolution. Elle inclut des contraintes sur les données initiales.
Les équations G00 = 8πGT00 et G0i = 8πGT0i ne propagent rien ; elles filtrent les données
admissibles. La relativité générale est ainsi une théorie où la dynamique est inséparable d’une
règle d’admissibilité.
Proposition 1 (Lecture variationnelle). L’action d’Einstein–Hilbert est la forme de volume
minimale compatible avec une métrique dynamique et des équations du second ordre. Son
terme de bord n ’est pas un accessoire technique : il définit ce qui est tenu fixe lorsque le
possible est tranché en un état.
4 Unicité d’Einstein–Hilbert et coût des extensions
Le théorème de Lovelock fournit la forme d’unicité essentielle 4,5. En dimension quatre, le seul
tenseur symétrique d’ordre deux, sans divergence, construit à partir de la métrique et de ses
dérivées jusqu’à l’ordre deux, est une combinaison linéaire de Gµν etgµν. Sous les conditions
de covariance, d’équations au plus secondes et d’absence de champ additionnel, il ne reste
donc que l’équation ( 1).
Toute extension consiste à abandonner l’une des conditions minimales :
— dérivées quatrièmes : termes R2, RµνRµν, CµνρσCµνρσ ou gravité conforme ;
3

— champ scalaire additionnel : théories scalaire-tenseur ou dilaton ;
— torsion : cadre d’Einstein–Cartan ;
— non-localité : opérateurs analytiques en □−1, mémoire ou noyaux effectifs ;
— brisure de covariance : foliation privilégiée ou éther dynamique.
Le critère n’est pas d’interdire ces extensions, mais d’en exiger le prix complet : contenu
de champ déclaré, stabilité des modes, contraintes solaires, régime de validité et réfutabilité.
À cet égard, l’action spectrale de Connes–Chamseddine et la gravité induite de Sakharov
sont des précédents importants : les termes d’Einstein–Hilbert et de courbure supérieure
y apparaissent comme coeﬀicients d’un développement effectif plutôt que comme axiomes
isolés 6,7.
Remarque 2. La constance de la forme (1) à basse énergie n ’implique pas qu’elle soit
fondamentale. Elle implique seulement que toute théorie candidate doit l’avoir comme limite
contrôlée.
5 Thermodynamique locale et δ(E − T S) = 0
L’expression δ(E −TS ) = 0 évoque un principe d’énergie libre. Sa version relativiste la plus
propre est locale et horizons par horizons. Pour un observateur accéléré, l’horizon de Rindler
possède une température d’Unruh 8 :
TU = ¯hκ
2πkB
. (8)
Si l’entropie est proportionnelle à l’aire,
dS =ηdA, (9)
et si le bilan local de Clausius δQ = TdS est imposé, alors l’évolution de l’aire, gouvernée
par l’équation de Raychaudhuri 9, conduit à une relation entre tenseur de Ricci et tenseur
énergie–impulsion. Jacobson a montré que l’exigence de ce bilan pour tous les horizons locaux
de Rindler redonne l’équation d’Einstein comme équation d’état, la constante cosmologique
entrant comme constante d’intégration 10.
La portée exacte de ce résultat doit être maintenue avec soin. Il ne démontre pas que l’espace-
temps est « fait » d’information. Il montre qu’avec des hypothèses d’équilibre local, d’entropie
d’aire et de température d’accélération, la forme des équations d’Einstein est celle d’un bilan
thermodynamique de la causalité.
Principe 2 (Statut de δ(E −TI ) = 0 ). La variation d’une fonctionnelle du type E −TI
est admissible comme équation d’état locale de l’espace-temps lorsque I est une entropie
d’horizon ou une fonction spectrale régularisée. Elle ne devient une action fondamentale que
si la mesure d’information, le contenu de champ et la cut-off sont déclarés.
6 Fonctionnelle informationnelle effective
Une généralisation informationnelle contrôlée peut s’écrire
Seff[g] = SEH [g] +Sbord −TI Λ[g] +Sm[g,ψ ], (10)
oùIΛ[g] est diffeomorphe-invariante et régularisée à l’échelle Λ. Deux définitions sont compa-
tibles à basse dimension : une entropie de von Neumann géométrique,
I[g] = SvN [g] = (1 −β∂β) lnZβ[g], (11)
4

ou une action spectrale tronquée,
IΛ[g] = Trf
(D2
Λ2
)
, (12)
pour un opérateur de type Laplace D2 et une fonction de régularisation f 6,11. Le développe-
ment de Seeley–DeWitt donne alors
IΛ[g] = b0
∫
M
√g +b1
∫
M
√gR +
∫
M
√g
(
bR2R2 +bWeylC2 + · · ·
)
+ O(Λ−2) + non local. (13)
La variation de ( 10) ne détruit donc pas Einstein ; elle déplace les constantes :
1
Geff
= 1
G0
− 16πTb 1, (14)
αeff =α0 −Tb R2, β eff =β0 −Tb Weyl. (15)
Les termes quadratiques engendrent des corrections de type Yukawa dans le potentiel newto-
nien et des modes additionnels dont la stabilité doit être démontrée. Les bornes du Système
solaire et des expériences de Cavendish imposent que ces corrections soient faibles, courtes
ou découplées.
Remarque 3. Avant la déclaration d’un contenu de champ précis, les coeﬀicients b0,b1,bR2
et bWeyl restent des formes plutôt que des mesures. Une valeur numérique de Geff(T ) sans
secteur quantique déclaré serait une calibration déguisée en prédiction.
7 Décomposition conforme et problème de l’échelle
La décomposition
gµν = Ω 2(x) ¯gµν (16)
sépare la classe conforme [¯g], qui porte les angles, du facteur Ω, qui porte l’échelle locale. Elle
est utile comme paramétrage : la forme est lue dans [¯g], tandis que la stationnarité de l’action
fixe Ω. En quatre dimensions, l’action d’Einstein–Hilbert n’est toutefois pas invariante de
Weyl : √−gR − →√−¯g
(
Ω2 ¯R + 6Ω ¯□Ω
)
. (17)
Parler d’invariance conforme exige donc un prix supplémentaire : compensateur de type
dilaton, action Weyl carrée d’ordre quatre, ou brisure contrôlée de la symétrie. La position
prudente est de traiter ( 16) comme une décomposition de jauge adaptée au problème de
l’échelle, non comme une preuve que la nature possède une jauge conforme exacte.
Dans cette lecture, une « base » du tranchage serait la donnée d’une classe conforme et de
conditions au bord ; l’actualisation d’une grandeur mesurable correspond à la sélection d’un
Ω compatible avec les contraintes. Cette formulation garde l’intuition d’une scène invariante
sous changement d’éclairage, sans conférer à la métaphore conforme un statut expérimental
qu’elle n’a pas encore.
8 Discussion : stabilité, évolutivité et réfutabilité
La stabilité d’un univers covariant ne signifie pas l’absence de changement. Elle signifie l’exis-
tence de relations conservées malgré la redondance des descriptions : identités de Bianchi,
contraintes initiales, attracteurs classiques et bornes effectives. L’évolutivité vient de ce que
5

la géométrie est dynamique ; la stabilité vient de ce que cette dynamique est contrainte. C’est
cette combinaison de liberté locale et de fermeture globale qui donne à la même scène son
identité sous plusieurs éclairages : géométrique, thermodynamique ou informationnel.
La discipline théorique qui en découle peut être condensée en sept règles :
1. déclarer les invariances avant les équations ;
2. distinguer symétrie physique et redondance de jauge ;
3. écrire l’action avec ses termes de bord et ses contraintes ;
4. n’ajouter ni champ ni dérivée supérieure sans régime de réfutation ;
5. traiter δ(E −TI ) = 0 comme équation d’état locale tant que I n’est pas mesurée ;
6. exprimer toute information géométrique comme renormalisation de constantes ou opéra-
teurs effectifs ;
7. publier les coeﬀicients, les bornes nulles et les échecs au même niveau que les succès.
La conclusion est volontairement étroite. Les équations d’Einstein sont le point minimal
de fermeture invariante en dimension quatre ; les extensions thermo-informationnelles sont
légitimes comme théories effectives lorsqu’elles déclarent contenu, cut-off et stabilité ; et toute
lecture plus forte — ontologique, noétique ou computationnelle — doit être renvoyée à un
protocole où l’absence d’effet produirait une réfutation datée. La théorie peut éclairer la
scène ; elle ne doit pas décider à la place de la mesure.
Remerciements et statut
Ce texte est une synthèse formelle et critique. Il ne constitue ni une validation expérimen-
tale, ni une revue complète de la gravité quantique, ni une approbation des interprétations
ontologiques discutées dans le corpus qui l’a motivé.
Références
[1] Richard Arnowitt, Stanley Deser, and Charles W. Misner. The dynamics of general
relativity. In Louis Witten, editor, Gravitation : An Introduction to Current Research ,
pages 227–265. Wiley, New York, 1962.
[2] Gary W. Gibbons and Stephen W. Hawking. Action integrals and partition functions in
quantum gravity. Physical Review D , 15(10) :2752–2756, 1977.
[3] James W. York. Role of conformal three-geometry in the dynamics of gravitation. Phy-
sical Review Letters , 28(16) :1082–1085, 1972.
[4] David Lovelock. The einstein tensor and its generalizations. Journal of Mathematical
Physics, 12(3) :498–501, 1971.
[5] David Lovelock. The four-dimensionality of space and the einstein tensor. Journal of
Mathematical Physics , 13(6) :874–876, 1972.
[6] Ali H. Chamseddine and Alain Connes. The spectral action principle. Communications
in Mathematical Physics , 186(3) :731–750, 1997.
[7] Andrei D. Sakharov. Vacuum quantum fluctuations in curved space and the theory of
gravitation. Soviet Physics Doklady , 12 :1040–1041, 1968.
6

[8] William G. Unruh. Notes on black-hole evaporation. Physical Review D , 14(4) :870–892,
1976.
[9] Amal Kumar Raychaudhuri. Relativistic cosmology. i. Physical Review, 98(4) :1123–1126,
1955.
[10] Ted Jacobson. Thermodynamics of spacetime : The einstein equation of state. Physical
Review Letters, 75(7) :1260–1263, 1995.
[11] R. T. Seeley. Complex powers of an elliptic operator. In Singular Integrals (Proc.
Sympos. Pure Math., Chicago, Ill., 1966) , volume 10 of Proceedings of Symposia in Pure
Mathematics, pages 288–307. American Mathematical Society, Providence, RI, 1967.
7
