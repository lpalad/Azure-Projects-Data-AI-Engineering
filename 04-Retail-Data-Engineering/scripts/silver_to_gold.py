"""
Silver to Gold Layer Transformation
====================================
This script aggregates the cleaned Silver data into business-ready Gold metrics.
- Groups by key dimensions (Region, Segment, Category, Channel, StoreType)
- Calculates KPIs (TotalSales, GrossProfit, ProfitMargin, etc.)
- Adds time dimensions (Year, Quarter, Month)

Author: Data Engineering Portfolio
Platform: Microsoft Fabric / PySpark
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum as spark_sum, count, countDistinct, avg,
    round as spark_round, to_date, year, quarter, month
)

# ----------------------------
# Initialize Spark Session
# ----------------------------
# Note: In Microsoft Fabric, SparkSession is already available as 'spark'
# Uncomment below for local testing:
# spark = SparkSession.builder.appName("RetailSilverToGold").getOrCreate()

# ----------------------------
# Configuration
# ----------------------------
# Local paths (for development/testing)
SILVER_PATH = "data/silver/retail_clean.parquet"
GOLD_PATH = "data/gold/retail_metrics.parquet"

# Fabric Lakehouse paths (uncomment for production)
# SILVER_PATH = "Files/silver/retail_clean"
# GOLD_PATH = "Files/gold/retail_metrics"

# ----------------------------
# Step 1: Load Silver Data
# ----------------------------
print("Loading Silver data...")
df_silver = spark.read.parquet(SILVER_PATH)

# If loading from CSV instead:
# df_silver = spark.read.option("header", "true").csv("data/silver/retail_clean.csv")

print(f"Silver records loaded: {df_silver.count()}")

# ----------------------------
# Step 2: Add Calculated Columns
# ----------------------------
print("\nAdding calculated columns...")

df_enriched = (
    df_silver
    # Calculate sales and cost amounts
    .withColumn("SalesAmount", spark_round(col("Quantity") * col("UnitPrice"), 2))
    .withColumn("CostAmount", spark_round(col("Quantity") * col("CostPrice"), 2))

    # Extract time dimensions from OrderDate
    .withColumn("OrderDateParsed", to_date(col("OrderDate"), "dd-MM-yyyy"))
    .withColumn("Year", year(col("OrderDateParsed")))
    .withColumn("Quarter", quarter(col("OrderDateParsed")))
    .withColumn("Month", month(col("OrderDateParsed")))
)

# ----------------------------
# Step 3: Aggregate to Gold Layer
# ----------------------------
print("Aggregating to Gold layer...")

df_gold = (
    df_enriched
    .groupBy(
        "Region",
        "CustomerSegment",
        "ProductCategory",
        "Channel",
        "StoreType",
        "Year",
        "Quarter",
        "Month"
    )
    .agg(
        # Sales metrics
        spark_round(spark_sum("SalesAmount"), 2).alias("TotalSales"),
        spark_round(spark_sum("CostAmount"), 2).alias("TotalCost"),
        spark_round(spark_sum("SalesAmount") - spark_sum("CostAmount"), 2).alias("GrossProfit"),

        # Order metrics
        count("OrderID").alias("OrderCount"),
        countDistinct("CustomerID").alias("CustomerCount"),
        spark_round(spark_sum("SalesAmount") / count("OrderID"), 2).alias("AvgOrderValue"),

        # Quantity metrics
        spark_sum("Quantity").alias("TotalQuantity"),

        # Profit margin (%)
        spark_round(
            ((spark_sum("SalesAmount") - spark_sum("CostAmount")) / spark_sum("SalesAmount")) * 100, 2
        ).alias("ProfitMargin")
    )
    .orderBy("Year", "Quarter", "Month", "Region")
)

# ----------------------------
# Step 4: Validate & Display
# ----------------------------
print("\nGold Schema:")
df_gold.printSchema()

print(f"\nGold records (aggregated): {df_gold.count()}")
print("\nSample Gold Data (first 20 rows):")
df_gold.show(20, truncate=False)

# ----------------------------
# Step 5: Save Gold Data
# ----------------------------
print(f"\nSaving Gold data to: {GOLD_PATH}")
df_gold.write.mode("overwrite").parquet(GOLD_PATH)

# For Fabric Delta table (uncomment for production):
# df_gold.write.mode("overwrite").format("delta").saveAsTable("gold_retail_metrics")

print("\n✓ Silver to Gold transformation complete!")
