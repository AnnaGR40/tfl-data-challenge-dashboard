# Databricks notebook source
# MAGIC %run ./00_setup_config

# COMMAND ----------

# MAGIC %run ./01_ingest_bikepoint_api
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Bronze Layer (Raw Ingestion)
# MAGIC ## Purpose
# MAGIC - Store API data as-is
# MAGIC - Preserve raw structure for traceability
# MAGIC ## What is stored
# MAGIC - Full JSON response
# MAGIC - Added ingestion_timestamp

# COMMAND ----------


# Write to Bronze table in Unity Catalog

# Write to Unity Catalog table
raw_df.write \
    .format("delta") \
    .mode(INGESTION_MODE) \
    .saveAsTable(f"workspace.{SCHEMA}.bronze_bikepoints")

print("Data written to Bronze layer")


# COMMAND ----------

# validate

spark.sql(f"SELECT COUNT(*) FROM {BRONZE_TABLE}").show()


# COMMAND ----------

display(spark.table(BRONZE_TABLE))


# COMMAND ----------

# basic assertion - data quality check
row_count = spark.table(BRONZE_TABLE).count()

assert row_count > 0, "❌ Bronze table is empty"
print("✅ Bronze data loaded:", row_count)
