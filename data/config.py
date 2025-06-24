import os

# Set up base directory and file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = 'decrypted_data.json'
OUTPUT_FILE_PATH = os.path.join(BASE_DIR, OUTPUT_FILE)

# API URLs
DATA_API_URL = "http://localhost:3000/getData"
ENCRYPTION_KEY_API_URL = "http://localhost:3000/getEncryptionKey?token="
VALIDATE_DATA_LEVEL_CODE_URL = "http://10.23.124.59:2222/validateDataLevelCode"

# Logging configuration
LOG_FILE = 'decryption.log'
