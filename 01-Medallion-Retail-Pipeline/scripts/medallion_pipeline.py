"""
Medallion Data Pipeline - Bronze to Silver
===========================================
This script processes raw data through the Medallion architecture:
- BRONZE: Raw data ingestion (as-is from source)
- SILVER: Cleaned and standardized data

Run: python medallion_pipeline.py
"""

import pandas as pd
import numpy as np
import re
import os

# =============================================================================
# CONFIGURATION
# =============================================================================
BASE_PATH = "/Volumes/SSD-CRUCIAL/Medallion/Local_Lakehouse"
BRONZE = f"{BASE_PATH}/bronze"
SILVER = f"{BASE_PATH}/silver"

# Ensure directories exist
os.makedirs(BRONZE, exist_ok=True)
os.makedirs(SILVER, exist_ok=True)


# =============================================================================
# HELPER FUNCTIONS - Reusable cleaning functions
# =============================================================================

def clean_quantity(qty):
    """
    Convert quantity to integer.
    Handles: 'one', 'Two', 'THREE', '02', '', NaN
    """
    if pd.isna(qty):
        return 0
    qty_str = str(qty).lower().strip()
    word_map = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }
    if qty_str in word_map:
        return word_map[qty_str]
    try:
        return int(float(qty_str))
    except:
        return 0


def clean_stock(stock):
    """
    Convert stock to integer.
    Handles: '25 units', 'twenty', 'twenty five', '', null
    """
    if pd.isna(stock) or stock == '' or stock == 'null':
        return None
    stock_str = str(stock).lower().strip()

    word_map = {
        'twenty five': 25, 'twenty': 20, 'eighteen': 18,
        'fifteen': 15, 'twelve': 12, 'ten': 10
    }
    for word, num in word_map.items():
        if word in stock_str:
            return num

    match = re.search(r'(\d+)', stock_str)
    if match:
        return int(match.group(1))
    return None


def clean_date(date_str):
    """
    Parse multiple date formats into standardized datetime.
    Handles: 2023/06/12, 12-07-2023, 2023.07.15, July 20th 2023
    """
    if pd.isna(date_str):
        return None
    date_str = str(date_str).strip()
    # Remove ordinal suffixes (20th -> 20)
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

    formats = [
        '%Y/%m/%d', '%d-%m-%Y', '%m-%d-%Y', '%Y.%m.%d',
        '%d/%m/%Y', '%d.%m.%Y', '%Y-%m-%d', '%B %d %Y'
    ]
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    try:
        return pd.to_datetime(date_str)
    except:
        return None


def clean_amount(amount):
    """
    Extract numeric value from currency strings.
    Handles: $799, ₹5000, Rs. 499, 1099 USD, INR 72000
    """
    if pd.isna(amount):
        return 0.0
    cleaned = re.sub(r'[$₹Rs.USD,INR\s]', '', str(amount), flags=re.IGNORECASE)
    try:
        return float(cleaned)
    except:
        return 0.0


def validate_email(email):
    """
    Validate email format. Returns email if valid, None if invalid.
    """
    if pd.isna(email):
        return None
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if re.match(pattern, str(email)):
        return email
    return None


def clean_text(text, remove_special=True):
    """
    Clean text: trim whitespace, remove special chars, title case.
    """
    if pd.isna(text) or text == '':
        return None
    cleaned = str(text).strip()
    if remove_special:
        cleaned = re.sub(r'[#@!$_]', ' ', cleaned).strip()
    return cleaned.title() if cleaned else None


def clean_boolean(value):
    """
    Convert various boolean representations to True/False.
    Handles: 'YES', 'yes', 'Y', 'True', 'NO', 'false', ''
    """
    if pd.isna(value) or value == '':
        return None
    val_str = str(value).lower().strip()
    if val_str in ['yes', 'y', 'true', '1']:
        return True
    if val_str in ['no', 'n', 'false', '0']:
        return False
    return None


# =============================================================================
# BRONZE LAYER - Raw Data Identification
# =============================================================================
def identify_bronze_issues():
    """
    Read raw files and identify data quality issues.
    This is for documentation/understanding - no transformations.
    """
    print("\n" + "="*70)
    print("BRONZE LAYER - Raw Data Identification")
    print("="*70)

    # --- Orders ---
    print("\n[ORDERS] Reading orders_data.csv...")
    orders = pd.read_csv(f"{BRONZE}/orders_data.csv")
    print(f"  Rows: {len(orders)}")
    print(f"  Columns: {list(orders.columns)}")
    print("\n  Issues found:")
    print("  - Qty: Contains words ('one', 'Two', 'THREE') instead of numbers")
    print("  - Order_Date: Multiple formats (2023/06/12, 12-07-2023, July 20th 2023)")
    print("  - Order_Amount$: Currency symbols ($, ₹, Rs., USD, INR)")
    print("  - Payment_Mode: Inconsistent (CreditCard, Credit card, CREDIT card)")
    print("  - Delivery_Status: Typos (delivrd, DELIVERD)")
    print("  - Email: Invalid formats (john.doe@@gmail..com)")
    print("  - Ship_Address: Special chars (#, !, $, @)")

    # --- Inventory ---
    print("\n[INVENTORY] Reading inventory_data.json...")
    inventory = pd.read_json(f"{BRONZE}/inventory_data.json")
    print(f"  Rows: {len(inventory)}")
    print(f"  Columns: {list(inventory.columns)}")
    print("\n  Issues found:")
    print("  - stock: Words ('twenty', 'fifteen'), units suffix ('25 units')")
    print("  - last_stocked: Multiple date formats")
    print("  - cost_price: Currency symbols ($, ₹, Rs., USD)")
    print("  - warehouse: Special chars (Delhi_1, BLR#2, mumbai@3)")
    print("  - available: Inconsistent (YES, yes, Y, True, NO, false)")

    # --- Returns ---
    print("\n[RETURNS] Reading returns_data.xlsx...")
    returns = pd.read_excel(f"{BRONZE}/returns_data.xlsx")
    print(f"  Rows: {len(returns)}")
    print(f"  Columns: {list(returns.columns)}")
    print("\n  Issues found:")
    print("  - Customer_ID: Inconsistent format (C_002), missing values")
    print("  - Product: Inconsistent case (apple iphone13, VIVO V25)")
    print("  - Return_Date: Multiple date formats")
    print("  - Refund_Status: Inconsistent (Done, in progress, PENDING)")
    print("  - Pickup_Address: Special chars (pune#city, bangalore!)")
    print("  - Return_Amount: Currency symbols")

    return orders, inventory, returns


# =============================================================================
# SILVER LAYER - Data Cleaning & Correction
# =============================================================================

def clean_orders():
    """
    Clean orders data and save to Silver layer.
    """
    print("\n" + "-"*70)
    print("SILVER: Cleaning Orders")
    print("-"*70)

    df = pd.read_csv(f"{BRONZE}/orders_data.csv")
    original_count = len(df)

    # 1. Rename columns (standardize naming)
    df = df.rename(columns={
        'Order_ID': 'OrderID',
        'cust_id': 'CustomerID',
        'Product_Name': 'ProductName',
        'Qty': 'Quantity',
        'Order_Date': 'OrderDate',
        'Order_Amount$': 'OrderAmount',
        'Delivery_Status': 'DeliveryStatus',
        'Payment_Mode': 'PaymentMode',
        'Ship_Address': 'ShipAddress',
        'Promo_Code': 'PromoCode',
        'Feedback_Score': 'FeedbackScore'
    })

    # 2. Clean Quantity (words to numbers)
    df['Quantity'] = df['Quantity'].apply(clean_quantity)

    # 3. Clean OrderDate (standardize formats)
    df['OrderDate'] = df['OrderDate'].apply(clean_date)

    # 4. Clean OrderAmount (remove currency symbols)
    df['OrderAmount'] = df['OrderAmount'].apply(clean_amount)

    # 5. Clean PaymentMode (lowercase, remove special chars)
    df['PaymentMode'] = df['PaymentMode'].apply(
        lambda x: re.sub(r'[^a-zA-Z]', '', str(x)).lower() if pd.notna(x) else 'unknown'
    )

    # 6. Clean DeliveryStatus (lowercase, remove special chars)
    df['DeliveryStatus'] = df['DeliveryStatus'].apply(
        lambda x: re.sub(r'[^a-zA-Z ]', '', str(x)).lower().strip() if pd.notna(x) else 'unknown'
    )

    # 7. Validate Email
    df['Email'] = df['Email'].apply(validate_email)

    # 8. Clean ShipAddress
    df['ShipAddress'] = df['ShipAddress'].apply(
        lambda x: re.sub(r'[#@!$]', '', str(x)).strip() if pd.notna(x) else None
    )

    # 9. Clean FeedbackScore
    df['FeedbackScore'] = pd.to_numeric(df['FeedbackScore'], errors='coerce')

    # 10. Fill nulls with defaults
    df['Quantity'] = df['Quantity'].fillna(0)
    df['OrderAmount'] = df['OrderAmount'].fillna(0.0)
    df['DeliveryStatus'] = df['DeliveryStatus'].fillna('unknown')
    df['PaymentMode'] = df['PaymentMode'].fillna('unknown')

    # 11. Drop rows with no CustomerID or ProductName
    df = df.dropna(subset=['CustomerID', 'ProductName'])

    # 12. Remove duplicates by OrderID
    df = df.drop_duplicates(subset=['OrderID'])

    # Save to Silver
    df.to_csv(f"{SILVER}/orders_clean.csv", index=False)

    print(f"  Original rows: {original_count}")
    print(f"  Clean rows: {len(df)}")
    print(f"  Saved to: {SILVER}/orders_clean.csv")

    return df


def clean_inventory():
    """
    Clean inventory data and save to Silver layer.
    """
    print("\n" + "-"*70)
    print("SILVER: Cleaning Inventory")
    print("-"*70)

    df = pd.read_json(f"{BRONZE}/inventory_data.json")
    original_count = len(df)

    # 1. Rename columns
    df = df.rename(columns={
        'product_id': 'ProductID',
        'productName': 'ProductName',
        'stock': 'Stock',
        'last_stocked': 'LastStocked',
        'warehouse': 'Warehouse',
        'cost_price': 'CostPrice',
        'available': 'Available'
    })

    # 2. Clean Stock (words to numbers)
    df['Stock'] = df['Stock'].apply(clean_stock)

    # 3. Clean LastStocked (standardize dates)
    df['LastStocked'] = df['LastStocked'].apply(clean_date)

    # 4. Clean CostPrice (remove currency symbols)
    df['CostPrice'] = df['CostPrice'].apply(
        lambda x: clean_amount(x) if pd.notna(x) else None
    )

    # 5. Clean Warehouse (remove special chars, title case)
    df['Warehouse'] = df['Warehouse'].apply(clean_text)

    # 6. Clean Available (convert to boolean)
    df['Available'] = df['Available'].apply(clean_boolean)

    # Save to Silver
    df.to_csv(f"{SILVER}/inventory_clean.csv", index=False)

    print(f"  Original rows: {original_count}")
    print(f"  Clean rows: {len(df)}")
    print(f"  Saved to: {SILVER}/inventory_clean.csv")

    return df


def clean_returns():
    """
    Clean returns data and save to Silver layer.
    """
    print("\n" + "-"*70)
    print("SILVER: Cleaning Returns")
    print("-"*70)

    df = pd.read_excel(f"{BRONZE}/returns_data.xlsx")
    original_count = len(df)

    # 1. Rename columns
    df = df.rename(columns={
        'Return_ID': 'ReturnID',
        'Order_ID': 'OrderID',
        'Customer_ID': 'CustomerID',
        'Return_Reason': 'ReturnReason',
        'Return_Date': 'ReturnDate',
        'Refund_Status': 'RefundStatus',
        'Pickup_Address': 'PickupAddress',
        'Return_Amount': 'ReturnAmount'
    })

    # 2. Clean CustomerID (trim, uppercase)
    df['CustomerID'] = df['CustomerID'].apply(
        lambda x: str(x).strip().upper() if pd.notna(x) else None
    )

    # 3. Clean Product (title case, remove special chars)
    df['Product'] = df['Product'].apply(
        lambda x: clean_text(x, remove_special=True) if pd.notna(x) else None
    )

    # 4. Clean ReturnDate (standardize dates)
    df['ReturnDate'] = df['ReturnDate'].apply(clean_date)

    # 5. Clean RefundStatus (lowercase, remove special chars)
    df['RefundStatus'] = df['RefundStatus'].apply(
        lambda x: re.sub(r'[^a-zA-Z]', '', str(x)).lower() if pd.notna(x) else None
    )

    # 6. Clean PickupAddress
    df['PickupAddress'] = df['PickupAddress'].apply(clean_text)

    # 7. Clean ReturnAmount (remove currency symbols)
    df['ReturnAmount'] = df['ReturnAmount'].apply(
        lambda x: clean_amount(x) if pd.notna(x) else None
    )

    # Save to Silver
    df.to_csv(f"{SILVER}/returns_clean.csv", index=False)

    print(f"  Original rows: {original_count}")
    print(f"  Clean rows: {len(df)}")
    print(f"  Saved to: {SILVER}/returns_clean.csv")

    return df


# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("MEDALLION DATA PIPELINE - PYTHON VERSION")
    print("="*70)

    # Step 1: Bronze - Identify issues in raw data
    identify_bronze_issues()

    # Step 2: Silver - Clean and correct data
    print("\n" + "="*70)
    print("SILVER LAYER - Data Cleaning & Correction")
    print("="*70)

    orders = clean_orders()
    inventory = clean_inventory()
    returns = clean_returns()

    # Summary
    print("\n" + "="*70)
    print("PIPELINE COMPLETE!")
    print("="*70)
    print(f"\nOutput files:")
    print(f"  Bronze (raw):   {BRONZE}/")
    print(f"    - orders_data.csv")
    print(f"    - inventory_data.json")
    print(f"    - returns_data.xlsx")
    print(f"\n  Silver (clean): {SILVER}/")
    print(f"    - orders_clean.csv")
    print(f"    - inventory_clean.csv")
    print(f"    - returns_clean.csv")
    print(f"\nNext step: Load Silver CSVs into Power BI for Gold layer (KPIs)")
