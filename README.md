# Računanje ciklov

Grafi, ki nas zanimajo, so nekateri grafi iz [Cenzusa kubičnih vozliščno tranzitivnih grafov](https://users.fmf.uni-lj.si/potocnik/work.htm). Za začetek so to grafi do reda $1000$, ki imajo ožino (najkrajši cikel) $6$, $7$ ali $8$, ki niso povezavno tranzitivni, in katerih red stabilizatorja vozlišča NI deljiv s $3$.
Vsi grafi iz cenzusa so kubični ($3$-regularni), enostavni, povezani in neusmerjeni.

_Tranzitivnost_ pomeni, da za vsak par vozlišč (povezav) lahko najdemo avtomorfizem grafa, ki preslika prvo vozlišče (povezavo) v drugo.

Naj bo $v$ naše najljubše vozlišče (npr. $0$) in naj bodo $e_1$, $e_2$ in $e_3$ povezave, ki se dotikajo $v$. 
Rekli bomo, da je graf _ciklično regularen_, če velja:
za vsak $k$ med $3$ in številom vozlišč grafa je število ciklov dolžine $k$, ki gredo skozi povezavo $e_i$, neodvisno od $i$ (torej enako za vse $e_1$, $e_2$, $e_3$). Vozlišča se v ciklu ne smejo ponavljati (razen prvega in zadnjega, ki sta enaka).

Če so naši cikli v resnici usmerjeni (npr. pri preiskovanju grafa) je dovolj, da primerjamo cikle, ki se v povezavah začnejo.

Naloga je poiskati primere ciklično regularnih grafov. To med drugim pomeni, da lahko s preiskovanjem nehamo takoj, ko se števili ciklov neke dolžine pri dveh od povezav ne ujemata.

Primožev komentar: 

> Za 6 domnevam, da jih ni, pri 7 ali 8 pa bi po mojem morali najti kake primere. Skratka, program, ki tole pregleda do, recimo, 1.000 vozlišč v enem tednu, prejme nagrado (ne samo simbolično). Če je 1.000 preveč, potem bom zadovoljen do manj (sam znam narediti do 400). Skratka, čim dlje.


## Orodja in literatura

* knjižnica `networkx`.
* SageMath se uporabi za preverjanje povezavne tranzitivnosti. Če ga imate že nameščenega, je treba virtualno okolje narediti s Pythonom, ki pride v paketu: `sage -python -m venv venv`.

Literatura:

- [Finding All the Elementary Circuits of a Directed Graph](https://epubs.siam.org/doi/10.1137/0204007), [PDF](https://www.cs.tufts.edu/comp/150GA/homeworks/hw1/Johnson%2075.PDF),
- [Johnson’s algorithm To find simple cycles in a directed graph](https://medium.com/@Andrew_D./johnsons-algorithm-to-find-simple-cycles-in-a-directed-graph-89d0314b0333).

## Datoteke

* `test.py` samo šteje cikle, ki vsebujejo vozlišče $0$, za vsak prvi graf nekega reda. Pri redu $46$ približno cca 20 minut.
* `gv_mod.py` iz izvornih podatkov pridobi tiste grafe, ki imajo ustrezen red stabilizatorja.
* `cvt-100.csv`: grafi do $100$ vozlišč.

Nove datoteke:
- `johnson.py`: kopija implementacije algoritma iz nx, a rahlo zoptimitirana (ne kopiramo vsakič cikla, le 
  prvi dve vozlišči) in prirejena (namesto `list(set(...)` dodam `sorted(set(...))`, da lahko prej prekinemo for zanko)
- `stuff.py`: dve pomožni funkciji (naloži grafe, naredi _kao lep_ loger)
- `prvi_poskus.py`: temelji na Ideja 1 (Glej spodaj)

Datoteke na OneDrive-u:

- `cvt-1000-girth-6-7-8-not-mod-3.csv`: `order`, `sparse6`
- `cvt-info-1000-girth-6-7-8-not-mod-3.csv`: `order`, `cvt_id`, `girth`, `mod3`, `sparse6`
- `Census3valentVTproperties.csv`: datoteka s podatki `Order`, `ID`, `Girth`, `Diam`, `IsBipartite`, `IsSPX`, `Gv`, ki se uporabi, da dobimo datoteko `cvt-info-1000-girth-6-7-8-not-mod-3.csv`

`order` je red grafa, `cvt_id` skupaj z redom tvori ID grafa v cenzusu: $(n, i)$, `mod3` je ostanek pri deljenju s $3$, `sparse6` pa je zapis grafa v tem formatu.

## Ideja 1

Imamo graf `G(V, E)`.

1. Najdemo "različni" povezavi, tj. povezavi, ki imata v (še vedno neusmerjenem) [grafu povezav](https://en.wikipedia.org/wiki/Line_graph)
   različni (neizomorfni) okolici vozlišč, ki so od njiju oddaljene največ `r`.
   - Želimo, da sta ti povezavi oblike `(x, y)` in `(x, z)` (kjer so `x, y, z` vozlišča iz `V`), tj. imata skupno
     vozlišče, saj bomo kasneje šteli cikle iz nekega vozlišča
   - Ker je to prvi poskus, sem iskal `x = 0` in morda se najde pri kakšnem drugem manjši polmer
2. Zagotovimo si, da pri DFS v Johnsonovem algoritmu vozlišči `y` in `z` prideta na sklad na koncu (zato, da sta prvi
   `pop()`-njeni in lahko zgodaj brejknemo)
3. Štejemo cikle.

### Trenutno stanje

Prvih 40 grafov v cca. toliko minutah (na 7 let starem prenosniku).

### Možnosti za izboljšavo:

1. Implementacija:
    - nx implementacija (in njena mini priredba našim potrebam je zelo daleč od učinkovite
    - `numba` (in bolj osnovne/čiste strukture) za začetek, lahko tudi `c++`
2. Algoritem:
    - Denimo, da sta polmera okolic `r`. Ali je dovolj gledati cikle dolžine `<= k(r)` (cca. `k = 2r` je videti ok meja)
    - Ali je dovolj gledati graf, ki vsebuje vozlišča iz unije teh okolic? (morda vsebuje veliko manj vozlišč)
    - Ali lahko prirežemo Johnsonov algoritem (tako, da ne nalagamo na sklad, če je trenutna pot že dovolj dolga)?
    - Ali lahko spremenimo Johnsona v iskanje v širino? (malo dvomim, ampak tako bi najprej dobili kratke cikle)

Pri algoritmičnih izboljšavah gre predvsem zato, da je krajših ciklov veliiiiko manj kot dolgih.


## Podatki

Poizvedba na DiscreteZOO bazi, s katero dobimo prvi nabor grafov:

```
select graph.'order', graph_cvt.cvt_index, graph.data, 
from
	graph inner join graph_cvt 
	on graph.zooid = graph_cvt.zooid
where
	graph.'order' <= 1000 and
	graph.is_vertex_transitive and
	not graph.is_edge_transitive and
	graph_cvt.cvt_index is not null and
	graph.girth >= 6 and
	graph.girth <=8
```

Na tej točki še ne upoštevamo pogoja, da red stabilizatorja vozlišča NI deljiv s 3.
Podatki o stabilizatorju so v datoteki `Census3valentVTproperties.csv` (prečiščeno iz tistega, kar je poslal Primož).
Skripta `gv-mod.py` izpiše datoteko s podatkom o modulu.

Novo dobljeno datoteko se za zdaj uvozi v DiscreteZOO bazo, naredi `join` po prvih dveh stolpcih in novo poizvedbo za samo tiste grafe, ki imajo ustrezen ostanek pri deljenju.
