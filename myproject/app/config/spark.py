from pyspark.sql import SparkSession
from config.constants import DELTA_LAKE_PATH

def create_spark_session(app_name="MyApp"):
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0") \
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore") \
        .config("spark.sql.warehouse.dir", DELTA_LAKE_PATH) \
        .getOrCreate()
    return spark

def get_delta_table_path(table_name):
    return f"{DELTA_LAKE_PATH}/{table_name}"