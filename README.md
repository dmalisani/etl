==================================================================
Flujo de trabajo mutilproccesing/multithreading ETL
==================================================================
Premisas:
---------
 * Optimizar el uso de recursos
 * Fácilmente extensible

Descripción:
------------
El sistema se divide en 3 capas:
 * la capa de parser tiene la lógica para extraer lineas del archivo de datos
 * la capa de procesamiento es la lógica de extracción de los datos de la api
 * la capa de persistencia implementa la clase que hace el almacenamiento de los datos

***************
digest_data() 
***************
Este método consume un *reader*(1) y lee un batch de lineas validándolas y por cada uno de los batch lanza un **proceso** (*process_line*) que maneja el batch.
 - la cantidad de procesos se corresponde al nros de cpus disponibles en el sistema.
 - process_line llama al data_extractor que completará el registro
 - cuando se completa el trabajo de data_extractor llama al *store_batch*

***************
data_extractor()
***************
Genera un **thread** por cada línea del batch y se encarga de conectarse a la api para rellenar los datos buscados (*fill_item*). Lanza tantos threads como items tenga el batch

***************
fill_item()
***************
Hace un get de la API correspondiente para traer los datos básicos, y lanza un **thread** por cada consulta complementaria que se necesite.

***************
store_batch()
***************
Instancia de la clase que maneja la base de datos. En el ejemplo, la clase PG implementa un manejador
de postgres que escribe el batch en la DB

Como extender:
--------------
 * Para soportar otros formatos de entrada deberá escribirse un reader que sea un generador de líneas de datos
 * Para cambiar la lógica de procesamiento de los datos se deberá modificar/extender fill_item()
 * La salida de los datos para se escribirá una clase que implementé el método *write_rows*  

***********
(1) reader es un generador que puede lee csv y entrega una línea por vez 

Como probar:
--------------
 * Tener instalado docker y docker-compose
 * clonar el repo
 * situarse en el directorio de la app: ``/etl`` 
 * ``docker-compose build`` genera 3 containers posgres, adminer y el ETL4
 * ``docker-compose up`` pone en funcionamiento los containers.
 * con ``docker instpect etl_1`` podrá ver la IP que toma el container ( {ip_container} )
 * en el navegador ponga {ip_container}:5000 y verá el mensaje de funcionamiento con la url para lanzar la prueba
