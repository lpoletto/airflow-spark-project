`mkdir -p ./dags ./logs ./plugins ./config ./scripts ./spark_drivers`

crear archivo `.env` colocar AIRFLOW_UID=50000
El problema es de permisos en el volumen de logs.

Solución recomendada: sudo chown -R 50000:50000 ./logs

Luego reinicia tus servicios:

docker-compose down
docker-compose up -d