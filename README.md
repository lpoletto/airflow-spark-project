# Instalación

1. Crear las siguientes carpetas a la misma altura del `docker-compose.yml`.

```bash
mkdir -p ./dags ./logs ./plugins ./config ./scripts ./spark_drivers
```

2. Crear un archivo con variables de entorno llamado `.env` ubicado a la misma altura que el `docker-compose.yml`. Cuyo contenido sea:
```bash
POSTGRES_HOST=... # YOUR_POSTGRES_HOST
POSTGRES_PORT=... # YOUR_POSTGRES_PORT
POSTGRES_DB=... # YOUR_POSTGRES_DB
POSTGRES_USER=... # YOUR_POSTGRES_USER
POSTGRES_SCHEMA=... # YOUR_POSTGRES_SCHEMA
POSTGRES_PASSWORD=... # YOUR_POSTGRES_PASSWORD
POSTGRES_URL="jdbc:postgresql://${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}?user=${POSTGRES_USER}&password=${POSTGRES_PASSWORD}"
DRIVER_PATH=/tmp/drivers/postgresql-42.5.2.jar,/tmp/drivers/mysql-connector-j-8.0.32.jar
```
3. Descargar las imagenes de Airflow y Spark. En caso de error al descargar las imagenes, debe hacer un login en DockerHub.
```bash
docker pull lpoletto/airflow:airflow_2_6_2
docker pull lpoletto/spark:spark_3_4_1
```
4. Las imagenes fueron generadas a partir de los Dockerfiles ubicados en `docker_images/`. Si se desea generar las imagenes nuevamente, ejecutar los comandos que están en los Dockerfiles.
5. Ejecutar el siguiente comando para levantar los servicios de Airflow y Spark.
```bash
docker-compose up -d
```
6. Una vez que los servicios estén levantados, ingresar a Airflow en `http://localhost:8080/`.
7. En la pestaña `Admin -> Connections` crear una nueva conexión con los siguientes datos para Postgres:
    * Conn Id: `postgres_default`
    * Conn Type: `Postgres`
    * Host: `postgres` (El nombre del servicio de PostgreSQL (ej. *postgres*), o *host.docker.internal* si la base de datos está fuera de la red Docker.)
    * Database: `base de datos de Postgres`
    * Schema: `esquema de Postgres`
    * User: `usuario de Postgres`
    * Password: `contraseña de Postgres`
    * Port: `5432`
8. En la pestaña `Admin -> Connections` crear una nueva conexión con los siguientes datos para Spark:
    * Conn Id: `spark_default`
    * Conn Type: `Spark`
    * Host: `spark://spark`
    * Port: `7077`
    * Extra: `{"queue": "default"}`
9. En la pestaña `Admin -> Variables` crear una nueva variable con los siguientes datos:
    * Key: `driver_class_path`
    * Value: `/tmp/drivers/postgresql-42.5.2.jar`
10. En la pestaña `Admin -> Variables` crear una nueva variable con los siguientes datos:
    * Key: `spark_scripts_dir`
    * Value: `/opt/airflow/scripts`
11. En la pestaña `Admin -> Variables` crear una nueva variable con los siguientes datos:
    * Key: `raw_data_dir`
    * Value: `/opt/airflow/data/raw_data`
...
12. Ejecutar el DAG `my_dag`.

#

crear archivo `.env` colocar AIRFLOW_UID=50000

El problema de permisos en el volumen de logs y data. Solución recomendada:

```bash 
sudo chown -R 50000:50000 ./logs
sudo chown -R 50000:50000 ./data
```

Luego reinicia tus servicios:

```bash
docker-compose down
docker-compose up -d
```