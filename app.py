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
    return render_template('index.html', unit_codes=unit_codes)

# Process API call and display results
@app.route('/calculate', methods=['POST'])
def calculate():
    # Extract data from JSON
    data = request.json
    # Separate input payments and other fields
    input_pmts = {
        key:value
        for key, value in data['input_pmts'].items()
        if key.isnumeric() and value is not None
    }

    # Prepare payload with the desired structure
    payload = {
        "unit_code": data.get('unit_code'),
        "tenor_years": data.get('tenor_years'),
        "periods_per_year": data.get('periods_per_year'),
        "input_pmts": input_pmts,  # Only include non-None payment values
        "interest_rate": data.get('interest_rate'),
        "base_dp": data.get('base_dp'),
        "base_tenor_years": data.get('base_tenor_years'),
        "base_periods_per_year": data.get('base_periods_per_year'),
        "max_discount": data.get('max_discount')
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
