from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import datetime
# create a new SparkSession
spark = SparkSession.builder.appName("ingestion_postgres_to_hive_latest_version").getOrCreate()

# define ingestion date
ingestion_date = datetime.date(2023, 1, 1)

# define source table in postgresql
source_database = "metastore"
source_table = "dacthuong"

# define target table in hive
target_database = "infor"
target_table = "dacthuong"

# write parquet file to hive
def write_data_from_postgres_to_hive(source_database, source_table, target_database, target_table, ingestion_date):
    # check target table is exists or not
    query = f"SHOW TABLES IN {target_database} LIKE '{target_table}'"
    is_target_exists = spark.sql(query).count() > 0
    # get max updated_at
    if is_target_exists is True:
        # get target dataframe
        spark.sql(f"CREATE OR REPLACE TEMPORARY VIEW target_table AS SELECT * FROM {target_database}.{target_table}")
        #spark.table(f"{target_database}.{target_table}").createOrReplaceTempView("target_table")
        target_df = spark.sql("select * from target_table");
        max_updated_at = spark.sql(f"select max(updated_at) as max_updated_at from target_table").first()['max_updated_at']
    # Define PostgreSQL connection properties
    # get source dataframe
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
        latest_record_df = df
    else:
        latest_record_df = df.filter(df["updated_at"] >= max_updated_at)
    # deduplicate row in latest record
    window_spec = Window.partitionBy("id").orderBy(col("updated_at").desc())
    deduplicate_latest_record_df = latest_record_df.withColumn("rank", row_number().over(window_spec)) \
              .filter("rank = 1").drop("rank")
    
    # merge distinct latest record to exists table in hive
    if is_target_exists is True:
        result_df = target_df.alias('t').join(
            deduplicate_latest_record_df.alias('d'),
            target_df.id == deduplicate_latest_record_df.id,
            'full'
        ).select(
            #coalesce("d.id", "t.id").alias("id"),
            "t.*"
        )
        # write result_df to hive table
        result_df.write.mode("overwrite").mode("overwrite").saveAsTable(f"{target_database}.{target_table}_temp")
        spark.sql(f"use {target_database}")
        spark.sql(f"drop table {target_table}")
        spark.sql(f"ALTER TABLE {target_table}_temp RENAME TO {target_database}.{target_table}")
        #result_df.write.mode("overwrite").saveAsTable(f"{target_database}.{target_table}")
    else:
        deduplicate_latest_record_df.write.mode("overwrite").saveAsTable(f"{target_database}.{target_table}")

if __name__ == '__main__':
    write_data_from_postgres_to_hive(source_database, source_table, target_database, target_table, ingestion_date)
