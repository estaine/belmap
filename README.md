# Belarus Districts Interactive Map

An interactive web application for visualizing and managing data about districts and district-like cities in Belarus. The project collects, processes, and displays comprehensive information including:
- Area (square kilometers)
- Population
- Administrative centers
- District boundaries (GeoJSON)
- Bordering districts and cities
- Regional groupings

## Features

- **Interactive Map**: Leaflet-based web interface for exploring district boundaries
- **Data Visualization**: SVG maps with district groupings and adjacency information
- **Regional Management**: Create and manage custom regional groupings
- **REST API**: Flask backend providing district data in multiple formats
- **Automated Data Collection**: Web scraping from Wikipedia sources

## Project Structure

```
belmap/
├── src/
│   ├── collectors/         # Data collection scripts
│   │   ├── collect_districts.py       # Scrape district data from Wikipedia
│   │   ├── fetch_district_boundaries.py  # Fetch GeoJSON boundaries
│   │   └── generate_geojson.py        # Generate GeoJSON data
│   ├── models/             # Data models (Pydantic)
│   │   └── district.py
│   ├── server/             # Flask web server
│   │   └── app.py
│   └── web/                # Frontend application
│       ├── index.html      # Interactive map interface
│       ├── app.js          # Frontend logic
│       ├── styles.css
│       └── assets/         # SVG maps and visualizations
├── data/                   # Processed data files
│   ├── districts.json      # District information
│   ├── district_boundaries.json  # Boundary coordinates
│   └── mappings.csv        # District code mappings
├── districts.json          # Main district data
├── district_adjacency.json # District neighbor information
└── requirements.txt        # Python dependencies
```

## Data Sources

The data is automatically collected from official Wikipedia pages for all regions of Belarus:
- [Brest Region](https://ru.wikipedia.org/wiki/Районы_Брестской_области)
- [Vitebsk Region](https://ru.wikipedia.org/wiki/Районы_Витебской_области)
- [Gomel Region](https://ru.wikipedia.org/wiki/Районы_Гомельской_области)
- [Grodno Region](https://ru.wikipedia.org/wiki/Районы_Гродненской_области)
- [Minsk Region](https://ru.wikipedia.org/wiki/Районы_Минской_области)
- [Mogilev Region](https://ru.wikipedia.org/wiki/Районы_Могилёвской_области)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd belmap
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Application

Start the Flask development server:
```bash
python src/server/app.py
```

The application will be available at `http://localhost:5000`

### Collecting District Data

Collect district information from Wikipedia:
```bash
python src/collectors/collect_districts.py
```

Fetch district boundaries (GeoJSON):
```bash
python src/collectors/fetch_district_boundaries.py
```

Generate GeoJSON for mapping:
```bash
python src/collectors/generate_geojson.py
```

### Extract Adjacency Information

Process district neighbor relationships:
```bash
python extract_adjacency.py
```

### Transform District Data

Convert and transform district data formats:
```bash
python transform_districts.py
```

## API Endpoints

- `GET /` - Main web interface
- `GET /api/districts` - Get all districts data
- `GET /api/districts/geojson` - Get districts in GeoJSON format
- `GET /data/mappings.csv` - Get district code mappings
- `POST /api/regions` - Save regional groupings

## Technologies Used

- **Backend**: Python 3.12, Flask
- **Data Processing**: BeautifulSoup4, Requests, Pydantic, NumPy, SciPy, Shapely
- **Frontend**: HTML5, JavaScript, Leaflet.js
- **Data Formats**: JSON, GeoJSON, CSV, SVG

## Output Files

- `districts.json` - Complete district database
- `district_adjacency.json` - District neighbor relationships
- `beldist.svg` - SVG visualization of districts
- `data/district_boundaries.json` - Geographic boundary data
- `data/regions.json` - Custom regional groupings

## License

This project is for educational and informational purposes.
