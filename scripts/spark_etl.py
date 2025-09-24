from os import environ as env
from datetime import datetime
from pyspark.sql import SparkSession

# Path del driver de Postgres para Spark (JDBC) (También sirve para Redshift)
DRIVER_PATH = env["DRIVER_MYSQL_PATH"]
# JDBC_DRIVER = "org.postgresql.Driver"
JDBC_DRIVER = "com.mysql.cj.jdbc.Driver"

# Configuración de SparkSession con soporte S3
spark = SparkSession.builder.master("local[1]") \
    .appName("ETL Spark") \
    .config("spark.jars", DRIVER_PATH) \
    .config("spark.executor.extraClassPath", DRIVER_PATH) \
    .getOrCreate()


# Conexión a MySQL
mysql_url = f"jdbc:mysql://mysql:3306/{env['MYSQL_DATABASE']}"
mysql_properties = {
    "user": env["MYSQL_USER"],
    "password": env["MYSQL_PASSWORD"],
    "driver": JDBC_DRIVER
}

print("====Step 1 - Read data from MySql database====")
try:
    # Leer una tabla de la base de datos f1db
    sql_query = """
    SELECT *
    FROM f1db.circuits
    """

    df = spark.read \
        .format("jdbc") \
        .option("url", mysql_url) \
        .option("driver", mysql_properties["driver"]) \
        .option("query", sql_query) \
        .option("user", mysql_properties["user"]) \
        .option("password", mysql_properties["password"]) \
        .load()

    print("\n✅ Connection successful")
except Exception as e:
    print(f"\n❌ Connection failed: {str(e)}")

# Mostrar el esquema y las primeras filas del DataFrame
print("\n====Mostrar el esquema y las primeras filas del DataFrame====")
df.show(10, truncate=False)
print(f"\n====Total records====\n{df.count()}")
print(f"\n====Schema====")
df.printSchema()

print("\n====Step 2 - Write data to datalake as csv====")
spark.sparkContext.stop()