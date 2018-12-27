# Repositorio para mi tesis 2.0
Segundo intento para poder comenzar decentemente mi trabajo de título, todo gracias al "Chicoteo Mortal" del Prof. Mauricio Oyarzún en la UNAP.

## CHANGELOG
**26-12-2018** - _"Recalentado" Edition_
* Cuarto gran commit
* getRunsData() genera efectivamente el array de los largos de los RUN que se generan en una matriz, sea o no ordenada
* Generación de datos para histograma completo, generación de arrays y json de salida en archivo en carpeta /output/

**24-12-2018** - _Ho-Ho-Ho M--therf--ker Edition_
* Tercer Commit
* Se agregaron las funciones getOrderedMatrix() y getRunsData() para obtención de datos para histograma
* Falta pulir getRunsData(), debido a un comportamiento no-previsto con una matriz externa.

**05-12-2018** - _It's my first job Edition_
* Segundo Commit
* Se ordenaron mucho más las clases RankerNode y Ranker Tree
* A partir de acá se generará un Branch para replantear una función de RankerNode (Ordenamiento tiene que ser de mayor a menor) y agregar funciones de recreación de matriz ordenada

**16-11-2018**
* Commit Inicial
* Se entrega junto con las clases RankerNode y RankerTree el archivo "demo_1.py" para verificar que las clases nombradas funcionen (y espero que sigan funcionando, ayer funcionaban!)
* Aprendiendo a realizar READMES como la gente

## TO-DO
- [x] Ordenamiento decreciente de árbol
- [x] Implementar Búsqueda de última generación de hijos (Access?)
- [x] Creación de nueva matriz ordenada
- [ ] ~~Creación de función Rank (Espera... Wavelet Tree?!)~~ Se reemplazó por RUN, pero sería ideal implementarlo
- [x] Creación de función para generar datos de cantidad de Runs
- [ ] Creación de un histograma para lo anterior (Matriz anterior vs. Matriz ordenada) 


**Manuel Benítez Cuevas**
