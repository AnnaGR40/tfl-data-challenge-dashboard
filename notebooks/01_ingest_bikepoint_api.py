# Databricks notebook source
# MAGIC %run ./00_setup_config

# COMMAND ----------

# MAGIC %md
# MAGIC # Purpose
# MAGIC
# MAGIC - call the API
# MAGIC - load raw data into a dataframe
# MAGIC - prepare it for Bronze (but does NOT write yet)

# COMMAND ----------

import requests
from pyspark.sql.functions import current_timestamp, to_json, struct, col
import json

# Call API
response = requests.get(API_BASE_URL)

# Basic check
if response.status_code != 200:
    raise Exception(f"API call failed with status {response.status_code}")

# Convert to JSON
data = response.json()

if DEBUG:
    print(f"Number of records fetched: {len(data)}")

# Convert JSON to string and read as single-column DataFrame
json_strings = [json.dumps(record) for record in data]
raw_df = spark.createDataFrame([(s,) for s in json_strings], ["json_data"])

# Add ingestion timestamp
raw_df = raw_df.withColumn("ingestion_timestamp", current_timestamp())

# Preview
display(raw_df)