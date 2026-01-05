<h1 align="center">
  <img src="m-fabric.webp" alt="Microsoft Fabric" width="100">
  <br>
  Azure Data Engineering Portfolio
</h1>

<p align="center">
  <strong>Production-ready data pipelines on Microsoft Fabric with Medallion Architecture</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Microsoft_Fabric-742774?style=for-the-badge&logo=microsoft&logoColor=white" alt="Microsoft Fabric">
  <img src="https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white" alt="PySpark">
  <img src="https://img.shields.io/badge/Delta_Lake-00ADD8?style=for-the-badge&logo=databricks&logoColor=white" alt="Delta Lake">
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions">
</p>

<p align="center">
  <a href="https://github.com/lpalad/Azure-Projects-Data-AI-Engineering/actions/workflows/ci.yml">
    <img src="https://github.com/lpalad/Azure-Projects-Data-AI-Engineering/actions/workflows/ci.yml/badge.svg" alt="CI Pipeline">
  </a>
  <img src="https://img.shields.io/badge/Projects-6-blue?style=flat-square" alt="Projects">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
</p>

---

## 📋 Table of Contents

1. [Why This Portfolio?](#-why-this-portfolio)
2. [Projects](#-projects)
3. [Architecture](#-architecture)
4. [Why Microsoft Fabric?](#-why-microsoft-fabric)
5. [CI/CD & Data Quality](#-cicd--data-quality)
6. [Tech Stack](#-tech-stack)
7. [Key Learnings](#-key-learnings)
8. [Getting Started](#-getting-started)
9. [About the Author](#-about-the-author)

---

## 🎯 Why This Portfolio?

This isn't just code—it's a demonstration of **production-ready data engineering**:

| What You'll See | Why It Matters |
|-----------------|----------------|
| **Medallion Architecture** | Industry-standard pattern used by Netflix, Airbnb, Uber |
| **Cloud-to-Cloud Migration** | Real enterprise scenario: AWS MySQL → Azure Fabric |
| **CI/CD Automation** | GitHub Actions catching bugs before production |
| **Data Quality Framework** | Pipelines that stop bad data before it spreads |
| **FinOps Awareness** | Fabric Capacity Management for cost optimization |
| **Hybrid-Cloud Skills** | OneLake Shortcuts connecting AWS S3 to Azure |

---

## 🏗️ Projects

### 01 | Medallion Retail Pipeline
| | |
|---|---|
| 📊 **What** | ETL pipeline processing retail transactions (Orders, Inventory, Returns) |
| 🔧 **Tech** | PySpark, Delta Lake, Power BI |
| 📁 **Data** | 3 data sources joined into unified analytics |
| 🎯 **Output** | Aggregated KPIs for business intelligence |

[→ View Project](./01-Medallion-Retail-Pipeline/)

---

### 02 | E-Commerce Customer 360
| | |
|---|---|
| 📊 **What** | Unified customer view from 5 disparate data sources |
| 🔧 **Tech** | PySpark, Delta Lake, Power BI |
| 📁 **Data** | Customers, Orders, Payments, Support Tickets, Web Activity |
| 🎯 **Output** | Single customer profile for marketing & sales analytics |

[→ View Project](./02-E-Commerce-Customer360/)

---

### 03 | ADF Data Migration
| | |
|---|---|
| 📊 **What** | Incremental CSV to SQL migration with file tracking |
| 🔧 **Tech** | Azure Data Factory, SQL Server |
| 📁 **Data** | CSV files with watermark-based incremental loads |
| 🎯 **Output** | Automated migration pipeline with audit trail |

[→ View Project](./03-Data-Migration-Project-End-To-End/)

---

### 04 | Retail Data Engineering
| | |
|---|---|
| 📊 **What** | Full Medallion pipeline with data quality checks |
| 🔧 **Tech** | PySpark, Delta Lake, Power BI, GitHub Actions |
| 📁 **Data** | 560 retail transactions with messy column names |
| 🎯 **Output** | Clean data + aggregated metrics + automated validation |

[→ View Project](./04-Retail-Data-Engineering/)

---

### 05 | Fabric End-To-End (LMS Analytics)
| | |
|---|---|
| 📊 **What** | Learning Management System pipeline with daily incremental loads |
| 🔧 **Tech** | PySpark, Delta Lake, ADLS Gen2 |
| 📁 **Data** | 10 daily CSV files simulating production data flow |
| 🎯 **Output** | Partitioned landing zone with date-based organization |

[→ View Project](./05-Fabric-End-To-End/)

---

### 06 | AWS MySQL to Fabric Migration
| | |
|---|---|
| 📊 **What** | Cloud-to-cloud migration guide (no-code approach) |
| 🔧 **Tech** | AWS RDS MySQL, Dataflow Gen2, Fabric Lakehouse |
| 📁 **Data** | Production MySQL database |
| 🎯 **Output** | Step-by-step migration template + Delta tables |

[→ View Project](./06-MySQL-to-Lakehouse-Migration/)

---

## 🏛️ Architecture

All projects follow the **Medallion Architecture** (Bronze → Silver → Gold):

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   SOURCE    │  →   │   BRONZE    │  →   │   SILVER    │  →   │    GOLD     │
│   (Raw)     │      │  (As-Is)    │      │  (Cleaned)  │      │ (Analytics) │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
     CSV                 Parquet            Delta Table          Delta Table
     JSON                                                              │
     Excel                                                             ▼
     MySQL                                                    ┌─────────────┐
                                                              │  Power BI   │
                                                              │  Dashboard  │
                                                              └─────────────┘
```

| Layer | Purpose | Example |
|-------|---------|---------|
| **Bronze** | Raw data ingestion (no transformations) | `Order iD`, `cust_ID` (messy names) |
| **Silver** | Cleaned, validated, standardized | `OrderID`, `CustomerID` (clean names) |
| **Gold** | Aggregated, joined, ready for analytics | TotalSales, ProfitMargin by Region |

---

## 🤔 Why Microsoft Fabric?

| Platform | Strength | Trade-off |
|----------|----------|-----------|
| **Databricks** | Best for heavy ML workloads | Complex setup, separate BI tool needed |
| **Snowflake** | Excellent SQL warehouse | No native notebook experience |
| **AWS Glue + Redshift** | Deep AWS integration | Multiple services to manage |
| **Microsoft Fabric** | Unified platform (ETL + BI + ML) | Newer, evolving feature set |

**I chose Fabric because:**
- Unifies Lakehouse, Dataflows, Notebooks, and Power BI in one platform
- Reduces tool sprawl and simplifies the data stack
- OneLake Shortcuts enable hybrid-cloud access to AWS S3
- Semantic Models bridge data engineering to business intelligence

---

## ✅ CI/CD & Data Quality

### Automated Pipeline (GitHub Actions)

Every push triggers automated validation:

| Check | What It Does |
|-------|--------------|
| **Python Syntax** | Validates all `.py` files compile correctly |
| **Code Linting** | Runs flake8 for code style enforcement |
| **Project Structure** | Verifies all project directories exist |
| **Data Quality** | Validates Bronze layer data before transformation |

### Data Quality Framework

Pipelines include pre-transformation validation:

```
==================================================
  DATA QUALITY CHECKS - Bronze Layer
==================================================
✓ Row count: 560 rows (PASS)
✓ Required columns: 14/14 present (PASS)
✓ Null check: OrderID has 0 nulls (PASS)
✓ Null check: CustomerID has 0 nulls (PASS)
✓ Value check: No invalid quantities (PASS)
✓ Value check: No negative/zero prices (PASS)
==================================================
✓ All critical data quality checks PASSED
==================================================
```

> **If critical checks fail → Pipeline stops before bad data propagates**

---

## 🔧 Tech Stack

### Cloud & Platform
![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Microsoft Fabric](https://img.shields.io/badge/Microsoft_Fabric-742774?style=for-the-badge&logo=microsoft&logoColor=white)
![Azure Data Factory](https://img.shields.io/badge/Azure_Data_Factory-0078D4?style=for-the-badge&logo=azure-devops&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

### Data Processing
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

### Data Storage
![Delta Lake](https://img.shields.io/badge/Delta_Lake-00ADD8?style=for-the-badge&logo=databricks&logoColor=white)
![Parquet](https://img.shields.io/badge/Parquet-50ABF1?style=for-the-badge&logo=apache&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

### Visualization & DevOps
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

### Microsoft Fabric Components
- **Lakehouse** — Unified storage (files + tables)
- **Dataflow Gen2** — No-code ETL for migrations
- **Notebooks** — PySpark development environment
- **Semantic Models** — Power BI data layer
- **OneLake Shortcuts** — Hybrid-cloud S3 access
- **Capacity Management** — FinOps cost optimization

---

## 💡 Key Learnings

Building these projects taught me:

| Learning | Insight |
|----------|---------|
| **Dataflow Gen2 is powerful** | No-code migrations that would take days in Python |
| **Delta Lake enables time travel** | Query data as it existed yesterday |
| **CI/CD isn't optional** | Caught 3 bugs before they hit production |
| **Data quality is non-negotiable** | One null OrderID broke a downstream report |
| **Documentation matters** | Visual READMEs get 10x more engagement |
| **Medallion scales** | Same pattern works for 500 rows or 500M rows |

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/lpalad/Azure-Projects-Data-AI-Engineering.git

# Navigate to a project
cd Azure-Projects-Data-AI-Engineering/04-Retail-Data-Engineering

# Follow project-specific README for setup
```

### Prerequisites

| Tool | Purpose |
|------|---------|
| Microsoft Fabric | Lakehouse, notebooks, dataflows |
| Power BI Desktop | Dashboard development |
| Python 3.11+ | Local script testing |
| Git | Version control |

---

## 👨‍💻 About the Author

**Leonard S Palad** | MBA | Master of AI (In-progress)

Building production ML systems and data pipelines that connect to business outcomes.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leonardspalad/)
[![Portfolio](https://img.shields.io/badge/AI_Portfolio-000000?style=for-the-badge&logo=github&logoColor=white)](https://salesconnect.com.au/aip.html)
[![Blog](https://img.shields.io/badge/Blog-FF5722?style=for-the-badge&logo=blogger&logoColor=white)](https://www.cloudhermit.com.au/)

### Related Repositories

| Repository | Description |
|------------|-------------|
| [AWS Projects](https://github.com/lpalad/AWS-Projects) | AWS infrastructure and AI/ML projects |
| [ML Lead Scoring](https://github.com/lpalad/mda) | Production ML system for sales conversion |

---

## 📅 Updates

| Date | Update |
|------|--------|
| January 2026 | Added CI/CD pipeline and Data Quality framework |
| January 2026 | Added MySQL to Lakehouse Migration (Project 06) |
| January 2026 | Added Fabric End-To-End LMS Pipeline (Project 05) |
| January 2026 | Added Retail Data Engineering Pipeline (Project 04) |
| January 2026 | Added Data Migration Project (Project 03) |
| January 2026 | Added E-Commerce Customer 360 Pipeline (Project 02) |
| January 2026 | Added Medallion Retail Pipeline (Project 01) |

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) for details

---

<p align="center">
  <strong>Built with Microsoft Fabric | Documented with care</strong>
  <br>
  <em>Because data engineering is about building systems, not just writing queries</em>
</p>
