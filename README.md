<h1 align="center">
  <img src="m-fabric.webp" alt="Microsoft Fabric" width="100">
  <br>
  Azure Data Engineering Portfolio
</h1>

<p align="center">
  <strong>6 Production-Ready Pipelines | Real Migrations | Working Code</strong>
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

## Executive Summary: Engineering Profit Through Data Rigor

I do not simply "manage data." I build the systems that protect your company's margins and drive its growth.

With over 15 years of experience and an MBA, I bridge the gap between complex engineering and the boardroom.

My work in Microsoft Fabric and Azure is defined by three pillars:

| Pillar | What It Means | How I Deliver It |
|--------|---------------|------------------|
| **Certainty** | A report is only useful if it is 100% accurate | Automated data quality gates. If the data is wrong, the pipeline stops. |
| **Efficiency** | Human effort is expensive. Automation is not. | OneLake Shortcuts and Dataflow Gen2 eliminate data silos and manual toil. |
| **Fiscal Discipline** | Cloud capacity is a cost center, not a blank check | Fabric Capacity Management ensures analytics drive revenue without "bill shock." |

---

## 📋 What's Inside

1. [The Logic of Experience](#the-logic-of-experience-what-15-years-taught-me)
2. [The 6 Projects](#the-6-projects)
3. [How I Build Pipelines](#how-i-build-pipelines)
4. [The Tech I Use](#the-tech-i-use)
5. [About Me](#about-me)

---

## The Logic of Experience: What 15 Years Taught Me

Most engineers learn from documentation. I learned from production.

These are the non-negotiable rules I apply to every project:

### 1. Data Quality Is Not Optional

One null value in a primary key can destroy a million-dollar decision.

I learned that it is better to stop a pipeline than to deliver a lie. Now, I validate every row before it moves forward.

```
✓ Does the file have data?
✓ Are all required columns present?
✓ Are there any null values in key fields?
✓ Are quantities and prices positive numbers?

If any check fails → Pipeline stops. Bad data never reaches reports.
```

### 2. Automation Is Freedom

Manual work is the birthplace of human error.

I use GitHub Actions and ADF triggers because a script does not get tired. A script does not forget a step. A script runs at 3am without complaint.

**Before automation:** 4 hours per week of manual file processing.
**After automation:** 4 minutes. Zero human intervention.

### 3. Simplicity Wins Over Cleverness

"Clever" code is a nightmare to maintain. The next person who reads it will curse your name.

I use the Medallion Architecture (Bronze → Silver → Gold) because it is a proven, boring, and indestructible pattern. Netflix uses it. Airbnb uses it. Uber uses it. It works at any scale.

### 4. Costs Are a Technical Requirement

In Microsoft Fabric, performance is easy. Lowering the bill is hard.

I build pipelines that process only what is necessary. Incremental loading. Partitioned storage. Scheduled workloads during off-peak hours. I protect the bottom line because I understand that every dollar spent on compute is a dollar not spent on growth.

---

## The 6 Projects

### Project 01: Medallion Retail Pipeline
> 🔴 Messy raw data → 🟢 Report-ready tables

**The problem:** Raw retail data is messy. Column names have typos. Dates are in wrong formats. You cannot build reports on this.

**What I built:** A three-layer pipeline that takes messy data and makes it clean.

| Layer | What Happens |
|-------|--------------|
| Bronze | Raw data comes in. I do not touch it. |
| Silver | I fix column names. I parse dates. I validate types. |
| Gold | I calculate TotalSales, GrossProfit, ProfitMargin. Ready for Power BI. |

**The result:** Clean data. Accurate reports. Stakeholders who trust the numbers.

[→ See the code](./01-Medallion-Retail-Pipeline/)

---

### Project 02: Customer 360
> 🔴 5 scattered systems → 🟢 One unified view

**The problem:** Customer data is scattered across 5 different systems. Sales cannot see the full picture. Marketing cannot personalize. Support cannot anticipate.

**What I built:** A pipeline that joins Customers, Orders, Payments, Support Tickets, and Web Activity into one unified view.

**The result:** One table with everything you need to know about each customer. Sales stops asking IT for reports. They just look at the dashboard.

[→ See the code](./02-E-Commerce-Customer360/)

---

### Project 03: ADF Data Migration
> 🔴 Manual imports → 🟢 Zero-touch automation

**The problem:** CSV files arrive daily. Someone has to manually import them into SQL Server. This takes hours every week. Errors happen. Files get missed.

**What I built:** An Azure Data Factory pipeline that automatically detects new files, loads them, and tracks what has been processed.

**The result:** Zero manual work. Files processed within minutes of arrival. Full audit trail of every import. The person who used to do this manually now does higher-value work.

[→ See the code](./03-Data-Migration-Project-End-To-End/)

---

### Project 04: Retail Data Engineering (with Quality Gates)
> 🔴 Bad data reaches reports → 🟢 Quality gates stop it

**The problem:** Bad data gets into reports. Nobody notices until the CFO asks why the numbers are wrong. By then, trust is damaged.

**What I built:** A pipeline with built-in validation. Before any transformation runs, the system checks every row against quality rules.

**If any check fails, the pipeline stops.** Bad data never reaches the reports. The team gets alerted. The problem gets fixed at the source.

**The result:** Confidence. When you see a number, you know it is correct. When the CFO asks, you have an answer.

[→ See the code](./04-Retail-Data-Engineering/)

---

### Project 05: LMS Analytics (Incremental Loads)
> 🔴 Full reprocessing daily → 🟢 Incremental loads only

**The problem:** Student data arrives every day. Reprocessing everything from scratch is slow and expensive. But you cannot miss a single day.

**What I built:** An incremental loading pipeline. Each day's data goes into its own partition. Queries only read what they need. Storage costs stay low.

**The result:** Fast processing. Efficient storage. Easy troubleshooting when something goes wrong with one specific day.

[→ See the code](./05-Fabric-End-To-End/)

---

### Project 06: AWS MySQL to Azure Migration
> 🔴 Cross-cloud complexity → 🟢 Migration in minutes

**The problem:** Your database is in AWS. Your analytics team uses Azure. Someone needs to move the data without losing a single row.

**What I built:** A complete migration using Dataflow Gen2. No code required. Point, click, migrate. Step-by-step guide included.

**The result:** Data flows from AWS to Azure in minutes. Your team can repeat this for other databases without calling a consultant.

[→ See the code](./06-MySQL-to-Lakehouse-Migration/)

---

## How I Build Pipelines

Every pipeline follows the same proven pattern:

```
SOURCE → BRONZE → SILVER → GOLD → POWER BI
```

| Stage | What I Do | Why It Matters |
|-------|-----------|----------------|
| **Source** | Connect to CSV, JSON, Excel, MySQL, APIs | Your data is everywhere. I can reach it. |
| **Bronze** | Store raw data exactly as received | You can always go back to the original. Auditors love this. |
| **Silver** | Clean, validate, standardize | Data quality problems die here. They do not spread. |
| **Gold** | Aggregate, join, calculate KPIs | Reports are fast because the heavy lifting is done. |
| **Power BI** | Build dashboards | Business users see insights, not tables. |

This is not my invention. It is an industry standard. I use it because it works.

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

### Microsoft Fabric Expertise

| Component | What I Do With It |
|-----------|-------------------|
| **Lakehouse** | Structure files and tables for fast queries and low storage costs |
| **Dataflow Gen2** | Migrate databases without writing code |
| **Notebooks** | Write PySpark transformations that scale to millions of rows |
| **Semantic Models** | Connect data engineering to Power BI for self-service analytics |
| **OneLake Shortcuts** | Bridge AWS S3 to Azure without moving or duplicating data |
| **Capacity Management** | Monitor and optimize costs to prevent bill shock |

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

### Prerequisites

| Tool | Why You Need It |
|------|-----------------|
| Microsoft Fabric account | To run the pipelines |
| Power BI Desktop | To view the dashboards |
| Python 3.11+ | To test scripts locally |
| Git | To clone this repository |

---

## About Me

**Leonard S Palad** | MBA | Master of AI (In Progress)

I build data systems that connect to business outcomes.

15 years of experience. Production ML systems. AWS pipelines. Azure migrations. Real projects with real results.

I do not just write code. I build systems that protect margins, drive growth, and earn trust.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leonardspalad/)
[![Portfolio](https://img.shields.io/badge/AI_Portfolio-000000?style=for-the-badge&logo=github&logoColor=white)](https://salesconnect.com.au/aip.html)
[![Blog](https://img.shields.io/badge/Blog-FF5722?style=for-the-badge&logo=blogger&logoColor=white)](https://www.cloudhermit.com.au/)

### Other Work

| Repository | What It Demonstrates |
|------------|----------------------|
| [AWS Projects](https://github.com/lpalad/AWS-Projects) | Lambda, DynamoDB, IoT pipelines at scale |
| [ML Lead Scoring](https://github.com/lpalad/mda) | Production ML that lifted sales conversion 40-50% |

---

## Recent Updates

| Date | What Changed |
|------|--------------|
| January 2026 | Added CI/CD pipeline with automated testing |
| January 2026 | Added data quality framework |
| January 2026 | Added AWS MySQL to Azure migration guide |
| January 2026 | Added LMS incremental loading pipeline |
| January 2026 | Added Retail Data Engineering with quality gates |
| January 2026 | Added ADF migration project |
| January 2026 | Added Customer 360 pipeline |
| January 2026 | Added Medallion Retail Pipeline |

---

## License

MIT License - Use this code however you want.

---

<p align="center">
  <strong>I do not just manage data. I engineer profit.</strong>
  <br><br>
  If you need someone who can migrate your databases, build pipelines that never fail, and make sure every number is right—let's talk.
</p>
