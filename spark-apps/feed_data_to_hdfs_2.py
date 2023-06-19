from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# create a new SparkSession
spark = SparkSession.builder.appName("ExampleApp2").getOrCreate()

# define the schema for the DataFrame
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("value", StringType(), True)
])

# create the data for the DataFrame
data = [(4, "Ho Chi Minh"),
        (5, "Thai Lan"),
        (6, "Singapore")]

# create the DataFrame
df = spark.createDataFrame(data, schema)
df.show()
hdfs_path = "hdfs://namenode:9000/input/file_2.parquet"
df.write.parquet(hdfs_path)