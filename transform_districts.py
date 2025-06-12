import json
import csv
import re

def extract_belarusian_name(name):
    # Extract the Belarusian name from brackets and remove "бел." prefix
    match = re.search(r'\((.*?)\)', name)
    if match:
        bel_name = match.group(1)
        return re.sub(r'^бел\.\s*', '', bel_name)
    return ""

def clean_russian_name(name):
    # Remove the Belarusian part in parentheses and any extra whitespace
    return re.sub(r'\s*\([^)]*\)', '', name).strip()

def read_mappings(csv_file):
    mappings = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 4:  # We need at least 4 columns: name, code, admin_center, belarusian_name
                district_name = clean_russian_name(row[0])
                code = row[1].lower()  # Convert code to lowercase
                admin_center = row[2]
                belarusian_name = row[3]
                mappings[district_name] = {
                    'code': code,
                    'admin_center': admin_center,
                    'belarusian_name': belarusian_name
                }
    return mappings

def transform_districts(districts_file, mappings_file, output_file):
    # Read the mappings
    mappings = read_mappings(mappings_file)
    
    # Read the districts data
    with open(districts_file, 'r', encoding='utf-8') as f:
        districts = json.load(f)
    
    # Transform the districts
    transformed_districts = []
    for district in districts:
        district_name = clean_russian_name(district['name'])
        mapping = mappings.get(district_name, {})
        
        # Create the transformed district entry
        transformed_district = {
            'code': mapping.get('code', ''),
            'name': mapping.get('belarusian_name', ''),
            'name_ru': district_name,
            'name_be': extract_belarusian_name(district['name']),
            'region': district['region'],
            'square': district['square'],
            'population': district['population'],
            'bordering_districts': district['bordering_districts'],
            'administrative_center': mapping.get('admin_center', '')
        }
        transformed_districts.append(transformed_district)
    
    # Write the transformed data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_districts, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    transform_districts(
        'web/districts.json',
        'web/mappings.csv',
        'web/districts_transformed.json'
    ) 