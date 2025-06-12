import json
import os
from typing import Dict, List, Tuple

def create_district_geojson(districts: List[Dict]) -> Dict:
    """Create GeoJSON data for districts."""
    features = []
    
    for district in districts:
        # Create a simple polygon for each district
        # In a real implementation, you would use actual geographic coordinates
        # This is just a placeholder that creates a small square for each district
        coordinates = generate_district_coordinates(district)
        
        feature = {
            "type": "Feature",
            "properties": {
                "id": district["id"],
                "name": district["name"],
                "name_ru": district["name_ru"],
                "name_be": district["name_be"],
                "region": district["region"],
                "square": district["square"],
                "population": district["population"],
                "is_city": district["is_city"],
                "administrative_center": district["administrative_center"]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

def generate_district_coordinates(district: Dict) -> List[Tuple[float, float]]:
    """Generate placeholder coordinates for a district.
    In a real implementation, you would use actual geographic coordinates."""
    # This is just a placeholder that creates a small square
    # The actual coordinates should be replaced with real district boundaries
    base_lat = 53.7098  # Center of Belarus
    base_lon = 27.9534
    
    # Create a small square around the base point
    size = 0.1  # Size of the square in degrees
    return [
        (base_lon - size, base_lat - size),
        (base_lon + size, base_lat - size),
        (base_lon + size, base_lat + size),
        (base_lon - size, base_lat + size),
        (base_lon - size, base_lat - size)  # Close the polygon
    ]

def main():
    # Load district data
    with open('data/districts.json', 'r', encoding='utf-8') as f:
        districts = json.load(f)
    
    # Generate GeoJSON
    geojson_data = create_district_geojson(districts)
    
    # Save GeoJSON data
    with open('data/districts.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main() 