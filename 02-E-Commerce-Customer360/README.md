# E-Commerce Customer 360 Pipeline

## Overview
A **Customer 360** analytics pipeline implementing the **Medallion Architecture** (Bronze → Silver → Gold). This project joins 5 data sources to create a unified customer view for analytics and KPI reporting.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MEDALLION ARCHITECTURE                           │
│                    Customer 360 View                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   BRONZE (Raw)           SILVER (Cleaned)         GOLD (Analytics)  │
│   ┌────────────┐        ┌────────────────┐       ┌──────────────┐  │
│   │ customers  │   →    │ customers_clean│   →   │              │  │
│   └────────────┘        └────────────────┘       │              │  │
│   ┌────────────┐        ┌────────────────┐       │              │  │
│   │ orders     │   →    │ orders_clean   │   →   │  gold_joined │  │
│   └────────────┘        └────────────────┘       │              │  │
│   ┌────────────┐        ┌────────────────┐       │  (LEFT JOIN  │  │
│   │ payments   │   →    │ payments_clean │   →   │   on         │  │
│   └────────────┘        └────────────────┘       │  CustomerID) │  │
│   ┌────────────┐        ┌────────────────┐       │              │  │
│   │ support_   │   →    │ support_       │   →   │              │  │
│   │ tickets    │        │ tickets_clean  │       │              │  │
│   └────────────┘        └────────────────┘       └──────┬───────┘  │
│   ┌────────────┐        ┌────────────────┐              │          │
│   │ web_       │   →    │ web_activities │   →          ▼          │
│   │ activities │        │ _clean         │       ┌──────────────┐  │
│   └────────────┘        └────────────────┘       │  Power BI    │  │
│                                                  │  Dashboard   │  │
│                                                  └──────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Dashboard

![E-Commerce KPI Dashboard](screenshots/dashboard.jpg)

## Tech Stack
- **Python / Pandas** - Local data processing
- **PySpark** - Distributed processing on Fabric
- **Microsoft Fabric** - Lakehouse, Notebooks, Semantic Models
- **Power BI** - Dashboard and KPI visualization

## Data Sources

| File | Description | Key Fields |
|------|-------------|------------|
| customers.csv | Customer master data | CustomerID, Name, Email, Gender, DOB, City |
| orders.csv | Order transactions | OrderID, CustomerID, Amount, Status, Date |
| payments.csv | Payment records | PaymentID, CustomerID, Method, Status, Amount |
| support_tickets.csv | Customer support issues | TicketID, CustomerID, IssueType, Resolution |
| web_activities.csv | Website browsing data | SessionID, CustomerID, PageViewed, Device |

## Data Cleaning (Silver Layer)

### Customers
| Field | Cleaning Applied |
|-------|------------------|
| Name | Title Case (`john DOE` → `John Doe`) |
| Email | Validate format, lowercase, invalid → null |
| Gender | Standardize (`M`, `male`, `MALE` → `Male`) |
| DOB | Parse multiple date formats → `YYYY-MM-DD` |
| City | Title Case (`MUMBAI` → `Mumbai`) |

### Orders
| Field | Cleaning Applied |
|-------|------------------|
| OrderDate | Parse multiple formats → `YYYY-MM-DD` |
| Amount | 2 decimal places, NaN → 0.00 |
| Status | Title Case (`shipped` → `Shipped`) |

### Payments
| Field | Cleaning Applied |
|-------|------------------|
| PaymentDate | Parse multiple formats, NaN → blank |
| PaymentMethod | Merge duplicates (`creditcard` → `Credit Card`) |
| PaymentStatus | Title Case |
| Amount | 2 decimal places |

### Support Tickets
| Field | Cleaning Applied |
|-------|------------------|
| IssueType | Title Case |
| TicketDate | Parse multiple formats |
| ResolutionStatus | Title Case |

### Web Activities
| Field | Cleaning Applied |
|-------|------------------|
| PageViewed | Lowercase |
| SessionTime | Parse multiple formats |
| DeviceType | Title Case |

## Gold Layer (Joined Table)

```python
# Customer 360 View - All tables joined on CustomerID
gold = (
    customers
    .merge(orders, on='CustomerID', how='left')
    .merge(payments, on='CustomerID', how='left')
    .merge(support_tickets, on='CustomerID', how='left')
    .merge(web_activities, on='CustomerID', how='left')
)
```

**Why LEFT JOIN?** Keep all customers, even if they have no orders, payments, tickets, or web activity.

## Project Structure

```
02-E-Commerce-Customer360/
├── README.md
├── data/
│   ├── bronze/           # Raw data (as-is)
│   │   ├── customers.csv
│   │   ├── orders.csv
│   │   ├── payments.csv
│   │   ├── support_tickets.csv
│   │   └── web_activities.csv
│   ├── silver/           # Cleaned data
│   │   ├── customers_clean.csv
│   │   ├── orders_clean.csv
│   │   ├── payments_clean.csv
│   │   ├── support_tickets_clean.csv
│   │   └── web_activities_clean.csv
│   └── gold/             # Joined analytics table
│       └── gold_joined.csv
├── notebooks/
│   └── E-com.ipynb       # Complete pipeline notebook
└── screenshots/
    ├── dashboard.jpg
    └── E-Com-Revenue-KPS.pdf
```

## How to Run

### Local (Python)
```bash
# Open Jupyter Notebook
jupyter notebook notebooks/E-com.ipynb
# Run all cells
```

### Microsoft Fabric
1. Upload raw files to Lakehouse `/Files/bronze/`
2. Copy PySpark code from notebook into Fabric Notebook
3. Run all cells
4. Gold table ready for Power BI

## KPIs Generated

| KPI | Chart Type |
|-----|------------|
| Total Revenue | Card |
| Total Orders | Gauge |
| Total Tickets | Gauge |
| Order by Device Type | Bar Chart |
| Order Status Distribution | Bar Chart |
| Revenue by Payment Method | Donut Chart |
| Support Ticket by Type | Bar Chart |

## Key Insights
- **iOS** dominates device usage (47.58%)
- **Credit Card** is the top payment method (38.44%)
- Most support tickets are **Closed** (50%+)
- Total revenue: **$2.19K** from **15 orders**

## Author
Leonard S Palad | MBA | Master of AI (In-progress)
- LinkedIn: https://www.linkedin.com/in/leonardspalad/
- Blog: https://www.cloudhermit.com.au/
