# README #

Este repositorio hospeda una libreria python la cual sera usada desde el repositorio principal.
Esta libreria contiene utilidades para conectarse a una maquina virtual remota, en este caso se trata de una maquina virtual de windows.
El motivo por el que se ha escrito esta libreria es por automatizar el peroceso actual de creacion de conexiones en raspberries. El proceso actual es:

1. Generación de ejecutables.
 Un administrador se encarga de usar 
el script setup.bat para generar los ejecutables tanto cuando hay 
nuevas RB como cuando se alcanza la fecha de expiración de los 
archivos antiguos.
2. Control de funcionamiento.
 Un administrar ejecuta diariamente el 
script check.exe en una virtual y almacena la información de las RB 
que están funcionando y de las que dan error. En el caso de error de 
alguna RB, procede con la planificación para intentar solucionar el 
problema.


### Release

En el caso de que se quiera publicar una nueva version de la libreria, siga las siguientes instrucciones https://packaging.python.org/tutorials/packaging-projects/

Un target ha sido añadido para facilitar este proceso. En el caso de que desee publicar una nueva version, actualice la version del paquete en el archivo `setup.bat`, y ejecute `make publish`.
El paquete puede ser visualizado en la pagina de pypi https://pypi.org/project/ssh-client/