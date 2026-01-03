"""
Bronze to Silver Layer Transformation
======================================
This script cleans and standardizes the raw retail data from Bronze layer.
- Renames messy column names to clean PascalCase format
- Parses dates to proper date type
- Casts numeric columns to appropriate types

Author: Data Engineering Portfolio
Platform: Microsoft Fabric / PySpark
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, initcap, round as spark_round, date_format
from pyspark.sql.types import IntegerType, DoubleType

# ----------------------------
# Initialize Spark Session
# ----------------------------
# Note: In Microsoft Fabric, SparkSession is already available as 'spark'
# Uncomment below for local testing:
# spark = SparkSession.builder.appName("RetailBronzeToSilver").getOrCreate()

# ----------------------------
# Configuration
# ----------------------------
# Local paths (for development/testing)
BRONZE_PATH = "data/bronze/retail_raw_data_560.json"
SILVER_PATH = "data/silver/retail_clean.parquet"

# Fabric Lakehouse paths (uncomment for production)
# BRONZE_PATH = "Files/bronze/retail_raw_data_560.json"
# SILVER_PATH = "Files/silver/retail_clean"

# ----------------------------
# Step 1: Load Bronze Data
# ----------------------------
print("Loading Bronze data...")
df_bronze = spark.read.option("multiline", "true").json(BRONZE_PATH)

print(f"Bronze records loaded: {df_bronze.count()}")
print("\nBronze Schema (raw):")
df_bronze.printSchema()

# ----------------------------
# Step 2: Rename Columns (Bronze → Silver)
# ----------------------------
print("\nApplying column renaming...")

df_silver = (
    df_bronze
    # Rename all columns to clean PascalCase format
    .withColumnRenamed("Order iD", "OrderID")
    .withColumnRenamed("order_date", "OrderDate")
    .withColumnRenamed("cust_ID", "CustomerID")
    .withColumnRenamed("Cust Segment", "CustomerSegment")
    .withColumnRenamed("region", "Region")
    .withColumnRenamed("prodct_ID", "ProductID")
    .withColumnRenamed("Prodct Category", "ProductCategory")
    .withColumnRenamed("prod_Name", "ProductName")
    .withColumnRenamed("QTY", "Quantity")
    .withColumnRenamed("price_unit", "UnitPrice")
    .withColumnRenamed("cost_unit", "CostPrice")
    .withColumnRenamed("channel", "Channel")
    .withColumnRenamed("new customer", "NewCustomer")
    .withColumnRenamed("store type", "StoreType")

    # Cast data types
    .withColumn("OrderID", col("OrderID").cast(IntegerType()))
    .withColumn("OrderDate", date_format(to_date(col("OrderDate"), "dd-MM-yyyy"), "dd-MM-yyyy"))
    .withColumn("Quantity", col("Quantity").cast(IntegerType()))
    .withColumn("UnitPrice", spark_round(col("UnitPrice").cast(DoubleType()), 2))
    .withColumn("CostPrice", spark_round(col("CostPrice").cast(DoubleType()), 2))

    # Standardize text columns (Title Case)
    .withColumn("Channel", initcap(col("Channel")))
    .withColumn("NewCustomer", initcap(col("NewCustomer")))
    .withColumn("StoreType", initcap(col("StoreType")))
)

# ----------------------------
# Step 3: Validate & Display
# ----------------------------
print("\nSilver Schema (cleaned):")
df_silver.printSchema()

print(f"\nSilver records: {df_silver.count()}")
print("\nSample Silver Data (first 10 rows):")
df_silver.show(10, truncate=False)

# ----------------------------
# Step 4: Save Silver Data
# ----------------------------
print(f"\nSaving Silver data to: {SILVER_PATH}")
df_silver.write.mode("overwrite").parquet(SILVER_PATH)

# For Fabric Delta table (uncomment for production):
# df_silver.write.mode("overwrite").format("delta").saveAsTable("silver_retail_clean")

print("\n✓ Bronze to Silver transformation complete!")
