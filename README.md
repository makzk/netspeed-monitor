## Monitor de velocidad de internet

Esta pequeña aplicación realiza una prueba de velocidad cada cierto tiempo
(mediante el módulo [netspeed-cli](https://pypi.org/project/speedtest-cli/))
y guarda los resultados en una base de datos MongoDB, para luego mostrarlos
en una página expuesta con Flask.

### Instalación

Se requiere instalar Python 3 en su última versión, y acceso a una base
de datos MongoDB, tal como se dice anteriormente. Con eso, realizar los
siguientes pasos:

1. Instalar `virtualenv` de forma global. Es decir, ya sea mediante el
proveedor de paquetes de tu sistema, en el caso de Linux, o mediante
una instalación global con pip.
   * Con pip es ejecutar: `pip install virtualenv`. Puede requerir permisos
     de administrador.
2. Clonar este repositorio en alguna carpeta a la que tengas acceso.
3. Crear un *virtualenv* en la carpeta donde hayas clonado el repositorio
   * `virtualenv -p python3 .venv` (en el caso de que el ejecutable de
    python sea `python3`)
4. Activar el virtuaenv:
   * Windows: ejecutar `.venv\Scripts\activate.bat`
   * *nix: `source .venv/bin/activate`
5. Instalar dependencias: `pip install -r requirements.txt`
6. Copiar `settings.example.py` a `settings.py` y configurar:
   * `DATABASE_URI`: el formato es `'mongodb://HOST/NOMBRE_DB'`, por ejemplo
   `'mongodb://127.0.0.1/netspeed'`
   * `SERVER_ID`: el ID del servidor de speedtest. Se puede obtener con el
   comando speedtest-cli, por ejemplo, ejecutando 
   `speedtest-cli --serverlist | grep Chile` en Linux o 
   `speedtest-cli --serverlist | findstr /R /C:"Chile"` en Windows,
   para filtrar los servidores que sean de Chile. Resultará en varias líneas
   del formato `ID) Nombre servidor, País`. Utilizar el ID mostrado.

### Ejecución

Este sistema tiene dos ejecuciones: el *worker*, que genera los resultados
de pruebas de velocidad, y la página, que muestra los resultados.

#### Worker

Idealmente, el *worker* se ejecuta mediante `.venv/bin/python worker.py`
(estando en la ruta del proyecto), y se debe ejecutar cada cierto tiempo,
ya sea cada 15, 20 o 30 minutos, por ejemplo. Se debe programar una tarea
que ejecute el comando periódicamente, por ejemplo, en Linux es con CRON
o con timers de Systemd.

#### Sitio web

Se debe ejecutar la aplicación Flask con el módulo `app.py`, en la siguiente
forma, en Linux:

```
$ export FLASK_APP=hello.py
$ flask run
 * Running on http://127.0.0.1:5000/
```

Luego de ello, entrar a http://127.0.0.1:5000/

Se pueden ver más formas de ejecución aquí: 
https://flask.palletsprojects.com/en/1.1.x/quickstart/
