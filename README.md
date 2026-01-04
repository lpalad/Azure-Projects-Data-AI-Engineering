# Azure Data & AI Engineering Projects

## Overview
A collection of Azure and Microsoft Fabric projects demonstrating data engineering, ETL pipelines, and analytics patterns. Each project includes documentation, code, and best practices.

<p align="center">
  <img src="m-fabric.webp" alt="Microsoft Fabric" width="600">
</p>

## Projects

### Data Engineering / ETL

| # | Project | Description | Tech Stack |
|---|---------|-------------|------------|
| 1 | [Medallion Retail Pipeline](./01-Medallion-Retail-Pipeline/) | ETL pipeline for retail data using Medallion Architecture (Orders, Inventory, Returns) | Python, PySpark, Fabric, Power BI |
| 2 | [E-Commerce Customer 360](./02-E-Commerce-Customer360/) | Customer analytics pipeline joining 5 data sources for unified customer view | Python, PySpark, Fabric, Power BI |
| 3 | [Data Migration Project](./03-Data-Migration-Project-End-To-End/) | Azure Data Factory pipeline for incremental CSV to SQL migration with file tracking | Azure Data Factory, SQL, CSV |
| 4 | [Retail Data Engineering](./04-Retail-Data-Engineering/) | Retail transaction pipeline with Medallion Architecture and aggregated business KPIs | PySpark, Fabric, Delta Lake, Power BI |
| 5 | [Fabric End-To-End](./05-Fabric-End-To-End/) | LMS analytics pipeline with incremental daily loads simulating production environment | PySpark, Fabric, Delta Lake |
| 6 | [MySQL to Lakehouse Migration](./06-MySQL-to-Lakehouse-Migration/) | Cloud-to-cloud migration guide from AWS MySQL to Fabric Lakehouse using Dataflow Gen2 | AWS RDS, MySQL, Fabric, Dataflow Gen2 |

## Architecture

All projects follow the **Medallion Architecture**:

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   SOURCE    │  →   │   BRONZE    │  →   │   SILVER    │  →   │    GOLD     │
│   (Raw)     │      │  (As-Is)    │      │  (Cleaned)  │      │ (Analytics) │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
     CSV                 Parquet            Delta Table          Delta Table
     JSON                                                              │
     Excel                                                             ▼
                                                               ┌─────────────┐
                                                               │  Power BI   │
                                                               │  Dashboard  │
                                                               └─────────────┘
```

- **Bronze**: Raw data ingestion (no transformations)
- **Silver**: Cleaned, validated, and standardized data
- **Gold**: Aggregated, joined tables ready for analytics

## Tech Stack

### Cloud & Platform
![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Microsoft Fabric](https://img.shields.io/badge/Microsoft_Fabric-742774?style=for-the-badge&logo=microsoft&logoColor=white)
![Azure Data Factory](https://img.shields.io/badge/Azure_Data_Factory-0078D4?style=for-the-badge&logo=azure-devops&logoColor=white)

### Data Processing
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

### Data Storage
![Delta Lake](https://img.shields.io/badge/Delta_Lake-00ADD8?style=for-the-badge&logo=databricks&logoColor=white)
![Parquet](https://img.shields.io/badge/Parquet-50ABF1?style=for-the-badge&logo=apache&logoColor=white)
![SQL](https://img.shields.io/badge/SQL_Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)

### Visualization & Tools
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## CI/CD Pipeline

![CI Pipeline](https://github.com/lpalad/Azure-Projects-Data-AI-Engineering/actions/workflows/ci.yml/badge.svg)

This repository includes automated CI/CD using GitHub Actions:

| Check | Description |
|-------|-------------|
| **Python Syntax** | Validates all `.py` files compile correctly |
| **Code Linting** | Runs flake8 for code style enforcement |
| **Project Structure** | Verifies all project directories exist |
| **Data Quality** | Validates Bronze layer data before transformation |

## Data Quality

Pipelines include automated data quality validation:

```
✓ Row count validation
✓ Required columns check
✓ Null value detection
✓ Value range validation
```

If critical checks fail, the pipeline stops before bad data propagates.

## Getting Started

1. Clone this repository
2. Navigate to a project folder
3. Follow the project-specific README for setup instructions

```bash
git clone https://github.com/lpalad/Azure-Projects-Data-AI-Engineering.git
cd Azure-Projects-Data-AI-Engineering/01-Medallion-Retail-Pipeline
```

## Related Repositories

- [AWS Projects](https://github.com/lpalad/AWS-Projects) - AWS infrastructure and AI/ML projects

## Blog Posts

Related blog posts: https://www.cloudhermit.com.au

## Author

**Leonard S Palad** | MBA | Master of AI (In-progress)

- AI Portfolio: https://salesconnect.com.au/aip.html
- LinkedIn: https://www.linkedin.com/in/leonardspalad/
- Blog: https://www.cloudhermit.com.au/

## Updates

- January 2026: Added Retail Data Engineering Pipeline (Project 04)
- January 2026: Added Data Migration Project (Project 03)
- January 2026: Added E-Commerce Customer 360 Pipeline
- January 2026: Added Medallion Retail Pipeline

## License

MIT License - See [LICENSE](./LICENSE) for details
