import requests
from config import VALIDATE_DATA_LEVEL_CODE_URL

def validate_codes(data, api_data, validation_logs):
    """Validate decrypted data against API data."""
    for key, value in data.items():
        if key not in ["status", "errorCode", "entryDate"] and (value is None or value == "null" or value == ""):
            validation_logs.append({
                "error": f"'{key}' is null or None in decrypted data.",
                "token": f'{data.get("token")}',
                "error_details": data
            })
            return False
    
    level_codes = {
        "level1Code": data.get("level1Code"),
        "level2Code": data.get("level2Code"),
        "level3Code": data.get("level3Code"),
        "level4Code": data.get("level4Code"),
        "level5Code": data.get("level5Code"),
        # "level6Code": data.get("level6Code"),
        # "level7Code": data.get("level7Code"),
        # "level8Code": data.get("level8Code"),
        # "level9Code": data.get("level9Code"),
        # "level10Code": data.get("level10Code"),
        "dataGranularityId": 43
    }
    
    if any(level_codes.values()):
        try:
            response = requests.post(VALIDATE_DATA_LEVEL_CODE_URL, json=level_codes)
            response.raise_for_status()
            result = response.text.strip()
            
            if result == "Invalid Level Code":
                validation_logs.append({
                    "error": "Invalid Level Code",
                    "error_details": {
                        "level_codes": level_codes,
                    }
                })
                return False
        except requests.RequestException as e:
            validation_logs.append({
                "error": f"Failed to validate level codes: {str(e)}",
                "error_details": {
                    "level_codes": level_codes,
                }
            })
            return False
    
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
            })
            return False
        
        try:
            if int(data_value) != int(api_value):
                validation_logs.append({
                    "error": f"{data_field} doesn't match: Decrypted data ({data_value}) != API data ({api_value}).",
                })
                return False
        except ValueError:
            validation_logs.append({
                "error": f"Invalid value for {data_field}.",
            })
            return False
    
    return True

def validate_data(lst):
    """Validate a list of decrypted data."""
    validation_logs = []
    previous_token = None
    api_data = None
    for data in lst:
        token = data.get("token")
        if not token:
            validation_logs.append({"error": "Missing token in data."})
            continue
        if token != previous_token:
            try:
                response = requests.get(f"http://10.23.124.59/getEncryptionKey?token={token}")
                response.raise_for_status()
                api_data = response.json()
                previous_token = token
            except requests.RequestException as e:
                validation_logs.append({"error": f"Failed to get encryption key: {str(e)}"})
                api_data = None
                previous_token = None
                continue
        if api_data is None:
            validation_logs.append({"error": "No valid API data available."})
            continue
        if not validate_codes(data, api_data, validation_logs):
            continue
    return validation_logs
