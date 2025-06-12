import os
from flask import Flask, jsonify, request, send_from_directory
import json

# Set static folder to absolute path of src/web
static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../web'))
app = Flask(__name__, static_folder=static_folder)

# Load district data from the root folder
with open('districts.json', 'r', encoding='utf-8') as f:
    districts = json.load(f)

# Load GeoJSON data if available
geojson_data = None
try:
    with open('data/districts.geojson', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
except FileNotFoundError:
    print("Warning: districts.geojson not found")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/districts')
def get_districts():
    return jsonify(districts)

@app.route('/api/districts/geojson')
def get_districts_geojson():
    if geojson_data is None:
        return jsonify({"error": "GeoJSON data not available"}), 404
    return jsonify(geojson_data)

@app.route('/data/mappings.csv')
def get_mappings():
    return send_from_directory('data', 'mappings.csv')

@app.route('/api/regions', methods=['POST'])
def save_regions():
    data = request.json
    # Save regions to a file
    with open('data/regions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 