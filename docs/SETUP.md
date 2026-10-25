# Local Setup Guide

## Prerequisites

- Python 3.12
- Git
- Docker (optional, for containerized tests)
- Access to Azure resources for running the cloud pipeline

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/retail-intelligence-platform.git
cd retail-intelligence-platform
```

Replace `YOUR_USERNAME` with your GitHub username.

## 2. Set Up the Python Test Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

Install the test dependencies:

```bash
pip install -r tests/requirements.txt
```

## 3. Run the Tests

```bash
pytest -v tests/
```

## 4. Run the Tests with Docker

From the repository root:

```bash
docker build -t retail-intelligence-platform .
docker run --rm retail-intelligence-platform
```

## 5. Cloud Pipeline

The Databricks notebook uses Azure Data Lake Storage Gen2, Delta Lake, and Azure SQL Database. Configure cloud access through the appropriate Azure identity and secret-management mechanisms before executing it.

Never commit passwords, access keys, connection strings, or production data.

## Current Limitations

The local tests validate sample retail data. They do not yet execute the cloud pipeline end to end. Airflow orchestration and failure notifications are planned enhancements.
