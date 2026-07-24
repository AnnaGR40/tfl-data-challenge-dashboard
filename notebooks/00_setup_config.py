# Databricks notebook source
# Database / schema
CATALOG = "workspace"   # this is my current catalog 
SCHEMA = "bikepoint_db"


spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")


# Table names
BRONZE_TABLE = f"{CATALOG}.{SCHEMA}.bronze_bikepoints"
SILVER_TABLE = f"{CATALOG}.{SCHEMA}.silver_bikepoints"
GOLD_TABLE = f"{CATALOG}.{SCHEMA}.gold_bikepoints"

# Paths (if you prefer storage instead of tables)
BASE_PATH = "/mnt/bikepoint"
BRONZE_PATH = f"{BASE_PATH}/bronze"
SILVER_PATH = f"{BASE_PATH}/silver"
GOLD_PATH = f"{BASE_PATH}/gold"

# API config
API_BASE_URL = "https://api.tfl.gov.uk/BikePoint/"

# Ingestion settings
INGESTION_MODE = "append"  # important for future historical tracking

# Debug mode
DEBUG = True

print("Configuration loaded")
print(f"Schema: {SCHEMA}")
print(f"Bronze table: {BRONZE_TABLE}")
