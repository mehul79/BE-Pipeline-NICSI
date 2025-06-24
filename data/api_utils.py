import requests
from config import DATA_API_URL, ENCRYPTION_KEY_API_URL
import logging

def fetch_data_from_api():
    try:
        response = requests.get(DATA_API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except Exception as e:
        logging.error(f"Error fetching data from API: {str(e)}")
        return []

def get_encryption_key(token):
    try:
        response = requests.get(f"{ENCRYPTION_KEY_API_URL}{token}")
        response.raise_for_status()
        data = response.json()
        encryption_key = data.get('encryptionKey')
        if encryption_key == "Invalid Token":
            return None, None
        return encryption_key, data.get('portLanguageId')
    except Exception as e:
        logging.error(f"Error fetching encryption key: {str(e)}")
        return None, None
