from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import lit
from py4j.java_gateway import java_import

# create a new SparkSession
spark = SparkSession.builder.appName("ingestion_parquet_to_hive").getOrCreate()

# define source path
source_path = "hdfs://namenode:9000/input/"

# define target table
target_database = "infor"
target_table = "nation"

# check target table is exists or not
query = f"SHOW TABLES IN {target_database} LIKE '{target_table}'"
is_target_exists = spark.sql(query).count() > 0

# get max creation time in target table
if is_target_exists is True:
    max_creation_time = spark.sql(f"select max(creation_time) as max_creation_time from {target_database}.{target_table}").first()['max_creation_time']


# write parquet file to hive
def write_parquet_file_to_hive(path_file, creation_time):
    global is_target_exists       
    df = spark.read.parquet(path_file)
    df_creation_time = df.withColumn("creation_time", lit(creation_time))
    if is_target_exists is False:
        df_creation_time.write.mode("overwrite").saveAsTable(f"{target_database}.{target_table}")
    else:
        is_target_exists = True
        df_creation_time.write.mode("append").saveAsTable(f"{target_database}.{target_table}")


# get list of file in source folder at hdfs
URI           = sc._gateway.jvm.java.net.URI
Path          = sc._gateway.jvm.org.apache.hadoop.fs.Path
FileSystem    = sc._gateway.jvm.org.apache.hadoop.fs.FileSystem
Configuration = sc._gateway.jvm.org.apache.hadoop.conf.Configuration
fs = FileSystem.get(URI("hdfs://namenode:9000"), Configuration())
status_files = fs.listStatus(Path('/input/'))

# browse files in source folder in hdfs
for status_file in status_files:
    if status_file.getModificationTime() > max_creation_time:
        write_parquet_file_to_hive(str(status_file.getPath()), status_file.getModificationTime())
    