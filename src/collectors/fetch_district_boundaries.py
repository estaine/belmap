import requests
import json
from typing import Dict, List
import time

def fetch_district_boundaries(district_name: str, region: str) -> Dict:
    """Fetch district boundaries from OpenStreetMap using Overpass API."""
    # Construct the query
    query = f"""
    [out:json][timeout:25];
    area["name:en"="Belarus"]->.belarus;
    (
      relation["admin_level"="8"]["name:en"="{district_name}"](area.belarus);
      relation["admin_level"="8"]["name:ru"="{district_name}"](area.belarus);
      relation["admin_level"="8"]["name:be"="{district_name}"](area.belarus);
    );
    out body;
    >;
    out skel qt;
    """
    
    # Make the request to Overpass API
    response = requests.post(
        'https://overpass-api.de/api/interpreter',
        data=query
    )
    
    if response.status_code != 200:
        print(f"Error fetching data for {district_name}: {response.status_code}")
        return None
    
    data = response.json()
    
    # Process the response
    if not data.get('elements'):
        print(f"No data found for {district_name}")
        return None
    
    # Extract coordinates
    coordinates = []
    for element in data['elements']:
        if element['type'] == 'way':
            # Get the nodes for this way
            nodes = [n for n in data['elements'] if n['type'] == 'node' and n['id'] in element['nodes']]
            # Sort nodes according to the way's node order
            nodes.sort(key=lambda n: element['nodes'].index(n['id']))
            # Extract coordinates
            way_coords = [(n['lon'], n['lat']) for n in nodes]
            coordinates.append(way_coords)
    
    return {
        'name': district_name,
        'region': region,
        'coordinates': coordinates
    }

def main():
    # Load district data
    with open('data/districts.json', 'r', encoding='utf-8') as f:
        districts = json.load(f)
    
    # Fetch boundaries for each district
    boundaries = []
    for district in districts:
        print(f"Fetching boundaries for {district['name']}...")
        boundary = fetch_district_boundaries(district['name'], district['region'])
        if boundary:
            boundaries.append(boundary)
        # Be nice to the API
        time.sleep(1)
    
    # Save the boundaries
    with open('data/district_boundaries.json', 'w', encoding='utf-8') as f:
        json.dump(boundaries, f, ensure_ascii=False, indent=2)
    
    # Generate SVG
    generate_svg(boundaries)

def generate_svg(boundaries: List[Dict]):
    """Generate SVG map from district boundaries."""
    # Find the bounding box
    min_lon = min(min(min(lon for lon, lat in way) for way in district['coordinates']) for district in boundaries)
    max_lon = max(max(max(lon for lon, lat in way) for way in district['coordinates']) for district in boundaries)
    min_lat = min(min(min(lat for lon, lat in way) for way in district['coordinates']) for district in boundaries)
    max_lat = max(max(max(lat for lon, lat in way) for way in district['coordinates']) for district in boundaries)
    
    # Calculate the viewBox
    width = max_lon - min_lon
    height = max_lat - min_lat
    viewBox = f"{min_lon} {min_lat} {width} {height}"
    
    # Start SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewBox}">
    <style>
        .district {{
            fill: #e9ecef;
            stroke: #fff;
            stroke-width: 0.001;
            transition: fill 0.2s;
        }}
        .district:hover {{
            fill: #dee2e6;
            cursor: pointer;
        }}
        .district.selected {{
            fill: #007bff;
        }}
        .district.in-region {{
            fill: #28a745;
        }}
    </style>
"""
    
    # Add districts
    for district in boundaries:
        for way in district['coordinates']:
            points = ' '.join(f"{lon},{lat}" for lon, lat in way)
            svg += f'    <path class="district" data-district-id="{district["name"]}" d="M {points} Z" />\n'
    
    # Close SVG
    svg += '</svg>'
    
    # Save SVG
    with open('src/web/assets/map.svg', 'w', encoding='utf-8') as f:
        f.write(svg)

if __name__ == '__main__':
    main() 