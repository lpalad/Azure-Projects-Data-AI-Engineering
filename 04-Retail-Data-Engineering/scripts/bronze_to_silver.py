"""
Bronze to Silver Layer Transformation
======================================
This script cleans and standardizes the raw retail data from Bronze layer.
- Renames messy column names to clean PascalCase format
- Parses dates to proper date type
- Casts numeric columns to appropriate types
- Includes data quality validation checks

Author: Data Engineering Portfolio
Platform: Microsoft Fabric / PySpark
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, initcap, round as spark_round, date_format
from pyspark.sql.types import IntegerType, DoubleType
import sys

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

# Required columns in Bronze layer
REQUIRED_COLUMNS = [
    "Order iD", "order_date", "cust_ID", "Cust Segment", "region",
    "prodct_ID", "Prodct Category", "prod_Name", "QTY", "price_unit",
    "cost_unit", "channel", "new customer", "store type"
]


# ----------------------------
# Data Quality Functions
# ----------------------------
def run_data_quality_checks(df, stage="Bronze"):
    """
    Run data quality validation checks on the DataFrame.
    Returns True if all checks pass, False otherwise.
    """
    print("\n" + "=" * 50)
    print(f"  DATA QUALITY CHECKS - {stage} Layer")
    print("=" * 50)

    checks_passed = True
    row_count = df.count()

    # Check 1: Row count > 0
    if row_count > 0:
        print(f"✓ Row count: {row_count} rows (PASS)")
    else:
        print(f"✗ Row count: {row_count} rows (FAIL)")
        checks_passed = False

    # Check 2: Required columns exist
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if len(missing_cols) == 0:
        print(f"✓ Required columns: {len(REQUIRED_COLUMNS)}/{len(REQUIRED_COLUMNS)} present (PASS)")
    else:
        print(f"✗ Missing columns: {missing_cols} (FAIL)")
        checks_passed = False

    # Check 3: Null check on key columns
    null_order_id = df.filter(col("Order iD").isNull()).count()
    if null_order_id == 0:
        print(f"✓ Null check: OrderID has {null_order_id} nulls (PASS)")
    else:
        print(f"✗ Null check: OrderID has {null_order_id} nulls (FAIL)")
        checks_passed = False

    null_cust_id = df.filter(col("cust_ID").isNull()).count()
    if null_cust_id == 0:
        print(f"✓ Null check: CustomerID has {null_cust_id} nulls (PASS)")
    else:
        print(f"✗ Null check: CustomerID has {null_cust_id} nulls (FAIL)")
        checks_passed = False

    # Check 4: Value range checks
    negative_qty = df.filter(col("QTY") <= 0).count()
    if negative_qty == 0:
        print(f"✓ Value check: No invalid quantities (PASS)")
    else:
        print(f"⚠ Value check: {negative_qty} rows with quantity <= 0 (WARNING)")

    negative_price = df.filter(col("price_unit") <= 0).count()
    if negative_price == 0:
        print(f"✓ Value check: No negative/zero prices (PASS)")
    else:
        print(f"⚠ Value check: {negative_price} rows with price <= 0 (WARNING)")

    print("=" * 50)

    if checks_passed:
        print("✓ All critical data quality checks PASSED")
    else:
        print("✗ Some data quality checks FAILED")

    print("=" * 50 + "\n")

    return checks_passed


# ----------------------------
# Step 1: Load Bronze Data
# ----------------------------
print("Loading Bronze data...")
df_bronze = spark.read.option("multiline", "true").json(BRONZE_PATH)

# ----------------------------
# Step 2: Run Data Quality Checks
# ----------------------------
quality_passed = run_data_quality_checks(df_bronze, "Bronze")

if not quality_passed:
    print("ERROR: Data quality checks failed. Pipeline stopped.")
    sys.exit(1)

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
