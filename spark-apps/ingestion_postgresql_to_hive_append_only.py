from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import lit, to_date
import datetime
# create a new SparkSession
spark = SparkSession.builder.appName("ingestion_postgres_to_hive").getOrCreate()

# define ingestion date
ingestion_date = datetime.date(2023, 1, 1)

# define source table in postgresql
source_database = "metastore"
source_table = "quynhuong"

# define target table in hive
target_database = "infor"
target_table = "quynhuong"

# write parquet file to hive
def write_data_from_postgres_to_hive(source_database, source_table, target_database, target_table, ingestion_date):
    # check target table is exists or not
    query = f"SHOW TABLES IN {target_database} LIKE '{target_table}'"
    is_target_exists = spark.sql(query).count() > 0
    # get max id
    if is_target_exists is True:
        max_id = spark.sql(f"select max(id) as max_id from {target_database}.{target_table}").first()['max_id']
    # Define PostgreSQL connection properties
    jdbc_url = f"jdbc:postgresql://metastore:5432/{source_database}"
    connection_properties = {
        "user": "thuong",
        "password": "thuong",
        "driver": "org.postgresql.Driver"
    }
    df = spark.read.jdbc(url=jdbc_url, table=source_table, properties=connection_properties)
    # add extract_date column
    ingestion_date_string = ingestion_date.strftime("%Y-%m-%d") 
    # append or overwrite data from postgresql to hive
    if is_target_exists is False:
        df_extract_date = df.withColumn("extract_date", to_date(lit(ingestion_date_string)))
        df_extract_date.write.mode("overwrite").saveAsTable(f"{target_database}.{target_table}")
    else:
        is_target_exists = True
        latest_record_df = df.filter(df["id"] > max_id)
        df_extract_date = latest_record_df.withColumn("extract_date", to_date(lit(ingestion_date_string)))
        df_extract_date.write.mode("append").saveAsTable(f"{target_database}.{target_table}")

if __name__ == '__main__':
    write_data_from_postgres_to_hive(source_database, source_table, target_database, target_table, ingestion_date)
