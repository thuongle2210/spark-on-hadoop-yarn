import pyarrow as pa
import pandas as pd

import pyarrow.parquet as pq

# Create a PyArrow table with sample data
data = {
    'id': [1, 2, 3],
    'value': ['A', 'B', 'C']
}
df = pd.DataFrame(data)

table = pa.Table.from_pandas(df)

# Define the HDFS path where you want to store the Parquet file
hdfs_path = 'hdfs://namenode:9000/input'

# Write the table to Parquet file on HDFS
pq.write_to_dataset(table, hdfs_path)
