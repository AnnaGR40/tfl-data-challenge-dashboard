# Databricks notebook source
# MAGIC
# MAGIC %run ./00_setup_config
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Purpose 
# MAGIC
# MAGIC - Add business metrics
# MAGIC
# MAGIC
# MAGIC ## Occupancy rate (main KPI)
# MAGIC
# MAGIC occupancy_rate = nb_bikes / nb_docks
# MAGIC
# MAGIC Why:
# MAGIC - Shows how “full” a station is
# MAGIC - Gives an immediate sense of balance
# MAGIC How to explain:
# MAGIC “This helps identify whether stations tend to be empty, full, or balanced.”
# MAGIC
# MAGIC ## Empty station flag 
# MAGIC
# MAGIC is_empty = nb_bikes == 0
# MAGIC
# MAGIC Why:
# MAGIC - Users can't rent bikes -> bad experience
# MAGIC
# MAGIC ## Full station flag 
# MAGIC
# MAGIC is_full = nb_empty_docks == 0
# MAGIC
# MAGIC Why:
# MAGIC Users can't return bikes -> also bad experience
# MAGIC
# MAGIC ## Capacity stress (simple version)
# MAGIC
# MAGIC capacity_stress = abs(0.5 - occupancy_rate)
# MAGIC
# MAGIC Why:
# MAGIC - Measures how “unbalanced” a station is
# MAGIC - Highlights problem stations quickly
# MAGIC
# MAGIC

# COMMAND ----------


from pyspark.sql.functions import col, when, abs

# Load Silver table
silver_df = spark.table(SILVER_TABLE)

display(silver_df)


# COMMAND ----------

gold_df = silver_df.select(
    "station_id",
    "station_name",
    "lat",
    "lon",
    "nb_bikes",
    "nb_empty_docks",
    "nb_docks",
    "snapshot_timestamp",

    # 1. Occupancy rate
    (col("nb_bikes") / col("nb_docks")).alias("occupancy_rate"),

    # 2. Empty flag
    when(col("nb_bikes") == 0, 1).otherwise(0).alias("is_empty"),

    # 3. Full flag
    when(col("nb_empty_docks") == 0, 1).otherwise(0).alias("is_full"),

    # 4. Capacity stress
    abs(0.5 - (col("nb_bikes") / col("nb_docks"))).alias("capacity_stress")
)

# COMMAND ----------

display(gold_df)

# COMMAND ----------

gold_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(GOLD_TABLE)

print("✅ Gold table created")

# COMMAND ----------

# verifications for the dashboard
spark.sql(f"SELECT COUNT(*) FROM {GOLD_TABLE}").show()

# COMMAND ----------

# verifications for the dashboard

display(spark.table(GOLD_TABLE))

# COMMAND ----------

# basic assertion - avoid dividing by zero
invalid_docks = gold_df.filter(col("nb_docks") == 0).count()

assert invalid_docks == 0, "❌ Invalid stations with zero docks"

# COMMAND ----------

# basic assertion - metric sanity
invalid_occupancy = gold_df.filter(
    (col("occupancy_rate") < 0) | (col("occupancy_rate") > 1)
).count()

assert invalid_occupancy == 0, "❌ Occupancy out of range"