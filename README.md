<h1 align="center">
  <img src="m-fabric.webp" alt="Microsoft Fabric" width="100">
  <br>
  Azure Data Engineering Portfolio
</h1>

<p align="center">
  <strong>6 production-ready pipelines. Real migrations. Working code.</strong>
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

## The Problem With Most Data Engineering Portfolios

They show tutorials. Not production work.

Anyone can follow a YouTube video. Few can build pipelines that catch bad data before it breaks reports. Fewer still can migrate databases across clouds without losing a single row.

This portfolio is different.

Every project here solves a real problem. Every pipeline has validation. Every migration was tested against production data.

---

## 📋 What's Inside

1. [Why Hire Me](#why-hire-me)
2. [The 6 Projects](#the-6-projects)
3. [How I Build Pipelines](#how-i-build-pipelines)
4. [The Tech I Use](#the-tech-i-use)
5. [What I Learned](#what-i-learned)
6. [About Me](#about-me)

---

## Why Hire Me

Here is what I bring to your team:

| Skill | Proof |
|-------|-------|
| **I build pipelines that work** | 6 complete projects, all tested, all documented |
| **I catch problems early** | Data quality checks stop bad data before it spreads |
| **I automate everything** | GitHub Actions runs tests on every single commit |
| **I migrate databases safely** | AWS MySQL to Azure Fabric with zero data loss |
| **I care about costs** | Fabric Capacity Management to prevent bill shock |
| **I connect to your existing systems** | OneLake Shortcuts bridge AWS S3 to Azure |

Most candidates talk about what they can do. I show you.

---

## The 6 Projects

### Project 01: Medallion Retail Pipeline

**The problem:** Raw retail data is messy. Column names have typos. Dates are in wrong formats. You cannot build reports on this.

**What I built:** A three-layer pipeline that takes messy data and makes it clean.

| Layer | What Happens |
|-------|--------------|
| Bronze | Raw data comes in. I do not touch it. |
| Silver | I fix column names. I parse dates. I validate types. |
| Gold | I calculate TotalSales, GrossProfit, ProfitMargin. Ready for Power BI. |

**The result:** Clean data. Accurate reports. Happy stakeholders.

[→ See the code](./01-Medallion-Retail-Pipeline/)

---

### Project 02: Customer 360

**The problem:** Customer data is scattered across 5 different systems. Sales cannot see the full picture.

**What I built:** A pipeline that joins Customers, Orders, Payments, Support Tickets, and Web Activity into one unified view.

**The result:** One table with everything you need to know about each customer. Sales teams stop asking IT for reports.

[→ See the code](./02-E-Commerce-Customer360/)

---

### Project 03: ADF Data Migration

**The problem:** CSV files arrive daily. Someone has to manually import them into SQL Server. This takes hours every week.

**What I built:** An Azure Data Factory pipeline that automatically detects new files, loads them, and tracks what has been processed.

**The result:** Zero manual work. Files processed within minutes of arrival. Full audit trail of every import.

[→ See the code](./03-Data-Migration-Project-End-To-End/)

---

### Project 04: Retail Data Engineering (with Quality Checks)

**The problem:** Bad data gets into reports. Nobody notices until the CFO asks why the numbers are wrong.

**What I built:** A pipeline with built-in validation. Before any transformation runs, the system checks:

```
✓ Does the file have data?
✓ Are all required columns present?
✓ Are there any null values in key fields?
✓ Are quantities and prices positive numbers?
```

**If any check fails, the pipeline stops.** Bad data never reaches the reports.

**The result:** Confidence. When you see a number, you know it is correct.

[→ See the code](./04-Retail-Data-Engineering/)

---

### Project 05: LMS Analytics (Daily Loads)

**The problem:** Student data arrives every day. You need to process it without reprocessing everything from scratch.

**What I built:** An incremental loading pipeline. Each day's data goes into its own partition. Queries only read what they need.

**The result:** Fast processing. Efficient storage. Easy troubleshooting when something goes wrong with one day's data.

[→ See the code](./05-Fabric-End-To-End/)

---

### Project 06: AWS MySQL to Azure Migration

**The problem:** Your database is in AWS. Your analytics team uses Azure. Someone needs to move the data.

**What I built:** A complete migration using Dataflow Gen2. No code required. Point, click, migrate.

**The result:** Data flows from AWS to Azure in minutes. Step-by-step guide included so your team can repeat this for other databases.

[→ See the code](./06-MySQL-to-Lakehouse-Migration/)

---

## How I Build Pipelines

Every pipeline follows the same proven pattern:

```
SOURCE → BRONZE → SILVER → GOLD → POWER BI
```

| Stage | What I Do | Why It Matters |
|-------|-----------|----------------|
| **Source** | Connect to CSV, JSON, Excel, MySQL | Your data is everywhere. I can reach it. |
| **Bronze** | Store raw data exactly as received | You can always go back to the original. |
| **Silver** | Clean, validate, standardize | Data quality problems stop here. |
| **Gold** | Aggregate, join, calculate KPIs | Reports are fast because the work is done. |
| **Power BI** | Build dashboards | Business users see insights, not tables. |

This is not my invention. Netflix uses this pattern. Airbnb uses it. Uber uses it. It works at scale.

---

## The Tech I Use

### Platforms
![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Microsoft Fabric](https://img.shields.io/badge/Microsoft_Fabric-742774?style=for-the-badge&logo=microsoft&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

### Languages & Tools
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

### Storage & Processing
![Delta Lake](https://img.shields.io/badge/Delta_Lake-00ADD8?style=for-the-badge&logo=databricks&logoColor=white)
![Parquet](https://img.shields.io/badge/Parquet-50ABF1?style=for-the-badge&logo=apache&logoColor=white)

### Visualization & DevOps
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

### Microsoft Fabric Skills
- **Lakehouse** — I know how to structure files and tables for fast queries
- **Dataflow Gen2** — I migrate databases without writing code
- **Notebooks** — I write PySpark transformations that scale
- **Semantic Models** — I connect data engineering to Power BI
- **OneLake Shortcuts** — I bridge AWS S3 to Azure without moving data
- **Capacity Management** — I monitor costs so you do not get surprised bills

---

## What I Learned

Building these projects taught me lessons that matter:

| Lesson | What Happened |
|--------|---------------|
| **Data quality is not optional** | One null OrderID broke three downstream reports. Now I validate everything. |
| **Automation saves hours** | Manual file processing took 4 hours per week. Pipeline does it in 4 minutes. |
| **Documentation is part of the job** | Nobody uses pipelines they cannot understand. I document everything. |
| **Simple patterns beat clever code** | Medallion Architecture is not exciting. It just works. Every time. |
| **Costs matter** | Fabric can get expensive fast. I learned to pause capacity and schedule workloads. |
| **Testing catches mistakes** | GitHub Actions found 3 bugs before they reached production. |

---

## How To Run These Projects

```bash
# Clone the repository
git clone https://github.com/lpalad/Azure-Projects-Data-AI-Engineering.git

# Pick a project
cd Azure-Projects-Data-AI-Engineering/04-Retail-Data-Engineering

# Read the README for that project
# Each one has specific setup instructions
```

### What You Need

| Tool | Why |
|------|-----|
| Microsoft Fabric account | To run the pipelines |
| Power BI Desktop | To view the dashboards |
| Python 3.11+ | To test scripts locally |
| Git | To clone this repository |

---

## About Me

**Leonard S Palad** | MBA | Master of AI (In Progress)

I build data systems that connect to business outcomes.

15 years of experience. Production ML systems. AWS pipelines. Azure migrations. Real projects with real results.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leonardspalad/)
[![Portfolio](https://img.shields.io/badge/AI_Portfolio-000000?style=for-the-badge&logo=github&logoColor=white)](https://salesconnect.com.au/aip.html)
[![Blog](https://img.shields.io/badge/Blog-FF5722?style=for-the-badge&logo=blogger&logoColor=white)](https://www.cloudhermit.com.au/)

### Other Work

| Repository | What It Shows |
|------------|---------------|
| [AWS Projects](https://github.com/lpalad/AWS-Projects) | Lambda, DynamoDB, IoT pipelines |
| [ML Lead Scoring](https://github.com/lpalad/mda) | Production ML that lifted sales 40-50% |

---

## Recent Updates

| Date | What Changed |
|------|--------------|
| January 2026 | Added CI/CD pipeline with automated testing |
| January 2026 | Added data quality framework |
| January 2026 | Added AWS MySQL migration guide |
| January 2026 | Added LMS incremental loading pipeline |
| January 2026 | Added Retail Data Engineering with validation |
| January 2026 | Added ADF migration project |
| January 2026 | Added Customer 360 pipeline |
| January 2026 | Added Medallion Retail Pipeline |

---

## License

MIT License - Use this code however you want.

---

<p align="center">
  <strong>I do not just write code. I build systems that work.</strong>
  <br><br>
  If you need someone who can migrate your data, build your pipelines, and make sure the numbers are right—let's talk.
</p>
