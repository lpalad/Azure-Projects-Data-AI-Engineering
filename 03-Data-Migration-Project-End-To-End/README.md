<p align="center">
  <h1 align="center">Data Migration Project (End-to-End)</h1>
  <p align="center">
    <strong>Azure Data Factory Pipeline for Incremental CSV to SQL Migration</strong>
  </p>
  <p align="center">
    <a href="#architecture">Architecture</a> •
    <a href="#database-schema">Schema</a> •
    <a href="#pipeline-logic">Pipeline</a> •
    <a href="#how-to-run">How to Run</a>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Azure_Data_Factory-0078D4?style=for-the-badge&logo=azure-devops&logoColor=white" alt="Azure Data Factory">
  <img src="https://img.shields.io/badge/SQL_Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white" alt="SQL Server">
  <img src="https://img.shields.io/badge/Azure_SQL-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white" alt="Azure SQL">
  <img src="https://img.shields.io/badge/CSV-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white" alt="CSV">
</p>

---

## Overview

An **Azure Data Factory (ADF)** end-to-end data migration pipeline that incrementally loads daily product CSV files into a SQL database. The pipeline tracks processed files to prevent duplicate loads.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA MIGRATION PIPELINE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   SOURCE (CSV Files)              AZURE DATA FACTORY                │
│   ┌────────────────┐             ┌──────────────────┐              │
│   │ product_       │             │                  │              │
│   │ 2024-07-01.csv │ ──────────► │  1. Lookup       │              │
│   │ 2024-07-02.csv │             │     (FileTracker)│              │
│   │ 2024-07-03.csv │             │                  │              │
│   │ ...            │             │  2. Filter       │              │
│   │ 2024-07-10.csv │             │     (New files)  │              │
│   └────────────────┘             │                  │              │
│                                  │  3. ForEach      │              │
│                                  │     - Copy Data  │              │
│                                  │     - Script     │              │
│                                  └────────┬─────────┘              │
│                                           │                        │
│                                           ▼                        │
│                           ┌───────────────────────────┐            │
│                           │      AZURE SQL DB         │            │
│                           │  ┌─────────────────────┐  │            │
│                           │  │    DimProduct       │  │            │
│                           │  │    (Product Data)   │  │            │
│                           │  └─────────────────────┘  │            │
│                           │  ┌─────────────────────┐  │            │
│                           │  │    FileTracker      │  │            │
│                           │  │    (Audit Table)    │  │            │
│                           │  └─────────────────────┘  │            │
│                           └───────────────────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

![Azure Data Factory](https://img.shields.io/badge/Azure_Data_Factory-0078D4?style=for-the-badge&logo=azure-devops&logoColor=white)
![Azure SQL](https://img.shields.io/badge/Azure_SQL-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL_Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![Azure Blob Storage](https://img.shields.io/badge/Azure_Blob-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)

---

## Data Sources

**10 Daily Product CSV Files** (July 1-10, 2024)

| File | Records | Description |
|------|---------|-------------|
| `product_2024-07-01.csv` | 10 | Daily product snapshot |
| `product_2024-07-02.csv` | 10 | Daily product snapshot |
| `...` | ... | ... |
| `product_2024-07-10.csv` | 10 | Daily product snapshot |

**CSV Schema:**
```
ProductID,ProductName,Category,Price
101,Shampoo,Personal Care,180
102,Toothpaste,Personal Care,90
103,Rice,Groceries,650
...
```

---

## Database Schema

### DimProduct (Dimension Table)

```sql
CREATE TABLE DimProduct (
    ProductID INT,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    Price FLOAT,
    FileName VARCHAR(100),    -- Source file tracking
    LoadDate DATETIME2(0)     -- When data was loaded
);
```

### FileTracker (Audit Table)

```sql
CREATE TABLE FileTracker (
    FileName VARCHAR(100),
    LoadDate DATETIME2(0)
);
```

---

## Pipeline Logic

### 1. Lookup Activity
Retrieves list of already-processed files from `FileTracker` table.

### 2. Filter Activity
Filters out files that have already been processed:
```
@not(contains(string(activity('Lookup1').output.value), item().name))
```

### 3. ForEach Activity
For each new file:
- **Copy Data**: Load CSV into `DimProduct` table
- **Script Activity**: Insert record into `FileTracker`

```sql
INSERT INTO FileTracker (FileName, LoadDate)
VALUES ('@{item().name}', GETUTCDATE());
```

---

## Project Structure

```
03-Data-Migration-Project-End-To-End/
├── README.md
├── DATASET/
│   ├── product_2024-07-01.csv
│   ├── product_2024-07-02.csv
│   ├── product_2024-07-03.csv
│   ├── product_2024-07-04.csv
│   ├── product_2024-07-05.csv
│   ├── product_2024-07-06.csv
│   ├── product_2024-07-07.csv
│   ├── product_2024-07-08.csv
│   ├── product_2024-07-09.csv
│   └── product_2024-07-10.csv
└── sql.txt                    # SQL schema and pipeline snippets
```

---

## How to Run

### Prerequisites
1. Azure subscription
2. Azure Data Factory instance
3. Azure SQL Database or SQL Server
4. Azure Blob Storage (for CSV files)

### Setup Steps

1. **Create Database Tables**
   ```sql
   -- Run sql.txt to create DimProduct and FileTracker tables
   ```

2. **Upload CSV Files**
   - Upload all CSV files to Azure Blob Storage

3. **Create ADF Pipeline**
   - Lookup: Query FileTracker for processed files
   - Get Metadata: List files in blob container
   - Filter: Exclude already-processed files
   - ForEach: Copy each new file + update tracker

4. **Run Pipeline**
   - Trigger manually or schedule daily

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Incremental Load** | Only processes new/unprocessed files |
| **File Tracking** | Audit table prevents duplicate loads |
| **Data Lineage** | FileName and LoadDate in DimProduct |
| **Idempotent** | Safe to re-run without duplicates |

---

## Related Repositories

- [AWS Projects](https://github.com/lpalad/AWS-Projects) - AWS infrastructure and AI/ML projects

## Blog Posts

Related blog posts: [cloudhermit.com.au](https://www.cloudhermit.com.au)

---

## Author

<table>
  <tr>
    <td>
      <strong>Leonard S Palad</strong><br>
      MBA | Master of AI (In-progress)
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://salesconnect.com.au/aip.html">AI Portfolio</a> •
      <a href="https://www.linkedin.com/in/leonardspalad/">LinkedIn</a> •
      <a href="https://www.cloudhermit.com.au/">Blog</a>
    </td>
  </tr>
</table>

---

<p align="center">
  <sub>Built with ❤️ using Azure Data Factory</sub>
</p>
