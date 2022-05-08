import pyarrow.parquet as pq


file = pq.read_table("yas.parquet")
print(file.schema)
