from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# create a new SparkSession
spark = SparkSession.builder.appName("ExampleApp").getOrCreate()

# define the schema for the DataFrame
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("city", StringType(), True)
])

# create the data for the DataFrame
data = [("Alice", 25, "New York"),
        ("Bob", 30, "London"),
        ("Charlie", 35, "Paris")]

# create the DataFrame
df = spark.createDataFrame(data, schema)
df.show()
hdfs_path = "hdfs://namenode:9000/output"
