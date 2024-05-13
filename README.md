# Zarankiewicz game

A Zarankiewicz-játék a Zarankiewicz-problémához kapcsolódó kétszemélyes táblajáték.

## Zarankiewicz-probléma

A [Zarankiewicz-probléma](https://en.wikipedia.org/wiki/Zarankiewicz_problem) egy megoldatlan matematikai probléma. A kérdés, hogy egy $n$ és $m$ csúcsú színosztályú páros gráfnak *maximum hány éle* lehet, ha nem tartalmazhat $r$ és $s$ csúcsú színosztályú teljes páros gráfot részgráfként. Ez a maximális élszám a **Zarankiewicz-szám** adott ($n, m, r, s$) számnégyesre.

A probléma átfogalmazható a következőképp: legfeljebb hány $1$-es lehet egy $n\cdot m$-es $0-1$-mátrixban, ha nincs $r$ sora és $s$ oszlopa úgy, hogy azok keresztezési mezői mind $1$-esek. A páros gráf incidenciamátrixa legyen a mátrix, a teljes páros gráf incidenciamátrixa pedig a keresztezési mezőkből álló mátrix.

A Zarankiewicz-probléma egyik legegyszerűbb esete az, amikor $r=s=2$, azaz nem lehet a mátrixban olyan résztéglalap, amelynek minden csúcsában $1$-es szerepel, és oldalai párhuzamosak a mátrix oldalaival. Ez a téglalap a **tiltott négyes** (forbidden rectangle).


## Zarankiewicz-játék

A játék egy $n\cdot m$-es táblán játszódik. A két játékos felváltva helyez korongokat a tábla mezőire. Több verziója is ismert, most négyfélét mutatok be. 
