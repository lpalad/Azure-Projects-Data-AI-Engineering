# Azure Data & AI Engineering Projects

## Overview
A collection of Azure and Microsoft Fabric projects demonstrating data engineering, ETL pipelines, and analytics patterns. Each project includes documentation, code, and best practices.

## Projects

### Data Engineering / ETL

| # | Project | Description | Tech Stack |
|---|---------|-------------|------------|
| 1 | [Medallion Retail Pipeline](./01-Medallion-Retail-Pipeline/) | ETL pipeline for retail data using Medallion Architecture (Orders, Inventory, Returns) | Python, PySpark, Fabric, Power BI |
| 2 | [E-Commerce Customer 360](./02-E-Commerce-Customer360/) | Customer analytics pipeline joining 5 data sources for unified customer view | Python, PySpark, Fabric, Power BI |

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

| Category | Technologies |
|----------|--------------|
| **Cloud Platform** | Microsoft Azure, Microsoft Fabric |
| **Data Processing** | Python, Pandas, PySpark |
| **Data Storage** | Delta Lake, Parquet, Lakehouse |
| **Orchestration** | Fabric Notebooks |
| **Visualization** | Power BI |
| **Version Control** | Git, GitHub |

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

- January 2026: Added Medallion Retail Pipeline
- January 2026: Added E-Commerce Customer 360 Pipeline

## License

MIT License - See [LICENSE](./LICENSE) for details
