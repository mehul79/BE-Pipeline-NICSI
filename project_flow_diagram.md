# Airflow ETL Pipeline - Complete Flow Diagram

## Flow Description

### 1. System Initialization

- Docker services start (Airflow, PostgreSQL, pgAdmin, Flask API)
- Database initialization and table creation
- Web interfaces become available

### 2. Daily ETL Pipeline (final_etl DAG)

- **Task 1**: Fetch encrypted data from external APIs via Flask server
- **Task 2**: Validate API responses and data integrity
- **Task 3**: Set up logging infrastructure and create daily log tables
- **Task 4**: Retrieve encryption keys and decrypt data using appropriate algorithms
- **Task 5**: Validate decrypted data against external validation APIs
- **Task 6**: Process and store final results in PostgreSQL

### 3. Data Migration Pipeline (data_migrations DAG)

- **Task 1**: Create database tables with dynamic naming
- **Task 2**: Execute local database ETL operations

### 4. Real-time Data Reception

- External APIs send encrypted data to Flask server
- Server processes data, extracts tokens, and retrieves encryption keys
- Data is stored for later processing by ETL pipelines

### 5. Monitoring and Management

- Users can monitor DAG execution through Airflow web UI
- Database management through pgAdmin interface
- Real-time data access through Flask API endpoints

### 6. Error Handling and Logging

- Comprehensive error logging to PostgreSQL tables
- Decryption logs for debugging
- Validation logs for data quality monitoring
- Task status reporting to Airflow scheduler

This diagram shows the complete end-to-end flow of your Airflow ETL system, including all components, data flows, and error handling mechanisms.
