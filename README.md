# Technical Test for DI
Creado por Emmanuel Palomeque Alcázar

### Iniciar contenedores docker

Se inicia con la instrucción 

`docker compose up -d`

Para terminar y eliminar los contenedores y volumenes creados

`docker compose down -v`

### Acceso a la aplicación

Para acceder a la aplicación hay que visitar en el navegador la dirección

http://localhost:8000/

### Descripción

Los contenedores se encuentran en el archivo docker-compose.yml

Se ejecutan dos instancias una para la base de datos y otra para la aplicación de django

Se puede consultar la base de datos a través de la aplicación PGAdmin usando las siguientes credenciales

- POSTGRES DB: `technical_test`
- POSTGRES USER: `postgres`
- POSTGRES PASSWORD: `postgres`
- POSTGRES PORT: `5432`