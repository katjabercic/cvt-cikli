# Računanje ciklov

Grafi, ki nas zanimajo, so nekateri grafi iz [Cenzusa kubičnih vozliščno tranzitivnih grafov](https://users.fmf.uni-lj.si/potocnik/work.htm). Za začetek so to grafi do reda $1000$, ki imajo ožino (najkrajši cikel) $6$, $7$ ali $8$, ki niso povezavno tranzitivni, in katerih red stabilizatorja vozlišča NI deljiv s $3$.
Vsi grafi iz cenzusa so kubični ($3$-regularni), enostavni, povezani in neusmerjeni.

_Tranzitivnost_ pomeni, da za vsak par vozlišč (povezav) lahko najdemo avtomorfizem grafa, ki preslika prvo vozlišče (povezavo) v drugo.

Naj bo $v$ naše najljubše vozlišče (npr. $0$) in naj bodo $e_1$, $e_2$ in $e_3$ povezave, ki se dotikajo $v$. 
Rekli bomo, da je graf _ciklično regularen_, če velja:
za vsak $k$ med $3$ in številom vozlišč grafa je število ciklov dolžine $k$, ki gredo skozi povezavo $e_i$, neodvisno od $i$ (torej enako za vse $e_1$, $e_2$, $e_3$). Vozlišča se v ciklu ne smejo ponavljati (razen prvega in zadnjega, ki sta enaka).

Če so naši cikli v resnici usmerjeni (npr. pri preiskovanju grafa) je dovolj, da primerjamo cikle, ki se v povezavah začnejo.

Naloga je poiskati primere ciklično regularnih grafov. To med drugim pomeni, da lahko s preiskovanjem nehamo takoj, ko se števili ciklov neke dolžine pri dveh od povezav ne ujemata.

## Orodja in literatura

* knjižnica `networkx`.

Literatura:

- [Finding All the Elementary Circuits of a Directed Graph](https://epubs.siam.org/doi/10.1137/0204007), [PDF](https://www.cs.tufts.edu/comp/150GA/homeworks/hw1/Johnson%2075.PDF),
- [Johnson’s algorithm To find simple cycles in a directed graph](https://medium.com/@Andrew_D./johnsons-algorithm-to-find-simple-cycles-in-a-directed-graph-89d0314b0333).

## Datoteke

* `test.py` samo šteje cikle, ki vsebujejo vozlišče $0$, za vsak prvi graf nekega reda. Pri redu $46$ približno cca 20 minut.
* `gv_mod.py` iz izvornih podatkov pridobi tiste grafe, ki imajo ustrezen red stabilizatorja.
* `cvt-100.csv`: grafi do $100$ vozlišč.
