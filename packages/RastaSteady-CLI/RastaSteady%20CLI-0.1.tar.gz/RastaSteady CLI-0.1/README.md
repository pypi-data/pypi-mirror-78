# RastaSteady CLI
RastaSteady es un software de estabilizacion de video para el sistema DJI FPV digital, aunque puede usarse con cualquier video.

### Instalacion
#### Genérica
RastaSteady CLI se puede instalar desde [PyPi](https://pypi.org/):
```sh
$ pip install --user rastasteady-cli

```

#### Desde el código fuente
Para usar el código fuente tal cual se publica se require [pipenv](https://pypi.org/project/pipenv/):
```sh
$ cd rastasteady-cli
$ pipenv install
$ pipenv shell
$ pip install --editable .
```
#### Contenedor
RastaSteady se puede ejecutar desde un contenedor para evitar conflictos de dependencias en el equipo donde se quiere ejecutar.

```sh
$ alias rastasteady-cli="docker run -v $PWD:/workdir quay.io/rastasteady/rastasteady-cli"
```

### Por hacer
#### Automatizaciones
 - creacion de pipeline para crear el paquete y subirlo a [PyPi](https://pypi.org/)
 - agregar Dockerfile para construir el contenedor y crear la integracion en quay.io

#### Usabilidad de la clase RastaSteady
 - agregar opcion para ocultar la salida de ffmpeg y enviarla a fichero
 - agregar opciones que permitan especificar la resolucion del fichero final deseado
 - agregar opcion para reutilizar los ficheros temporales existentes
 - poder trabajar con ficheros de entrada en directorios distintos al actual
 - poder definir el nombre y localización de los ficheros finales

#### Varios
 - comprobacion de fichero de origen antes de comenzar (existencia, permisos, etc.)
 - crear dependencia de la libreria rastasteady cuando esté publicada en [PyPi](https://pypi.org/).
