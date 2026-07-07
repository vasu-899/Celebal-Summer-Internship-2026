# Week 4 - Azure Cloud Fundamentals and Data Pipeline
## Celebal Technologies Summer Internship 2026

## Objective
Build an end-to-end data pipeline using Azure Storage Account and Azure Data Factory (ADF).

## Architecture
Blob Storage (CSV)

↓

Linked Service (BlobStorageLinkedService)

↓

ADF Pipeline (SuperstorePipeline)

↓

Get Metadata Activity (Validate file info)

↓

Copy Data Activity (Source → Destination)

↓

Output (output/output.csv in Blob Storage)

## Tools & Services Used
- Azure Portal
- Azure Resource Group
- Azure Storage Account + Blob Container
- Azure Data Factory (ADF) V2

## Project Structure

celebal_week4/

├── screenshots/          # All task screenshots

├── week4_summary.md      # Detailed summary and insights

└── README.md             # Project overview

## Tasks Completed
| Task | Description | Status |
|------|-------------|--------|
| Task 1 | Resource Group created | ✅ |
| Task 2 | Storage Account + Blob Container + CSV uploaded | ✅ |
| Task 3 | ADF created + Linked Service + Datasets + Get Metadata | ✅ |
| Task 4 | Pipeline with Copy Data activity | ✅ |
| Task 5 | Pipeline executed successfully | ✅ |
| Task 6 | IAM Roles (Reader + Contributor) assigned | ✅ |
| Mini Project | Blob → ADF → Destination pipeline | ✅ |

## Pipeline Flow
1. **Get Metadata Activity** — Validates source file (column count, size, item name)
2. **Copy Data Activity** — Copies CSV from source container to destination folder

## Key Learnings
- Azure Resource Group organizes all cloud resources
- Blob Storage stores unstructured data like CSV files
- Linked Service connects ADF to external data sources
- Get Metadata validates file before processing
- IAM roles control access between Azure services