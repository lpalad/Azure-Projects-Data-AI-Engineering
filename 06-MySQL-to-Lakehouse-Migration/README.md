<p align="center">
  <h1 align="center">AWS MySQL to Microsoft Fabric Migration</h1>
  <p align="center">
    <strong>Cloud-to-Cloud Database Migration using Dataflow Gen2</strong>
  </p>
  <p align="center">
    <a href="#prerequisites">Prerequisites</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#step-by-step-guide">Step-by-Step</a> •
    <a href="#next-steps">Next Steps</a>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AWS_RDS-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Microsoft_Fabric-Lakehouse-742774?style=for-the-badge&logo=microsoft&logoColor=white" alt="Microsoft Fabric">
  <img src="https://img.shields.io/badge/Dataflow_Gen2-ETL-0078D4?style=for-the-badge&logo=microsoft&logoColor=white" alt="Dataflow Gen2">
  <img src="https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI">
</p>

---

## Overview

A step-by-step guide for migrating data from **AWS MySQL (RDS)** to **Microsoft Fabric Lakehouse** using Dataflow Gen2. This no-code approach enables cloud-to-cloud migration in minutes.

<p align="center">
  <img src="../m-fabric.webp" alt="Microsoft Fabric" width="600">
</p>

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     AWS MySQL → Fabric Migration                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   AWS Cloud                        Microsoft Azure                          │
│   ┌─────────────────┐             ┌─────────────────────────────────────┐  │
│   │                 │             │  Microsoft Fabric                    │  │
│   │   MySQL RDS     │ ─────────── │  ┌─────────────────────────────────┐│  │
│   │                 │  Dataflow   │  │         Lakehouse               ││  │
│   │  ┌───────────┐  │   Gen2      │  │  ┌────────────────────────────┐││  │
│   │  │ Table 1   │  │ ──────────► │  │  │ Delta Tables               │││  │
│   │  │ Table 2   │  │  (JDBC)     │  │  │ • bronze_table_1           │││  │
│   │  │ Table 3   │  │             │  │  │ • bronze_table_2           │││  │
│   │  └───────────┘  │             │  │  │ • bronze_table_3           │││  │
│   │                 │             │  │  └────────────────────────────┘││  │
│   └─────────────────┘             │  └─────────────────────────────────┘│  │
│                                   │                  │                   │  │
│                                   │                  ▼                   │  │
│                                   │  ┌─────────────────────────────────┐│  │
│                                   │  │       Semantic Model            ││  │
│                                   │  │     + Power BI Report           ││  │
│                                   │  └─────────────────────────────────┘│  │
│                                   └─────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **AWS MySQL** | Running RDS instance with data |
| **MySQL Workbench** | Verify you can connect locally |
| **Microsoft Fabric** | Active workspace (Trial or Paid) |
| **Network Access** | MySQL accessible from internet |

---

## Step-by-Step Guide

### Step 1: Prepare AWS MySQL for External Access

**In AWS Console → RDS → Your Database:**

1. **Security Group** - Add inbound rule:

   | Setting | Value |
   |---------|-------|
   | Type | MySQL/Aurora |
   | Port | 3306 |
   | Source | 0.0.0.0/0 (or Azure IP ranges) |

2. **Public Accessibility** - Set to `Yes`

3. **Note your connection details:**

   ```
   Host:     your-db-instance.xxxxxxxx.us-east-1.rds.amazonaws.com
   Port:     3306
   Database: your_database_name
   Username: admin
   Password: ********
   ```

---

### Step 2: Create Lakehouse in Fabric

1. Go to **Microsoft Fabric** → Your Workspace
2. Click **+ New** → **Lakehouse**
3. Name it: `Migration_Source_Lakehouse`
4. Click **Create**

<details>
<summary><strong>Screenshot Reference</strong></summary>

```
Fabric Workspace
├── + New
│   └── Lakehouse
│       └── Name: Migration_Source_Lakehouse
```

</details>

---

### Step 3: Create Dataflow Gen2

1. In your Workspace → **+ New** → **Dataflow Gen2**
2. Name it: `MySQL_to_Lakehouse`

---

### Step 4: Connect to MySQL

1. Click **Get Data** → Search **MySQL**
2. Select **MySQL database**
3. Enter connection details:

   | Field | Value |
   |-------|-------|
   | Server | `your-db-instance.xxxxxxxx.region.rds.amazonaws.com` |
   | Database | `your_database_name` |

4. Click **Next**
5. Enter credentials:

   | Field | Value |
   |-------|-------|
   | Authentication | Basic |
   | Username | `your_username` |
   | Password | `your_password` |

6. Click **Connect**

---

### Step 5: Select Tables

The Navigator panel will show all available tables.

> **Note:** You may see MySQL system tables (`performance_schema.*`, `information_schema.*`). Ignore these and search for your actual database tables.

**To find your tables:**
- Use the **Search** box
- Type your database name or table name
- Check the tables you want to migrate:

```
☑ your_database.customers
☑ your_database.orders
☑ your_database.products
```

Click **Create** or **Transform Data**

---

### Step 6: Set Destination (Lakehouse)

1. In Power Query editor, look at bottom right
2. Click **Add data destination** → **Lakehouse**
3. Connect to your workspace
4. Select your Lakehouse
5. Set table name: `bronze_customers` (prefix with `bronze_` for Medallion pattern)
6. Click **Save settings**

---

### Step 7: Configure Load Settings

| Setting | Recommended Value |
|---------|-------------------|
| Update method | **Replace** (for initial full load) |
| Column mapping | Auto-mapped (verify correctness) |

> **Tip:** Use `Append` for incremental loads after initial migration.

---

### Step 8: Publish & Run

1. Click **Publish** (top right)
2. Wait for publish to complete
3. Click **Refresh now** to execute the dataflow

---

### Step 9: Verify Migration

1. Go to your **Workspace**
2. Open your **Lakehouse**
3. Expand **Tables** → **dbo**
4. Your migrated table should appear

```
Lakehouse
├── Tables
│   └── dbo
│       └── bronze_customers  ✓ Migration successful!
└── Files
```

---

## What Fabric Does Behind the Scenes

When you click "Refresh now", Fabric automatically:

| Action | Description |
|--------|-------------|
| Establishes JDBC connection | Secure connection to MySQL |
| Handles network routing | Routes traffic through Azure backbone |
| Converts data types | MySQL types → Delta Lake types |
| Creates Parquet files | Optimized columnar storage |
| Registers table in metastore | Enables SQL queries |
| Creates SQL endpoint | Ready for analytics |
| Enables semantic modeling | Power BI ready |

---

## Next Steps

### Option A: Migrate More Tables

Repeat Steps 4-9 for additional tables.

### Option B: Build Semantic Model

1. In Lakehouse → **New semantic model**
2. Select migrated tables
3. Define relationships
4. Create DAX measures

### Option C: Build Power BI Report

1. From Semantic Model → **Create report**
2. Build visualizations
3. Publish to workspace

### Option D: Schedule Refresh

1. Edit Dataflow Gen2
2. Click **Schedule refresh**
3. Set frequency (Daily, Hourly, etc.)

---

## Migration Patterns

| Pattern | Use Case | Update Method |
|---------|----------|---------------|
| **Full Load** | Initial migration, small tables | Replace |
| **Incremental** | Daily/hourly sync, large tables | Append |
| **CDC** | Near real-time, critical data | Event-driven |

---

## Troubleshooting

<details>
<summary><strong>Cannot connect to MySQL</strong></summary>

- Verify Security Group allows inbound on port 3306
- Check "Public Accessibility" is enabled
- Test connection from MySQL Workbench first

</details>

<details>
<summary><strong>Only see system tables (performance_schema)</strong></summary>

- Use Search box to filter by your database name
- Tables appear as: `database_name.table_name`

</details>

<details>
<summary><strong>Dataflow refresh fails</strong></summary>

- Check credentials haven't expired
- Verify MySQL instance is running
- Review error message in refresh history

</details>

---

## Cost Considerations

| Component | Cost Factor |
|-----------|-------------|
| AWS RDS | Running instance + data transfer out |
| Fabric Dataflow | Compute during refresh |
| Lakehouse Storage | Data stored in OneLake |
| Power BI | Included with Fabric capacity |

> **Tip:** For one-time migration, you can pause/delete AWS RDS after verification to save costs.

---

## Author

**Leonard Palad**

[![Portfolio](https://img.shields.io/badge/Portfolio-000?style=flat-square&logo=github)](https://github.com/lpalad)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin)](https://linkedin.com/in/yourprofile)

---

## Related Projects

| Project | Description |
|---------|-------------|
| [01-Medallion-Retail-Pipeline](../01-Medallion-Retail-Pipeline) | ETL with Bronze → Silver → Gold |
| [02-E-Commerce-Customer360](../02-E-Commerce-Customer360) | Customer 360 analytics |
| [03-Data-Migration-Project](../03-Data-Migration-Project-End-To-End) | ADF incremental migration |
| [04-Retail-Data-Engineering](../04-Retail-Data-Engineering) | PySpark transformations |
| [05-Fabric-End-To-End](../05-Fabric-End-To-End) | LMS analytics pipeline |

---

<p align="center">
  <em>Cloud-to-cloud migration made simple with Microsoft Fabric</em>
</p>
