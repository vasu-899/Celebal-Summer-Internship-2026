# Week 4 - Detailed Summary
## Azure Cloud Fundamentals and Data Pipeline using ADF

---

## Task 1: Resource Group
**What:** A Resource Group is a logical container for Azure resources.

**Why:** It helps organize and manage all related Azure services together.

**Steps Taken:**
- Navigated to Azure Portal
- Created Resource Group: `celebal-week4-rg`
- Region: East US

**Screenshot:** `screenshots/01_resource_group.png`

---

## Task 2: Storage Setup
**What:** Azure Blob Storage stores unstructured data like CSV files.

**Why:** ADF needs a source location to read data from.

**Steps Taken:**
- Created Storage Account: `celebalwk4vasu899`
- Created Blob Container: `superstore-data`
- Uploaded `Sample - Superstore.csv` to container

**Screenshots:**
- `screenshots/02_storage_account.png`
- `screenshots/03_blob_container.png`
- `screenshots/04_csv_uploaded.png`

---

## Task 3: ADF Setup
**What:** Azure Data Factory is a cloud ETL service for data integration.

**Why:** ADF orchestrates data movement and transformation.

**Steps Taken:**
- Created ADF instance: `celebal-week4-adf`
- Created Linked Service: `BlobStorageLinkedService` (connects ADF to Blob)
- Created Source Dataset: `SourceDataset` (points to CSV file)
- Created Destination Dataset: `DestinationDataset` (points to output folder)
- Added Get Metadata activity to validate:
  - Column count
  - File size
  - Item name

**Screenshots:**
- `screenshots/05_adf_overview.png`
- `screenshots/06_linked_service.png`
- `screenshots/07_source_dataset.png`
- `screenshots/08_destination_dataset.png`
- `screenshots/09_get_metadata.png`

---

## Task 4: Pipeline Development
**What:** A pipeline is a logical grouping of activities in ADF.

**Why:** Pipeline automates the data movement process.

**Pipeline Logic:**
1. Get Metadata → validates source file exists and has correct structure
2. Copy Data → copies data from source to destination

**Activities Used:**
- Get Metadata: Checks file metadata before processing
- Copy Data: Moves data from Blob source to Blob destination

**Screenshot:** `screenshots/10_pipeline_design.png`

---

## Task 5: Pipeline Execution
**What:** Pipeline was executed using Debug mode.

**Result:** Pipeline executed successfully — Status: Succeeded

**Execution Flow:**
- Get Metadata: Retrieved file info ✅
- Copy Data: Data copied to output folder ✅

**Screenshot:** `screenshots/11_pipeline_execution.png`

---

## Task 6: IAM Roles
**What:** IAM (Identity and Access Management) controls who can access Azure resources.

**Roles Assigned:**
- Reader: Read-only access to Resource Group
- Contributor: ADF Managed Identity given access to Storage Account

**Why:** ADF needs Contributor access to read/write data in Blob Storage.

**Screenshot:** `screenshots/12_iam_roles.png`

---

## Mini Project: End-to-End Pipeline
**Problem:** Read CSV from Blob Storage and copy to destination using ADF.

**Solution Architecture:**
Blob Storage (superstore-data/Sample-Superstore.csv)

↓

Linked Service (BlobStorageLinkedService)

↓

ADF Pipeline (SuperstorePipeline)

↓

Get Metadata Activity (validates file)

↓

Copy Data Activity (copies file)

↓

Destination (superstore-data/output/output.csv)

**Result:** Pipeline executed successfully with metadata validation ✅

---

## Key Insights
- Azure Resource Groups help organize cloud resources efficiently
- Blob Storage is ideal for storing large CSV/data files
- Linked Services act as connection strings in ADF
- Get Metadata ensures data quality before processing
- IAM roles are critical for secure access between services
- ADF pipelines automate ETL without writing any code