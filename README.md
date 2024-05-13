# Zarankiewicz game

A Zarankiewicz-játék a Zarankiewicz-problémához kapcsolódó kétszemélyes táblajáték.

## Zarankiewicz-probléma

A [Zarankiewicz-probléma](https://en.wikipedia.org/wiki/Zarankiewicz_problem) egy megoldatlan matematikai probléma. A kérdés, hogy egy $n$ és $m$ csúcsú színosztályú páros gráfnak *maximum hány éle* lehet, ha nem tartalmazhat $r$ és $s$ csúcsú színosztályú teljes páros gráfot részgráfként. Ez a maximális élszám a **Zarankiewicz-szám** adott ($n, m, r, s$) számnégyesre.

A probléma átfogalmazható a következőképp: legfeljebb hány $1$-es lehet egy $n\cdot m$-es $0-1$-mátrixban, ha nincs $r$ sora és $s$ oszlopa úgy, hogy azok keresztezési mezői mind $1$-esek. A páros gráf incidenciamátrixa legyen a mátrix, a teljes páros gráf incidenciamátrixa pedig a keresztezési mezőkből álló mátrix.

A Zarankiewicz-probléma egyik legegyszerűbb esete az, amikor $r=s=2$, azaz nem lehet a mátrixban olyan résztéglalap, amelynek minden csúcsában $1$-es szerepel, és oldalai párhuzamosak a mátrix oldalaival. Ez a téglalap a **tiltott négyes** (forbidden rectangle).

<p align="center">
  <img width="200" height="200" src="images-and-links/tiltott_negyes.png">
</p>


## Zarankiewicz-játék

A játék egy $n\cdot m$-es táblán játszódik. A két játékos felváltva helyez korongokat a tábla mezőire. Több verziója is ismert, most négyfélét mutatok be. A *tiltott négyes* a játéknál azt jelenti, hogy a táblán azonos színű korongok vannak egy, a tábla oldalaival párhuzamos téglalap négy csúcsában. A négyféle játéktípus:

- a játékosoknak azonos/ különböző színű korongjaik vannak
- az nyer/ veszít, aki kialakít egy tiltott négyest

Természetesen a játéknak rengeteg más változatát is ki lehet találni, de ezekről később nem lesz szó. Néhány ezek közül nem igazán kapcsolódik az eredeti problémához. Például:

- $r\cdot s$-es részmátrixot veszünk a tiltott négyes helyett
- a tiltott négyes egy meghatározott méretű téglalap négy csúcsa
- a tiltott négyes egy négyzet négy csúcsa
- a tiltott négyes téglalapjának nem kell a tábla oldalaival párhuzamosnak lennie


## Nyerő stratégiák

A játék egyes változataiban az egyik játékosnak ismert nyerő stratégiája. Ezek a nyerő stratégiák Fábián Kata [szakdolgozatában](images-and-links/fabian_kata_cikk.pdf) találhatók, bizonyítással együtt. A következő játéktípusokban ismert a nyerő stratégia, a többi még megfejtésre vár.

1. A játékosoknak azonos színű korongjai vannak és az nyer, aki kialakít egy tiltott négyzetet
2. A játékosoknak különböző színű korongjai vannak és az nyer, aki kialakít egy tiltott négyzetet (itt a 4x4-es és a legalább 5x5-ös táblára van bizonyított stratégia)

Az első esetben ha $n$ és $m$ is páratlan, az első játékosnak van nyerő stratégiája, különben a másodiknak.

A második eset amőba-típusú játék, hiszen két színnel játszódik. Az ilyen játékokban a második játékosnak nem lehet nyerő stratégiája, különben az első "el tudná lopni" a stratégiáját. A cikkben erről is szó esik. Az első játékosnak viszont a megjelölt táblaméretekre van nyerő stratégiája. 


# Játék működése

A játék elinításakor a start gomb megnyomásával a játékmód-választó oldalra jutunk. Itt beállíthatjuk, hogy a négy játékmód melyike legyen. A SPACE billentyű lenyomása a többi beállításhoz visz. Itt kiválaszthatjuk, hogy két emberi játékos, egy emberi játékos és egy gép vagy két gép játsszon egymás ellen. Továbbá a tábla méretét is beállíthatjuk. A három előre megadott lehetőség mellett saját méreteket is megadhatunk az $n$ és $m$ feliratú mezőkre kattintva. Bár nagyobb táblaméreteket is meg lehet adni, $20\times20$-asnál lehetőleg ne legyen nagyobb, mert a cellák nagyon kicsik lesznek. A világosabb zöld szín jelzi, hogy írni lehet a "custom" felirat melletti mezőkbe. A BACKSPACE billentyűvel törölni is tudunk belőlük. Az ENTER megnyomásával fejezhetjük be az írást, ekkor visszavált a cella a sötétebb zöld színre. Ha a custom cellák kitöltése után mégis előre megadott méretet választunk, akkor a tábla mérete a kiválasztott előre megadott méretű lesz.

<p align="center">
  <img width="200" height="200" src="game-mode-select.gif" alt="animated" >
</p>


A játék a SPACE megnyomásával indul. Felül jelzi, hogy melyik játékos következik. Ha két szín van, az első játékosé a zöld, a másodiké a narancssárga. Különben zöld színűek az elfoglalt mezők. A soron következő játékos a kiválasztott cellára kattintással foglalhatja el a mezőt. Ha ez a játékos a számítógép, automatikusan választ mezőt. A játék végét a tiltott négyes megjelenése jelenti. Ekkor a tiltott négyest kiegészítő mező világosabb színű lesz. Az is lehetséges, hogy minden mező betelt, de nincs tiltott négyes. Ekkor döntetlen az eredmény. Ezután SPACE-szel lehet a legutolsó képernyőt megjeleníteni, ami kiírja a győztest (vagy azt, hogy döntetlen) és lehetőséget ad a játék újraindítására. A restart gomb a start képernyőre visz. A játékot bármikor leállíthatjuk az ESCAPE billentyűvel vagy az ablak bezárásával.

