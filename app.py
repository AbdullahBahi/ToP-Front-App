from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

import os

# Load unit codes from a text file in the same directory as app.py
def load_unit_codes():
    file_path = os.path.join(os.path.dirname(__file__), 'unit_codes.txt')
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Home route with form
@app.route('/')
def index():
    unit_codes = load_unit_codes()
    payment_frequencies = ["Annually", "Semi-Annually", "Quarterly", "Monthly"]
    return render_template('index.html', unit_codes=unit_codes, payment_frequencies=payment_frequencies)

# Process API call and display results
@app.route('/calculate', methods=['POST'])
def calculate():
    # Extract data from JSON
    data = request.json
    # Separate input payments and other fields
    input_pmts = {
        key:value/100
        for key, value in data['input_pmts'].items()
        if key.isnumeric() and value is not None
    }

    if data.get('tenor_years') is None:
        tenor_years = 0
    else:
        tenor_years = data.get('tenor_years')

    if data.get('payment_frequency') is None:
        payment_frequency = "quarterly"
    else:
        payment_frequency = data.get('payment_frequency')
    
    # Prepare payload with the desired structure
    payload = {
        "unit_code": data.get('unit_code'),
        "tenor_years": tenor_years,
        "payment_frequency": payment_frequency,
        "input_pmts": input_pmts,  
        "contract_date":data.get('contract_date')
    }
    # Send a request to the API
    response = requests.post(
        'https://top-app-1h8s.onrender.com/calculate_installments',
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    # Return API response to the frontend for display
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to calculate installments"}), 500


if __name__ == '__main__':
    app.run(debug=True)
