"""
Medallion Data Pipeline - PySpark Version for Microsoft Fabric
===============================================================
This script processes raw data through the Medallion architecture using PySpark.
Copy this code into a Fabric Notebook to execute.

Layers:
- BRONZE: Raw data ingestion (as-is from source)
- SILVER: Cleaned and standardized data
- GOLD: (Done in Power BI)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# =============================================================================
# CONFIGURATION - Update these paths for your Fabric Lakehouse
# =============================================================================
# Example Fabric path: "abfss://medallion@onelake.dfs.fabric.microsoft.com/medallion.Lakehouse/Files/"
LAKEHOUSE_PATH = "Files/"  # Relative path in Fabric Notebook
BRONZE = f"{LAKEHOUSE_PATH}bronze/"
SILVER = f"{LAKEHOUSE_PATH}silver/"


# =============================================================================
# BRONZE LAYER - Read Raw Data
# =============================================================================
print("="*70)
print("BRONZE LAYER - Reading Raw Data")
print("="*70)

# Read Orders CSV
df_orders_raw = spark.read.option("header", "true").csv(f"{BRONZE}orders_data.csv")
print(f"Orders: {df_orders_raw.count()} rows")

# Read Inventory JSON
df_inventory_raw = spark.read.json(f"{BRONZE}inventory_data.json")
print(f"Inventory: {df_inventory_raw.count()} rows")

# Read Returns (if converted to CSV/Parquet - Excel not directly supported)
# Option 1: Convert Excel to CSV first, then read
# Option 2: Use pandas to read Excel, then convert to Spark DataFrame
df_returns_raw = spark.read.option("header", "true").csv(f"{BRONZE}returns_data.csv")
print(f"Returns: {df_returns_raw.count()} rows")


# =============================================================================
# SILVER LAYER - Clean Orders
# =============================================================================
print("\n" + "="*70)
print("SILVER LAYER - Cleaning Orders")
print("="*70)

df_orders = (
    df_orders_raw

    # 1. Rename columns to standardized names
    .withColumnRenamed("Order_ID", "OrderID")
    .withColumnRenamed("cust_id", "CustomerID")
    .withColumnRenamed("Product_Name", "ProductName")
    .withColumnRenamed("Qty", "Quantity")
    .withColumnRenamed("Order_Date", "OrderDate")
    .withColumnRenamed("Order_Amount$", "OrderAmount")
    .withColumnRenamed("Delivery_Status", "DeliveryStatus")
    .withColumnRenamed("Payment_Mode", "PaymentMode")
    .withColumnRenamed("Ship_Address", "ShipAddress")
    .withColumnRenamed("Promo_Code", "PromoCode")
    .withColumnRenamed("Feedback_Score", "FeedbackScore")

    # 2. Clean Quantity: convert words ('one', 'Two', 'THREE') to integers
    .withColumn("Quantity",
        when(lower(col("Quantity")) == "one", 1)
        .when(lower(col("Quantity")) == "two", 2)
        .when(lower(col("Quantity")) == "three", 3)
        .when(lower(col("Quantity")) == "four", 4)
        .when(lower(col("Quantity")) == "five", 5)
        .otherwise(col("Quantity").cast(IntegerType()))
    )

    # 3. Clean OrderDate: parse multiple date formats
    .withColumn("OrderDate", coalesce(
        to_date(col("OrderDate"), "yyyy/MM/dd"),
        to_date(col("OrderDate"), "dd-MM-yyyy"),
        to_date(col("OrderDate"), "MM-dd-yyyy"),
        to_date(col("OrderDate"), "yyyy.MM.dd"),
        to_date(col("OrderDate"), "dd/MM/yyyy"),
        to_date(col("OrderDate"), "dd.MM.yyyy"),
        to_date(col("OrderDate"), "MMMM dd yyyy")
    ))

    # 4. Clean OrderAmount: remove currency symbols ($, ₹, Rs., USD, INR)
    .withColumn("OrderAmount", regexp_replace(col("OrderAmount"), r"[$₹Rs.USD,INR\s]", ""))
    .withColumn("OrderAmount", col("OrderAmount").cast(DoubleType()))

    # 5. Clean PaymentMode: lowercase, remove special characters
    .withColumn("PaymentMode", lower(regexp_replace(col("PaymentMode"), r"[^a-zA-Z]", "")))

    # 6. Clean DeliveryStatus: lowercase, remove special characters
    .withColumn("DeliveryStatus", lower(regexp_replace(col("DeliveryStatus"), r"[^a-zA-Z ]", "")))

    # 7. Validate Email: keep only valid emails, set invalid to null
    .withColumn("Email",
        when(col("Email").rlike(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"), col("Email"))
        .otherwise(lit(None))
    )

    # 8. Clean ShipAddress: remove special characters (#, @, !, $)
    .withColumn("ShipAddress", regexp_replace(col("ShipAddress"), r"[#@!$]", ""))

    # 9. Clean FeedbackScore: convert to double
    .withColumn("FeedbackScore", col("FeedbackScore").cast(DoubleType()))

    # 10. Fill null values with defaults
    .fillna({"Quantity": 0, "OrderAmount": 0.0, "DeliveryStatus": "unknown", "PaymentMode": "unknown"})

    # 11. Drop rows where CustomerID or ProductName is null
    .na.drop(subset=["CustomerID", "ProductName"])

    # 12. Remove duplicates by OrderID
    .dropDuplicates(["OrderID"])
)

print(f"Orders cleaned: {df_orders.count()} rows")
display(df_orders.limit(5))

# Save to Silver as Delta table
df_orders.write.mode("overwrite").format("delta").saveAsTable("silver_orders")


# =============================================================================
# SILVER LAYER - Clean Inventory
# =============================================================================
print("\n" + "="*70)
print("SILVER LAYER - Cleaning Inventory")
print("="*70)

df_inventory = (
    df_inventory_raw

    # 1. Rename columns
    .withColumnRenamed("product_id", "ProductID")
    .withColumnRenamed("productName", "ProductName")
    .withColumnRenamed("cost_price", "CostPrice")
    .withColumnRenamed("last_stocked", "LastStocked")

    # 2. Clean Stock: convert words to numbers, extract numeric part
    .withColumn("Stock",
        when(col("stock").rlike(r"^\d+$"), col("stock").cast(IntegerType()))
        .when(col("stock").isNull() | (col("stock") == "") | (col("stock") == "null"), lit(None))
        .when(lower(col("stock")).contains("twenty five"), lit(25))
        .when(lower(col("stock")).contains("twenty"), lit(20))
        .when(lower(col("stock")).contains("eighteen"), lit(18))
        .when(lower(col("stock")).contains("fifteen"), lit(15))
        .when(lower(col("stock")).contains("twelve"), lit(12))
        .when(lower(col("stock")).contains("ten"), lit(10))
        .otherwise(regexp_extract(col("stock"), r"(\d+)", 1).cast(IntegerType()))
    )

    # 3. Clean LastStocked: parse multiple date formats
    .withColumn("LastStocked", coalesce(
        to_date(col("LastStocked"), "yyyy/MM/dd"),
        to_date(col("LastStocked"), "dd-MM-yyyy"),
        to_date(col("LastStocked"), "yyyy.MM.dd"),
        to_date(col("LastStocked"), "dd.MM.yyyy"),
        to_date(col("LastStocked"), "yyyy-MM-dd")
    ))

    # 4. Clean CostPrice: extract numeric value
    .withColumn("CostPrice", regexp_extract(col("CostPrice"), r"(\d+\.?\d*)", 1).cast(DoubleType()))

    # 5. Clean Warehouse: remove special characters, capitalize
    .withColumn("Warehouse", initcap(trim(regexp_replace(col("warehouse"), r"[#@!$_]", " "))))

    # 6. Clean Available: convert to boolean
    .withColumn("Available",
        when(lower(col("available")).isin("yes", "y", "true", "1"), lit(True))
        .when(lower(col("available")).isin("no", "n", "false", "0"), lit(False))
        .otherwise(lit(None))
    )

    # Drop old columns
    .drop("stock", "warehouse", "available")
)

print(f"Inventory cleaned: {df_inventory.count()} rows")
display(df_inventory.limit(5))

# Save to Silver as Delta table
df_inventory.write.mode("overwrite").format("delta").saveAsTable("silver_inventory")


# =============================================================================
# SILVER LAYER - Clean Returns
# =============================================================================
print("\n" + "="*70)
print("SILVER LAYER - Cleaning Returns")
print("="*70)

df_returns = (
    df_returns_raw

    # 1. Rename columns
    .withColumnRenamed("Return_ID", "ReturnID")
    .withColumnRenamed("Order_ID", "OrderID")
    .withColumnRenamed("Customer_ID", "CustomerID")
    .withColumnRenamed("Return_Reason", "ReturnReason")
    .withColumnRenamed("Return_Date", "ReturnDate")
    .withColumnRenamed("Refund_Status", "RefundStatus")
    .withColumnRenamed("Pickup_Address", "PickupAddress")
    .withColumnRenamed("Return_Amount", "ReturnAmount")

    # 2. Clean CustomerID: trim and uppercase
    .withColumn("CustomerID", upper(trim(col("CustomerID"))))

    # 3. Clean Product: remove special chars, title case
    .withColumn("Product", initcap(trim(regexp_replace(col("Product"), r"[^a-zA-Z0-9\s]", ""))))

    # 4. Clean ReturnDate: parse multiple date formats
    .withColumn("ReturnDate", coalesce(
        to_date(col("ReturnDate"), "dd-MM-yyyy"),
        to_date(col("ReturnDate"), "yyyy/MM/dd"),
        to_date(col("ReturnDate"), "yyyy.MM.dd"),
        to_date(col("ReturnDate"), "dd.MM.yyyy"),
        to_date(col("ReturnDate"), "dd/MM/yyyy"),
        to_date(col("ReturnDate"), "MMMM dd yyyy")
    ))

    # 5. Clean RefundStatus: lowercase, remove special chars
    .withColumn("RefundStatus", lower(regexp_replace(col("RefundStatus"), r"[^a-zA-Z]", "")))

    # 6. Clean PickupAddress: remove special chars, title case
    .withColumn("PickupAddress", initcap(trim(regexp_replace(col("PickupAddress"), r"[#@!$]", " "))))

    # 7. Clean ReturnAmount: extract numeric value
    .withColumn("ReturnAmount", regexp_extract(col("ReturnAmount"), r"(\d+\.?\d*)", 1).cast(DoubleType()))
)

print(f"Returns cleaned: {df_returns.count()} rows")
display(df_returns.limit(5))

# Save to Silver as Delta table
df_returns.write.mode("overwrite").format("delta").saveAsTable("silver_returns")


# =============================================================================
# GOLD LAYER - Join Tables
# =============================================================================
print("\n" + "="*70)
print("GOLD LAYER - Joining Tables")
print("="*70)

# Load Silver tables with aliases
orders = spark.table("silver_orders").alias("o")
returns = spark.table("silver_returns").alias("r")
inventory = spark.table("silver_inventory").alias("i")

# LEFT JOIN: Orders + Returns (on OrderID)
# LEFT JOIN: + Inventory (on ProductName)
# Why LEFT JOIN? Keep ALL orders, even if no return or no inventory match

gold_joined = (
    orders
    .join(returns, col("o.OrderID") == col("r.OrderID"), "left")
    .join(inventory, col("o.ProductName") == col("i.ProductName"), "left")
    .select(
        # From Orders
        col("o.OrderID"),
        col("o.CustomerID"),
        col("o.ProductName"),
        col("o.Quantity"),
        col("o.OrderDate"),
        col("o.OrderAmount"),
        col("o.DeliveryStatus"),
        col("o.PaymentMode"),
        col("o.ShipAddress"),
        col("o.Email"),
        col("o.PromoCode"),
        col("o.FeedbackScore"),
        # From Returns
        col("r.ReturnID"),
        col("r.ReturnAmount"),
        col("r.RefundStatus"),
        col("r.ReturnReason"),
        # From Inventory
        col("i.Stock"),
        col("i.CostPrice"),
        col("i.Available")
    )
)

print(f"Gold joined table: {gold_joined.count()} rows")
display(gold_joined.limit(10))

# Save to Gold as Delta table
gold_joined.write.mode("overwrite").format("delta").saveAsTable("gold_joined")

# Also save as Parquet file for easy export
gold_joined.write.mode("overwrite").parquet(f"{LAKEHOUSE_PATH}gold/gold_joined.parquet")

print("✓ Saved to: gold_joined (Delta table)")
print(f"✓ Saved to: {LAKEHOUSE_PATH}gold/gold_joined.parquet")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*70)
print("PIPELINE COMPLETE!")
print("="*70)
print("""
Bronze Layer (Raw):
  - orders_data.csv
  - inventory_data.json
  - returns_data.csv

Silver Layer (Clean Delta Tables):
  - silver_orders
  - silver_inventory
  - silver_returns

Gold Layer (Joined Table):
  - gold_joined (Delta table)
  - gold/gold_joined.parquet

Next Step:
  - Create Semantic Model in Fabric
  - Connect Power BI to gold_joined table for KPI reporting
""")
