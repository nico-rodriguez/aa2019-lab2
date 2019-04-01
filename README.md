# Laboratorio 2 del curso Aprendizaje Automático 2019.
Se implementa una extensión del algoritmo ID3 para problemas multi-clase y atributos continuos. Además, se implementan dos tipos de clasificadores:
- un clasificador basado en un único árbol de decisión
- otro clasificador basado en varios árboles de decisión (uno por clase), donde cada uno clasifica una clase versus el resto. El clasificador realiza una especie de votación entre las clasificaciones de cada árbol para dar una clasificación final.

## Dependencias
* python3 >= 3.5.2
* treelib >= 1.5.5 : https://github.com/caesar0301/treelib

Para instalar la última versión de `treelib` como dependencia de python3 ejecutar `pip3 install [--user] treelib`.

## Modos de invocación
Hay tres modos de uso: *Entrenar*, *Evaluar* y *EvaluarAleatorio*. El primero genera el clasificador y separa las instancias
para entrenamiento y para verificación; el segundo evalúa un clasificador generado previamente con
el modo Entrenar y el tercero evalúa un clasificador aleatorio que sortea las etiquetas de clase basándose en
la cantidad de instancias que hay de cada clase.

### Entrenar un clasificador
Para Entrenar invocar como
```
python3 Main.py Entrenar [iris|covtype] [Single|Forest] [training] [directorio]
```
donde:
- `iris` o `covtype` indica el nombre del dataset que se utilizará.
- `Single` indica que se entrena un único árbol de decision multi-clase
y `Forest` indica que se entrena un clasificador formado por árboles que
clasifican una clase versus el resto.
- `training` indica la proporción de las instancias que serán destinadas
a entrenamiento; las restantes son destinadas a verificación. Debe ser
un número entre 0 y 1 (e.g. 0.8).
- `directorio` es el nombre del directorio en donde se van a guardar el clasificador
y los archivos de instancias (se guardan las de entrenamiento y verificación en dos
archivos diferentes). No debe existir otro directorio con el mismo nombre.

### Evaluar un clasificador luego de haberlo entrenado
Para Evaluar invocar como:
```
python3 Main.py Evaluar [iris|covtype] [directorio]
```
donde:
- `directorio` es un directorio generado tal como se genera con el modo Entrenar (para que funcione
correctamente, no se pueden modificar los archivos de dicho directorio). Los resultados de la evaluación
se guardan en un archivo dentro de ese mismo directorio.

### Evaluar el clasificador aleatorio (línea base)
Para EvaluarAleatorio invocar como:
```
python3 Main.py EvaluarAleatorio [iris|covtype] [validation] [salida]
```
donde:
- `validation` es la proporción de instancias del dataset seleccionado que se van a utilizar
para calcular las métricas.
- `salida` es el nombre del archivo en donde se escriben las métricas de la evaluación.

## Archivos generados
Al ejecutar el programa en modo *Entrenar*, se genera un directorio con el nombre especificado en *directorio* (si ya existía uno con ese nombre, el programa no realiza el entrenamiento). La estructura del directorio depende del clasificador que se entrena:
- si es *Single*
```
+-- _directorio
|   +-- breakpoints.txt
|   +-- classifier0.json
|   +-- training.txt
|   +-- validation.txt
```
donde *breakpoints.txt* contiene los puntos de corte de los atributos con valores continuos; *classifier0.json* contiene el árbol de decisión que se entrenó, de modo de poder cargarlo luego para evaluar sus métricas; *training.txt* contiene las instancias utilizadas para entrenar el clasificador y *validation.txt* contiene las instancias que pueden ser usadas para evaluar el clasificador (recordar que las instancias se separan según el valor del parámetro *training*).

- si es *Forest*
```
+-- _directorio
|   +-- breakpoints0.txt
|   +-- breakpoints1.txt
...
|   +-- classifier0.json
|   +-- classifier1.json
...
|   +-- distribution0.txt
|   +-- distribution1.txt
...
|   +-- training.txt
|   +-- validation.txt
```
donde ahora se tiene un archivo *breakpoints_.txt*, *classifier_.txt* y *distribution_.txt* por cada clase (recordar que para este clasificador se tiene un árbol de desición por cada clase). Los archivos *distribution_.txt* contienen las distribuciones de instancias por cada clase dentro del conjunto de entrenamiento utilizado para entrenar dicho árbol de desición.

En ambos casos, luego de invocar el programa en el modo *Evaluar*, se genera un archivo *evaluation.txt* en el mismo directorio con los valores de las métricas y la matriz de confusión para ese clasificador.

Si el programa se ejecuta en modo *EvaluarAleatorio*, se genera un archivo con el nombre indicado en el parámetro *salida*, que contiene los valores de las métricas y la matriz de confusión para ese clasificador.
