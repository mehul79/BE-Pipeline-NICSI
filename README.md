# 🔄 Airflow ETL Pipeline

A comprehensive ETL (Extract, Transform, Load) pipeline built with Apache Airflow for automated data processing, encryption/decryption, validation, and database operations. This project demonstrates modern data engineering practices with containerized deployment and real-time data processing capabilities.

📋 Overview
This Airflow-based ETL system processes encrypted data from multiple API sources, performs decryption using various algorithms (Java, ASP.NET, PHP), validates data integrity, and stores results in PostgreSQL databases. The system features automated scheduling, comprehensive logging, and robust error handling.

🏗️ Architecture
🔧 Apache Airflow (Python + Docker)

- Automated DAG scheduling and task orchestration
- Bash operators for modular task execution
- Comprehensive logging and monitoring
- Containerized deployment with Docker Compose

🌐 Flask API Server (Python + Flask)

- RESTful API endpoints for data reception
- CORS-enabled cross-origin requests
- Real-time data processing and encryption key management
- Token-based authentication and validation

🗄️ Database Layer (PostgreSQL + SQLAlchemy)

- Dynamic table creation with date-based naming
- Structured logging with timestamps
- Connection pooling and session management
- Data persistence and retrieval operations

🔐 Security & Encryption

- Multi-language decryption support (Java, ASP.NET, PHP)
- Token-based encryption key retrieval
- Secure data validation and integrity checks
- Encrypted data processing pipeline

🚀 Features
Core ETL Operations
✅ Automated data extraction from multiple API sources
✅ Multi-language decryption (Java, ASP.NET, PHP)
✅ Comprehensive data validation and integrity checks
✅ Dynamic database table creation and management
✅ Real-time logging and error tracking

Data Processing
✅ Token-based encryption key management
✅ Level code validation against external APIs
✅ Data granularity and hierarchy validation
✅ CSV export and temporary file handling
✅ Timezone-aware timestamp processing

Infrastructure
✅ Docker containerization with multi-service architecture
✅ Apache Airflow web interface and scheduler
✅ PostgreSQL database with pgAdmin interface
✅ Flask API server for data reception
✅ Comprehensive health checks and monitoring

🛠️ Quick Setup
Prerequisites
Python 3.8+, Docker, Docker Compose, PostgreSQL

1. Clone Repository

```bash
git clone <repository-url>
cd airflow_tutorial
```

2. Start Services

```bash
docker-compose up -d
```

3. Access Services

- Airflow Web UI: http://localhost:8080 (username: mehul, password: mehul)
- Flask API: http://localhost:5001
- pgAdmin: http://localhost:15432 (email: rahul2222@gmail.com, password: postgres)
- PostgreSQL: localhost:5434

4. Initialize DAGs
   The system will automatically load DAGs from the `dags/` directory and start processing based on the configured schedule.

📁 Project Structure

```
airflow_tutorial/
├── dags/                          # Apache Airflow DAG definitions
│   ├── final_etl.py              # Main ETL pipeline with 6-step workflow
│   ├── data_migrations.py        # Database migration and setup DAG
│   └── tomtom/                   # Additional DAG configurations
├── data/                         # Core ETL processing modules
│   ├── config.py                 # Configuration and API endpoints
│   ├── database.py               # Database models and connection setup
│   ├── etl_m12.py               # Main ETL processing logic
│   ├── api_utils.py             # API data fetching utilities
│   ├── decryption_utils.py      # Multi-language decryption functions
│   ├── validation_utils.py      # Data validation and integrity checks
│   └── logging_config.py        # Logging configuration setup
├── docker-compose.yaml          # Multi-service container orchestration
├── Dockerfile                   # Airflow container configuration
├── requirements.txt             # Python dependencies
└── flask_app.py                # Flask API server for data reception
```

🔧 DAG Workflows
Main ETL Pipeline (final_etl.py)

1. **fetch_the_api** - Retrieves data from external APIs
2. **validate_the_api** - Validates API responses and data integrity
3. **log_the_data** - Configures logging and error tracking
4. **decrypt_the_data** - Decrypts data using appropriate algorithms
5. **validate_the_data** - Performs comprehensive data validation
6. **final_etl_processing** - Processes and stores final results

Data Migration Pipeline (data_migrations.py)

1. **table_created** - Creates database tables with dynamic naming
2. **fetch_the_api** - Executes local database ETL operations

🔐 Decryption Support
The system supports decryption for multiple programming languages:

- **Java API** - decrypt_java_api()
- **ASP.NET API** - decrypt_asp_dot_net_api()
- **PHP Data** - decrypt_php_data()

Each decryption method is automatically selected based on the portLanguageId retrieved from the encryption key API.

📊 Data Validation
Comprehensive validation includes:

- Level code validation against external APIs
- Field integrity checks (ministryCode, projectCode, sectorCode, deptCode)
- Null/empty value detection
- Token-based authentication validation
- Data granularity verification

🗄️ Database Schema
Dynamic table creation with date-based naming:

```sql
CREATE TABLE logs_YYYY-MM-DD (
    id SERIAL PRIMARY KEY,
    error VARCHAR,
    token VARCHAR,
    error_details TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

🌐 API Endpoints
Flask Server (Port 5001):

- `POST /recvApiData` - Receive and process API data
- `GET /getData` - Retrieve stored data and encryption keys

External APIs:

- Data API: `http://localhost:3000/getData`
- Encryption Key API: `http://localhost:3000/getEncryptionKey?token=`
- Validation API: `http://10.23.124.59:2222/validateDataLevelCode`

🔧 Configuration
Environment Variables:

```bash
DATABASE_URL="postgresql://postgres:postgres@10.25.53.161:5432/demo"
AIRFLOW_UID=50000
AIRFLOW_WWW_USER_USERNAME=mehul
AIRFLOW_WWW_USER_PASSWORD=mehul
```

📝 About ETL, Cron Jobs, and Apache Airflow

**ETL (Extract, Transform, Load)** is a data integration process that:

- **Extract**: Retrieves data from various sources (APIs, databases, files)
- **Transform**: Cleans, validates, and processes data into the desired format
- **Load**: Stores processed data into target systems (databases, data warehouses)

**Cron Jobs** are time-based task schedulers in Unix-like systems that execute commands at specified intervals. While useful for simple automation, they lack the sophisticated orchestration, monitoring, and error handling capabilities needed for complex data pipelines.

**Apache Airflow** is a modern workflow orchestration platform that:

- Provides visual DAG (Directed Acyclic Graph) representation of workflows
- Offers built-in scheduling, monitoring, and alerting
- Supports complex dependencies and conditional execution
- Includes comprehensive logging and debugging tools
- Enables parallel task execution and resource management
- Provides a web-based UI for workflow management and monitoring

This project demonstrates how Airflow can replace traditional cron jobs with a more robust, scalable, and maintainable solution for data pipeline orchestration.

🤝 Contributing
Contributions are greatly appreciated! This project welcomes:

- Bug reports and feature requests
- Code improvements and optimizations
- Documentation enhancements
- Testing and validation improvements
- Performance optimizations

Please feel free to submit pull requests or open issues to help improve this ETL pipeline.

👨‍💻 Author Notes
Built by Mehul Gupta as a comprehensive ETL solution demonstrating modern data engineering practices. This project showcases the power of Apache Airflow for orchestrating complex data workflows, implementing secure data processing with multi-language decryption support, and building scalable data pipelines with containerized deployment.

Happy data processing! 🔄
