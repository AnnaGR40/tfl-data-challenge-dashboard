# Databricks notebook source
# MAGIC
# MAGIC %run ./00_setup_config

# COMMAND ----------

# MAGIC %md
# MAGIC # Purpose
# MAGIC
# MAGIC - parse json_data
# MAGIC - extract core fields (id, name, lat, lon)
# MAGIC - flatten additionalProperties
# MAGIC - create structured columns: 
# MAGIC                         - nb_bikes
# MAGIC                         - nb_empty_docks
# MAGIC                         - nb_docks
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *

# Load Bronze table
bronze_df = spark.table(BRONZE_TABLE)


# COMMAND ----------

# define schema for the json data
schema = StructType([
    StructField("id", StringType(), True),
    StructField("commonName", StringType(), True),
    StructField("lat", DoubleType(), True),
    StructField("lon", DoubleType(), True),
    StructField("additionalProperties", ArrayType(
        StructType([
            StructField("key", StringType(), True),
            StructField("value", StringType(), True)
        ])
    ), True)
])


# COMMAND ----------

# parse json data
bikepoint = bronze_df.withColumn(
    "parsed_json",
    from_json(col("json_data"), schema)
)

# COMMAND ----------

# DBTITLE 1,Cell 6
# extract top level columns

base_df = bikepoint.select(
    col("parsed_json.id").alias("station_id"),
    col("parsed_json.commonName").alias("station_name"),
    col("parsed_json.lat"),
    col("parsed_json.lon"),
    col("parsed_json.additionalProperties"),
    col("ingestion_timestamp")
)


# COMMAND ----------

display(base_df)

# COMMAND ----------

# explode array
from pyspark.sql.functions import explode

exploded_df = base_df.withColumn(
    "prop",
    explode(col("additionalProperties"))
)

display(exploded_df)


# COMMAND ----------

# extract key-value
kv_df = exploded_df.select(
    "station_id",
    "station_name",
    "lat",
    "lon",
    "ingestion_timestamp",
    col("prop.key").alias("key"),
    col("prop.value").alias("value")
)

display(kv_df)


# COMMAND ----------

# pivot key-value pairs into columns

silver_df = kv_df.groupBy(
    "station_id",
    "station_name",
    "lat",
    "lon",
    "ingestion_timestamp"
).pivot("key").agg({"value": "first"})

# COMMAND ----------

# clean rename columns
from pyspark.sql.functions import col

silver_final = silver_df.select(
    "station_id",
    "station_name",
    "lat",
    "lon",
    col("NbBikes").cast("int").alias("nb_bikes"),
    col("NbEmptyDocks").cast("int").alias("nb_empty_docks"),
    col("NbDocks").cast("int").alias("nb_docks"),
    col("ingestion_timestamp").alias("snapshot_timestamp")
)
display(silver_final)


# COMMAND ----------

# write to silver table
silver_final.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(SILVER_TABLE)

print("Silver table created")


# COMMAND ----------

# basic assertion - data quality check -no missing key fields
invalid_rows = silver_final.filter(
    col("station_id").isNull() | col("station_name").isNull()
).count()

assert invalid_rows == 0, "❌ Missing station IDs or names"


# COMMAND ----------

# basic assertion - data quality check -valid numeric values
invalid_bikes = silver_final.filter(col("nb_bikes") < 0).count()
assert invalid_bikes == 0, "❌ Negative bike values found"


# COMMAND ----------

# DBTITLE 1,Cell 15
# basic assertion - data quality check -consistency check
invalid_capacity = silver_final.filter(
    col("nb_bikes") + col("nb_empty_docks") != col("nb_docks")
).count()

if invalid_capacity > 0:
    print(f"⚠️ Warning: {invalid_capacity} rows have inconsistent dock counts (nb_bikes + nb_empty_docks != nb_docks)")
else:
    print("✅ All rows have consistent dock counts")