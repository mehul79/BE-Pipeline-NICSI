import argparse
from pathlib import Path

from etl_model import Connection
import config

# Initialize DATA Table
def main(db_connection):
    # Path(config.CSV_FILE_DIR).mkdir(parents=True, exist_ok=True)
    
    connection = Connection(db_connection)
    session = connection.get_session()
    session.execute('''CREATE TABLE IF NOT EXISTS megaphone (
    error_type INT,
    token INT, 
    error_details INT, 
    datatime TIMESTAMP)''')
    session.commit()
    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--connection", required=True, type=str)
    args = parser.parse_args()
    main(args.connection)