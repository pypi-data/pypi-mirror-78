# RastaSteady
RastaSteady es un software de estabilizacion de video para el sistema DJI FPV digital. RastaSteady está disponible para su uso online en https://rastasteady.com.

### Instalación local
#### Requisitos
Para el uso de RastaSteady localmente es necesario tener instalado:
- Python 3.8.5+
- ffmpeg con soporte de [vid.stab](http://public.hronopik.de/vid.stab/) (se puede descargar de [aqui](https://www.johnvansickle.com/ffmpeg/))

#### Paquete PyPi
RastaSteady se puede instalar desde [PyPi](https://pypi.org/):
```sh
$ pip install --user rastasteady
$ rastasteady --help
```

#### Desde el código fuente
Para usar el código fuente del repositorio se require [pipenv](https://pypi.org/project/pipenv/):
```sh
$ cd rastasteady
$ pipenv install
$ pipenv shell
$ pip install --editable .
$ rastasteady --help
```

#### Contenedor
RastaSteady se puede ejecutar desde un contenedor para evitar conflictos de dependencias en el equipo donde se quiere ejecutar:

```sh
$ alias rastasteady="docker run -v $PWD:/workdir quay.io/rastasteady/rastasteady"
$ rastasteady --help
```
