import json
import os
import sys
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import re

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.district import District

class DistrictCollector:
    def __init__(self):
        self.regions = {
            "Брестской": {
                "name_en": "Brest",
                "url": "https://ru.wikipedia.org/wiki/Районы_Брестской_области"
            },
            "Витебской": {
                "name_en": "Vitebsk",
                "url": "https://ru.wikipedia.org/wiki/Районы_Витебской_области"
            },
            "Гомельской": {
                "name_en": "Gomel",
                "url": "https://ru.wikipedia.org/wiki/Районы_Гомельской_области"
            },
            "Гродненской": {
                "name_en": "Grodno",
                "url": "https://ru.wikipedia.org/wiki/Районы_Гродненской_области"
            },
            "Минской": {
                "name_en": "Minsk",
                "url": "https://ru.wikipedia.org/wiki/Районы_Минской_области"
            },
            "Могилёвской": {
                "name_en": "Mogilev",
                "url": "https://ru.wikipedia.org/wiki/Районы_Могилёвской_области"
            }
        }
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(self.data_dir, exist_ok=True)

    def clean_number(self, value: str, is_float: bool = False):
        # Remove arrows, spaces, and non-numeric characters except dot and comma
        value = re.sub(r'[↗↘↑↓\s]', '', value)
        value = value.replace(',', '.')
        value = re.sub(r'[^\d\.]', '', value)
        if is_float:
            try:
                return float(value)
            except ValueError:
                return None
        else:
            try:
                return int(float(value))
            except ValueError:
                return None

    def collect_region_data(self, region_name: str) -> List[District]:
        """Collect data for a specific region."""
        url = self.regions[region_name]["url"]
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        districts = []
        
        # Find the main table with district data
        table = soup.find('table', {'class': 'wikitable'})
        if not table:
            raise ValueError(f"Could not find district table for {region_name}")
            
        for row in table.find_all('tr')[1:]:  # Skip header row
            cols = row.find_all(['td', 'th'])
            if len(cols) < 5:  # Skip rows without enough data
                continue
                
            try:
                # Extract data from columns
                name_ru = cols[1].get_text(strip=True)
                name_be = cols[1].find('a').get_text(strip=True) if cols[1].find('a') else name_ru
                square = self.clean_number(cols[4].get_text(strip=True), is_float=True)
                population = self.clean_number(cols[5].get_text(strip=True), is_float=False)
                if square is None or population is None:
                    continue
                # Extract administrative center (now from the fourth column)
                admin_center = cols[3].get_text(strip=True) if len(cols) > 3 else None
                # Create district object
                district = District(
                    name=name_ru,  # Using Russian name as default
                    name_ru=name_ru,
                    name_be=name_be,
                    region=self.regions[region_name]["name_en"],
                    square=square,
                    population=population,
                    bordering_districts=[],  # To be filled from separate pages
                    is_city="город" in name_ru.lower(),
                    administrative_center=admin_center
                )
                districts.append(district)
            except (ValueError, AttributeError) as e:
                print(f"Error processing row: {e}")
                continue
                
        return districts

    def collect_all_data(self):
        """Collect data for all regions."""
        all_districts = []
        
        for region_name in self.regions:
            try:
                print(f"Collecting data for {region_name} region...")
                districts = self.collect_region_data(region_name)
                all_districts.extend(districts)
            except Exception as e:
                print(f"Error collecting data for {region_name}: {e}")
                
        # Save to JSON file
        output_file = os.path.join(self.data_dir, "districts.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump([d.dict() for d in all_districts], f, ensure_ascii=False, indent=2)
            
        print(f"Data saved to {output_file}")

if __name__ == "__main__":
    collector = DistrictCollector()
    collector.collect_all_data() 