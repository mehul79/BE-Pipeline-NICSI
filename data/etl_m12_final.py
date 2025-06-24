import os
import json
import logging
import sys
import base64
import tempfile
from venv import logger
# from fastapi.background import P
import requests
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import pandas as pd
# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('decryption.log'),
        logging.StreamHandler()
    ]
)

try:
    # print("NICSI")
    incoming_data = requests.get("http://10.25.53.161:5001/getData")
    data = incoming_data.json()
    input_data = data['data'] 
except Exception as e:
    # logging.error(f"Error fetching data from API: {str(e)}")
    sys.exit(1)

# Define output file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = 'decrypted_data.json'
output_file_path = os.path.join(BASE_DIR, OUTPUT_FILE)



def decrypt_java_api(encrypted_text, key):
    try:
        # logging.info(f"Attempting to decrypt text: {encrypted_text[:50]}...")
        secret_key = key.encode('utf-8')
        if len(secret_key) not in [16, 24, 32]:
            raise ValueError(f"Invalid key length: {len(secret_key)}. Key must be 16, 24, or 32 bytes long.")
        iv = b'\x00' * 16  # ECB mode doesn't use IV, but we need it for the Cipher object
        cipher = Cipher(algorithms.AES(secret_key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(base64.b64decode(encrypted_text)) + decryptor.finalize()
        padding_length = decrypted_bytes[-1]
        decrypted_text = decrypted_bytes[:-padding_length].decode('utf-8')
        # print("decrypted_mera: ",decrypted_text)
        return decrypted_text
    except Exception as e:
        # logging.error(f"Decryption error in decrypt_java_api: {str(e)}")
        # print("decrypted_mera: ",decrypted_text)
        return encrypted_text  # Return the original encrypted text if decryption fails

def decrypt_asp_dot_net_api(encrypted_text_asp, key_asp_dot_net):
    try:
        # logging.info(f"Attempting to decrypt text: {encrypted_text_asp[:50]}...")
        secret_key = key_asp_dot_net.encode('utf-8')
        if len(secret_key) not in [16, 24, 32]:
            raise ValueError(f"Invalid key length: {len(secret_key)}. Key must be 16, 24, or 32 bytes long.")
        iv = b'\x00' * 16  # ECB mode doesn't use IV, but we need it for the Cipher object
        cipher = Cipher(algorithms.AES(secret_key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(base64.b64decode(encrypted_text_asp)) + decryptor.finalize()
        padding_length = decrypted_bytes[-1]
        decrypted_text = decrypted_bytes[:-padding_length].decode('utf-8')
        # print("decrypted_mera: ",decrypted_text)
        return decrypted_text
    except Exception as e:
        # logging.error(f"Decryption error in decrypt_asp_dot_net_api: {str(e)}")
        print("decrypted_mera: ",decrypted_text)
        return encrypted_text_asp  # Return the original encrypted text if decryption fails

def decrypt_php_data(encrypted_text, key):
    try:
        combined_bytes = base64.b64decode(encrypted_text)
        iv = combined_bytes[:16]
        encrypted_bytes = combined_bytes[16:]

        secret_key = key.encode('utf-8')
        cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()
        
        padding_length = decrypted_bytes[-1]
        decrypted_text = decrypted_bytes[:-padding_length].decode('utf-8')
        return decrypted_text
    except Exception as e:
        # logging.error(f"Decryption Error in decrypt_php_data: {str(e)}")
        return encrypted_text

encryption_key = None
port_language_id = None




api_count = 0 # variable used to count number of api calls to this api - getEncryptionKey
def get_encryption_key(token):
    global encryption_key, port_language_id, api_count
    try:
        response = requests.get(f"http://10.23.124.59/getEncryptionKey?token={token}")
        api_count += 1
        data = response.json()
        # print(data)
        encryption_key = data.get('encryptionKey')
        # print(encryption_key)
        if encryption_key == "Invalid Token":
            # logging.warning(f"Invalid token encountered: {token}")
            encryption_key = None
            port_language_id = None
            return False
        
        port_language_id = data.get('portLanguageId')
        # print(port_language_id)
        # logging.info(f"Updated encryption key and portLanguageId for token: {token}")
        return True
    except Exception as e:
        # logging.error(f"Error fetching encryption key: {str(e)}")
        encryption_key = None
        port_language_id = None
        return False


def decrypt_data(encrypted_text, key, portLanguageId):
    decryption_functions = {
        1: decrypt_java_api,
        2: decrypt_asp_dot_net_api,
        3: decrypt_php_data, 
    }

    decrypt_function = decryption_functions.get(portLanguageId)
    if decrypt_function:
        return decrypt_function(encrypted_text, key)
    else:
        # logging.error(f"Unsupported portLanguageId: {portLanguageId}")
        return encrypted_text

def pragyan_dec():
    decrypted_list = []
    verify_token = ''

    try:
        for item in input_data:
            token = item.get("token")
            
            if token is None or token == "0":
                # logging.warning(f"Null or '0' token encountered. Skipping decryption for this item. Token: {token}")
                continue

            if token != verify_token:
                # logging.info(f"New token encountered: {token}")
                if not get_encryption_key(token):
                    # logging.warning(f"Skipping decryption for invalid token: {token}")
                    decrypted_list.append(item)  # Add the original item without decryption
                    continue
                verify_token = token

            if not encryption_key or port_language_id is None:
                # logging.warning(f"No valid encryption key for token: {token}. Skipping decryption.")
                decrypted_list.append(item)  # Add the original item without decryption
                continue

            decrypted_entry = {}
            for key, value in item.items():

                #prevents key named "token" to not to decrypt
                if key == "token":
                    decrypted_entry[key] = value
                    # logging.info(f"Skipping decryption for key: {key}")

                #remove the key named apiLanguageId
                elif key == "apiLanguageId":
                    # logging.info(f"Skipping decryption for key: {key}")
                    continue
                

                elif value is not None and isinstance(value, str):
                    # logging.info(f"Decrypting value for {key}: {value[:50]}...")
                    try:
                        decrypted_value = decrypt_data(value, encryption_key, port_language_id)
                        if decrypted_value is not None:
                            decrypted_entry[key] = decrypted_value
                        else:
                            # logging.warning(f"Decryption failed for {key}, using original value")
                            decrypted_entry[key] = value
                    except Exception as e:
                        # logging.error(f"Decryption error for {key}: {str(e)}")
                        decrypted_entry[key] = value
                else:
                    decrypted_entry[key] = value

            decrypted_list.append(decrypted_entry)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

    return decrypted_list


lst = []

def main():

    # logging.info(f"Current working directory: {os.getcwd()}")
    # logging.info(f"Output file path: {output_file_path}")

    decrypted_data = pragyan_dec()
    
    if decrypted_data:
        try:
            with open(output_file_path, 'w') as f:
                json.dump(decrypted_data, f, indent=2)
            # logging.info(f"Decrypted data written to {output_file_path}")
        except Exception as e:
            logging.error(f"Error writing to output file: {str(e)}")
            # Fallback to writing to a temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                json.dump(decrypted_data, temp_file, indent=2)
            # logging.info(f"Decrypted data written to temporary file: {temp_file.name}")

        lst.extend(decrypted_data)
        validate_data(lst)
        #call the validate data function

    else:
        # logging.error("No data was decrypted.")
        sys.exit(1)






#logic for validation of incoming minstrycode sectorcode granulityId levelcodes 
validation_logs = []
def validate_codes(data, api_data, validation_logs):
    # Validate that no field (except status, errorCode, and entryDate) is null or None
    for key, value in data.items():
        if key not in ["status", "errorCode", "entryDate"] and (value is None or value == "null"):
            validation_logs.append({
                "error": f"'{key}' is null or None in decrypted data.",
                "token":f'{data.get("token")}',
                "error_details": data
            })
            return False
     # Validate level codes
    level_codes = {
        "level1Code": data.get("level1Code"),
        "level2Code": data.get("level2Code"),
        "level3Code": data.get("level3Code"),
        "level4Code": data.get("level4Code"),
        "level5Code": data.get("level5Code"),
        "dataGranularityId": 43
    }
    
    # Only proceed if we have at least one level code
    if level_codes:
        try:
            response = requests.post("http://10.23.124.59:2222/validateDataLevelCode", json=level_codes)
            response.raise_for_status()
            result = response.text.strip()
            
            if result == "Invalid Level Code":
                validation_logs.append({
                    "error": "Invalid Level Code",
                    "error_details": {
                        "level_codes": level_codes,
                        # "full_data": data
                    }
                })
                return False
            # If valid, we don't log anything and continue with other validations
        except requests.RequestException as e:
            validation_logs.append({
                "error": f"Failed to validate level codes: {str(e)}",
                "error_details": {
                    "level_codes": level_codes,
                    # "full_data": data
                }
            })
            return False
    # Validate ministryCode, projectCode, sectorCode, and departmentCode
    fields_to_validate = [
        ("ministryCode", "ministryCode"),
        ("projectCode", "projectCode"),
        ("sectorCode", "sectorCode"),
        ("departmentCode", "deptCode")
    ]
    
    for data_field, api_field in fields_to_validate:
        data_value = data.get(data_field)
        api_value = api_data.get(api_field)
        
        if api_value is None:
            validation_logs.append({
                "error": f"{api_field} is missing in API data.",
                # "error_details": data
            })
            return False
        
        try:
            if int(data_value) != int(api_value):
                validation_logs.append({
                    "error": f"{data_field} doesn't match: Decrypted data ({data_value}) != API data ({api_value}).",
                    # "error_details": data
                })
                return False
        except ValueError:
            validation_logs.append({
                "error": f"Invalid value for {data_field}.",
                # "error_details": data
            })
            return False
    
    return True


validation_logs = []
def validate_data(lst):
    # global api_count
    global validation_logs
    previous_token = None
    api_data = None
    # validation_logs = []
    for data in lst:
        token = data.get("token")
        # data_id = data.get("id")
        if not token:
            validation_logs.append({
                "error": f"Missing token in data.",
                # "error_details": data
            })
            continue
        if token != previous_token:
            # New token encountered, make API call
            encryption_key_url = f"http://10.23.124.59/getEncryptionKey?token={token}"
            # print(encryption_key_url)
            try:
                # api_count += 1
                response = requests.get(encryption_key_url)
                response.raise_for_status()
                api_data = response.json()
                previous_token = token  # Update previous_token
                # logger.info(f"New API call made for token: {token}")  # Commented out
            except requests.RequestException as e:
                validation_logs.append({
                    "error": f"Failed to get encryption key: {str(e)}",
                    # "error_details": data
                })
                api_data = None
                previous_token = None  # Reset previous_token on failure
                continue
        # else:
            # logger.info(f"Reusing API data for token: {token}")  # Commented out
        # If we don't have valid API data, skip this iteration
        if api_data is None:
            validation_logs.append({
                "error": f"No valid API data available.",
                # "error_details": data
            })
            continue
        # Validate codes
        if not validate_codes(data, api_data, validation_logs):
            # validation_logs.append({
            #     "error": f"Validation failed for codes.",
            #     "error_details": data
            # })
            continue
        # If all validations pass, you can process the data further here
        # logger.info(f"Data validated successfully for id: {data_id}")  # Commented out
    return validation_logs  # Return the validation logs instead of True

             
if __name__ == "__main__":
    main()

def process_logs(validation_logs):
    for log in validation_logs:
        error_message = log.get('error', 'No error message')
        token = log.get('token', 'No token')
        error_details = log.get('error_details', 'No error details')
        print(f"Error: {error_message}")
        print(f"Token: {token}")
        print(f"Error Details: {error_details}\n")
process_logs(validation_logs) 

    # log_df = process_logs(validation_logs)
    # # print(log_df)
