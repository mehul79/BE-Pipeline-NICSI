from numbers import Number
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

print("njdnsfkjndslnglndsl")
app = Flask(__name__)
CORS(app)

# Global variables to store data
stored_data = []
portLanguageId = None
encryptionKey = None

@app.route('/recvApiData', methods=['POST'])
def receive_api_data():
    global stored_data, portLanguageId, encryptionKey
    try:
        # Get data from the POST request
        data = request.json

        # Check if data is a list
        if not isinstance(data, list):
            return jsonify({'error': 'Data should be a list of dictionaries'}), 400

        # Store all the incoming data
        stored_data = data

        # Extract token values, ignoring 0 and null values
        tokens = [item.get('token') for item in data if isinstance(item, dict) and item.get('token') not in (0, None)]

        # Remove duplicates while preserving order
        unique_tokens = []
        seen = set()
        for token in tokens:
            if token not in seen:
                seen.add(token)
                unique_tokens.append(token)
        print(unique_tokens)
        if unique_tokens:
            my_token = unique_tokens[0]
            api_url = f"http://10.23.124.59/getEncryptionKey?token={my_token}"
            print("api_url",api_url)
            response = requests.get(api_url)
            my_data = response.json()
            portLanguageId = my_data['portLanguageId']
            print(portLanguageId)
            encryptionKey = my_data['encryptionKey']
            print(encryptionKey)

        return jsonify({'message': 'Data received and processed successfully', "token": unique_tokens}), 200

    except Exception as e:
        # print(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/getData', methods=['GET'])
def get_data():
    global stored_data, portLanguageId, encryptionKey
    return jsonify({
        'data': stored_data,
        'portLanguageId': portLanguageId,
        'encryptionKey': encryptionKey
    })

if __name__ == '__main__':
    print("Server is running. Waiting for data at http://localhost:5001/recvApiData")
    app.run(host='0.0.0.0', port=5001, debug=True)



