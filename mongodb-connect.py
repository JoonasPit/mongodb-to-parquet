import os
import pymongo as pmg
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
import json

table_definitions = {"Schema": "Foo_schema", "Table" : "new_table"}

def initialize_parquet_file(df):
    del df["_id"]
    table = pa.Table.from_pandas(df)
    
    custom_meta = json.dumps(table_definitions)
    existing_meta = table.schema.metadata
    combined_meta = {
        "custom_metadata".encode() : custom_meta.encode(),
        **existing_meta
    }
    output_ready_parquet = table.replace_schema_metadata(combined_meta)
    return output_ready_parquet

def mongodb_connect():
    database_connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    mongocnt = pmg.MongoClient(database_connection_string)
    return mongocnt

def main():
    mongodb_client = mongodb_connect()
    mydb = mongodb_client["foo_db"]
    mycol = mydb["tests"]

    all_documents_in_database = mycol.find({})

    listed_document_data = list(all_documents_in_database)
    df = pd.DataFrame(listed_document_data)
    final_product = initialize_parquet_file(df)

    snowflake_table_name = table_definitions.get("Table")
    pq.write_table(final_product, f'{snowflake_table_name}.parquet')


if __name__ == "__main__":
    main()