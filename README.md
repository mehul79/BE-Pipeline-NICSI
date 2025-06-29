# 🔄 Airflow ETL Pipeline

A comprehensive **ETL (Extract, Transform, Load)** pipeline built with **Apache Airflow** for automated data processing, encryption/decryption, validation, and database operations. This project demonstrates modern data engineering practices with containerized deployment and real-time data processing capabilities.

---

## 📋 Overview

This Airflow-based ETL system:

- Processes encrypted data from multiple API sources
- Performs decryption using Java, ASP.NET, and PHP algorithms
- Validates data integrity
- Stores results in PostgreSQL

Key features:

- Automated scheduling
- Comprehensive logging
- Robust error handling

---

## 🏗️ Architecture

### 🔧 Apache Airflow (Python + Docker)

- Automated DAG scheduling and task orchestration  
- Bash operators for modular task execution  
- Logging and monitoring  
- Containerized with Docker Compose  

### 🌐 Flask API Server (Python + Flask)

- RESTful endpoints for data reception  
- CORS-enabled  
- Real-time data processing  
- Token-based authentication  

### 🗄️ Database Layer (PostgreSQL + SQLAlchemy)

- Dynamic table creation (date-based naming)  
- Structured logs with timestamps  
- Connection pooling  
- Data persistence and retrieval  

### 🔐 Security & Encryption

- Decryption support for Java, ASP.NET, PHP  
- Token-based encryption key management  
- Integrity and validation checks  
- Secure encrypted data pipeline  

---

## 🚀 Features

### ✅ Core ETL Operations

- Data extraction from multiple APIs  
- Multi-language decryption  
- Data validation and integrity checks  
- Dynamic PostgreSQL table creation  
- Logging and error tracking  

### ✅ Data Processing

- Token-based encryption key management  
- External API validation (level codes)  
- CSV export & temporary file handling  
- Timezone-aware timestamp processing  

### ✅ Infrastructure

- Docker-based multi-service setup  
- Airflow UI + Scheduler  
- PostgreSQL + pgAdmin  
- Flask API server  
- Health checks and monitoring  

---

## 🛠️ Quick Setup

### ✅ Prerequisites

- Python 3.8+  
- Docker + Docker Compose  
- PostgreSQL  

### ✅ Setup Steps

1. **Clone the Repository**

```bash
git clone <repository-url>
cd airflow_tutorial
```

2. **Start Services**

```bash
docker-compose up -d
```

3. **Access Interfaces**

- Airflow UI: [http://localhost:8080](http://localhost:8080) (user: `mehul`, pass: `mehul`)  
- Flask API: [http://localhost:5001](http://localhost:5001)  
- pgAdmin: [http://localhost:15432](http://localhost:15432) (email: `rahul2222@gmail.com`, pass: `postgres`)  
- PostgreSQL: `localhost:5434`  

4. **Initialize DAGs**

DAGs are automatically loaded from the `dags/` folder.

---

## 📁 Project Structure

```
airflow_tutorial/
├── dags/                  
│   ├── final_etl.py             # Main ETL DAG  
│   ├── data_migrations.py       # Migration DAG  
│   └── tomtom/                  # Additional DAGs  
├── data/                  
│   ├── config.py                # Config & endpoints  
│   ├── database.py              # DB setup & models  
│   ├── etl_m12.py               # ETL core logic  
│   ├── api_utils.py             # API fetching utils  
│   ├── decryption_utils.py      # Decryption functions  
│   ├── validation_utils.py      # Validation logic  
│   └── logging_config.py        # Logging setup  
├── docker-compose.yaml          # Multi-service orchestration  
├── Dockerfile                   # Airflow Docker image  
├── requirements.txt             # Python packages  
└── flask_app.py                 # Flask API server  
```

---

## 🔧 DAG Workflows

### 📌 `final_etl.py` - Main ETL Pipeline

1. **fetch_the_api** – Fetch external API data  
2. **validate_the_api** – Validate API data  
3. **log_the_data** – Configure logging  
4. **decrypt_the_data** – Decrypt based on algorithm  
5. **validate_the_data** – Final data validation  
6. **final_etl_processing** – Store processed data  

### 📌 `data_migrations.py` - Migration Workflow

1. **table_created** – Create PostgreSQL tables dynamically  
2. **fetch_the_api** – Perform local DB ETL operations  

---

## 🔐 Decryption Support

Supports automatic decryption based on `portLanguageId`:

- **Java** → `decrypt_java_api()`  
- **ASP.NET** → `decrypt_asp_dot_net_api()`  
- **PHP** → `decrypt_php_data()`  

---

## 📊 Data Validation

Includes:

- Level code verification from external APIs  
- Field integrity checks (`ministryCode`, `projectCode`, etc.)  
- Null/empty value detection  
- Token validation  
- Granularity & hierarchy validation  

---

## 🗄️ Dynamic Database Schema

Example:

```sql
CREATE TABLE logs_YYYY_MM_DD (
    id SERIAL PRIMARY KEY,
    error VARCHAR,
    token VARCHAR,
    error_details TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🌐 API Endpoints

### 🔌 Flask Server (Port `5001`)

- `POST /recvApiData` – Receive API data  
- `GET /getData` – Fetch stored/encrypted data  

### 🔗 External APIs

- Data API: `http://localhost:3000/getData`  
- Encryption Key API: `http://localhost:3000/getEncryptionKey?token=`  
- Validation API: `http://10.23.124.59:2222/validateDataLevelCode`  

---

## ⚙️ Configuration

### 🔑 Environment Variables

```bash
DATABASE_URL="postgresql://postgres:postgres@10.25.53.161:5432/demo"
AIRFLOW_UID=50000
AIRFLOW_WWW_USER_USERNAME=mehul
AIRFLOW_WWW_USER_PASSWORD=mehul
```

---

## 📝 About ETL, Cron Jobs, and Airflow

### 🔄 What is ETL?

- **Extract**: Gather data from sources  
- **Transform**: Clean, validate, reshape data  
- **Load**: Store into target DB or warehouse  

### ⏰ Why Not Cron Jobs?

- Lacks error tracking and conditional logic  
- Hard to monitor/scale/debug

### 🌀 Why Apache Airflow?

- Visual DAGs and workflow management  
- Built-in logging, retries, alerts  
- Parallel execution and scheduling  
- Web UI for monitoring  
- Modular, scalable, and production-grade  

---

## 🤝 Contributing

We welcome contributions including:

- 🐛 Bug reports & feature requests  
- ⚡ Code improvements  
- 🧪 Tests & validation  
- 📝 Documentation updates  
- 🚀 Performance optimizations  

Submit PRs or open issues to contribute!

---

## 👨‍💻 Author Notes

Created by **Mehul Gupta** to demonstrate a modern, production-ready ETL pipeline with Airflow, Docker, Flask, and PostgreSQL. Includes secure multi-language decryption, robust validation, and real-time processing.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

**Happy data processing! 🔄**