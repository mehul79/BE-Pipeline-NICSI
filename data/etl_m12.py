import json
import logging
from datetime import datetime
import pandas as pd
import pytz
from config import OUTPUT_FILE_PATH
from logging_config import setup_logging
from api_utils import fetch_data_from_api, get_encryption_key
from decryption_utils import decrypt_java_api, decrypt_asp_dot_net_api, decrypt_php_data
from validation_utils import validate_data
import sys
import tempfile

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    # Return the validation logs for further processing
    return validation_logs

def get_current_date():
    # Get current time in UTC and convert to IST
    utc_now = datetime.now(pytz.utc)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_now = utc_now.astimezone(ist_timezone)
    return ist_now.date()  # Return only the date part

def main():
    setup_logging()
    input_data = fetch_data_from_api()
    decrypted_data = pragyan_dec(input_data)
    
    if decrypted_data:
        try:
            with open(OUTPUT_FILE_PATH, 'w') as f:
                json.dump(decrypted_data, f, indent=2)
            logger.info(f"Decrypted data written to {OUTPUT_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error writing to output file: {str(e)}")
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                json.dump(decrypted_data, temp_file, indent=2)
            logger.info(f"Decrypted data written to temporary file: {temp_file.name}")
        validation_logs = validate_data(decrypted_data)
    else:
        logger.error("No decrypted data found.")
        sys.exit(1)

    # Process logs to DataFrame
    validation_logs = process_logs(validation_logs)
    df = pd.DataFrame(validation_logs)

    # Log DataFrame details
    logger.info(f"DataFrame columns: {df.columns}")
    logger.info(f"DataFrame head:\n{df.head()}")

    # Instead of inserting into a database, you can perform additional processing here
    # For example, you can save the DataFrame to a CSV file
    output_csv = "validation_logs.csv"
    df.to_csv(output_csv, index=False)
    logger.info(f"Validation logs saved to {output_csv}")

    # You can also perform any other necessary operations with the data here

if __name__ == '__main__':
    main()