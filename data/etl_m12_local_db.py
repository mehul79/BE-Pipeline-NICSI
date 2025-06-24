import json
import sys
import logging
import tempfile
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal, Log, init_db
from config import OUTPUT_FILE_PATH
from logging_config import setup_logging
from api_utils import fetch_data_from_api, get_encryption_key
from decryption_utils import decrypt_java_api, decrypt_asp_dot_net_api, decrypt_php_data
from validation_utils import validate_data

def decrypt_data(encrypted_text, key, portLanguageId):
    decryption_functions = {
        1: decrypt_java_api,
        2: decrypt_asp_dot_net_api,
        3: decrypt_php_data,
    }
    decrypt_function = decryption_functions.get(portLanguageId)
    if decrypt_function:
        return decrypt_function(encrypted_text, key)
    return encrypted_text

def pragyan_dec(input_data):
    decrypted_list = []
    verify_token = ''
    encryption_key = None
    port_language_id = None
    for item in input_data:
        token = item.get("token")
        if token is None or token == "0":
            continue
        if token != verify_token:
            encryption_key, port_language_id = get_encryption_key(token)
            verify_token = token
        if not encryption_key or port_language_id is None:
            decrypted_list.append(item)
            continue
        decrypted_entry = {}
        for key, value in item.items():
            if key == "token":
                decrypted_entry[key] = value
            elif key == "apiLanguageId":
                continue
            elif value is not None and isinstance(value, str):
                decrypted_entry[key] = decrypt_data(value, encryption_key, port_language_id)
            else:
                decrypted_entry[key] = value
        decrypted_list.append(decrypted_entry)
    return decrypted_list

def process_logs(validation_logs):
    db = SessionLocal()
    try:
        for log in validation_logs:
            logging.debug(f"Processing log: {log}")
            db_log = Log(
                error=log.get('error', 'No error message'),
                token=log.get('token', 'No token'),
                error_details=json.dumps(log.get('error_details'))  # Convert dict to JSON string
            )
            db.add(db_log)
            logging.debug(f"Log added to session: {db_log}")
        db.commit()
        logging.info("Logs committed to the database.")
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error inserting logs into database: {str(e)}")
        logging.exception(e)
    finally:
        db.close()

def main():
    setup_logging()
    logging.info("Starting main process.")
    
    # Ensure the database tables are created
    if init_db():
        logging.info("Database initialization successful.")
    else:
        logging.error("Database initialization failed. Exiting.")
        sys.exit(1)
    
    input_data = fetch_data_from_api()
    logging.debug(f"Fetched input data: {input_data}")
    
    decrypted_data = pragyan_dec(input_data)
    logging.debug(f"Decrypted data: {decrypted_data}")
    
    if decrypted_data:
        try:
            with open(OUTPUT_FILE_PATH, 'w') as f:
                json.dump(decrypted_data, f, indent=2)
            logging.info(f"Decrypted data written to {OUTPUT_FILE_PATH}")
        except Exception as e:
            logging.error(f"Error writing to output file: {str(e)}")
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                json.dump(decrypted_data, temp_file, indent=2)
            logging.info(f"Decrypted data written to temporary file {temp_file.name}")
        
        validation_logs = validate_data(decrypted_data)
        logging.debug(f"Validation logs: {validation_logs}")
        process_logs(validation_logs)
    else:
        logging.error("No decrypted data available. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
