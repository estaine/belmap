# Belarus Districts Interactive Map & Game

An interactive web application for visualizing and managing data about districts and district-like cities in Belarus. The project includes both a data management system and a **fully client-based educational game** that tests knowledge of Belarusian geography.

The project collects, processes, and displays comprehensive information including:
- Area (square kilometers)
- Population
- Administrative centers
- District boundaries (GeoJSON)
- Bordering districts and cities
- Regional groupings

## Features

- **Client-Based Game**: Fully browser-based game with no server requirements (`/web/index.html`)
- **Interactive Map**: SVG maps with district groupings and adjacency information
- **Stub Leaderboard**: Local leaderboard with placeholder data (no database required)
- **Data Visualization**: Multiple map formats and visualizations
- **Regional Management**: Create and manage custom regional groupings
- **REST API** (optional): Flask backend for data management and collection
- **Automated Data Collection**: Web scraping from Wikipedia sources

## Project Structure

```
belmap/
├── web/                    # 🎮 Main Game (Client-based)
│   ├── index.html          # Educational geography game
│   ├── districts_transformed.json
│   ├── district_adjacency.json
│   ├── mappings.csv
│   └── beldist.svg
├── src/
│   ├── web/                # 🗺️ Regional Management Tool (Client-based)
│   │   ├── index.html      # Interactive map interface
│   │   ├── app.js          # Frontend logic
│   │   ├── districts.json
│   │   ├── mappings.csv
│   │   └── assets/         # SVG maps
│   ├── collectors/         # Data collection scripts
│   │   ├── collect_districts.py       # Scrape district data from Wikipedia
│   │   ├── fetch_district_boundaries.py  # Fetch GeoJSON boundaries
│   │   └── generate_geojson.py        # Generate GeoJSON data
│   ├── models/             # Data models (Pydantic)
│   │   └── district.py
│   └── server/             # Flask web server (optional)
│       └── app.py
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

### Option 1: Educational Geography Game (Recommended)

The main game is located in `/web/` and is fully client-based:

```bash
cd web
python3 -m http.server 8000
# Visit http://localhost:8000
```

Features:
- 20 rounds of district identification
- Scoring system with time penalties
- Distance-based hints (color-coded)
- Stub leaderboard (no database)

### Option 2: Regional Management Tool

A tool for creating custom regional groupings in `/src/web/`:

```bash
cd src/web
python3 -m http.server 8001
# Visit http://localhost:8001
```

Features:
- Interactive district selection
- Create custom regions
- View statistics (area, population)
- Save to localStorage

### Option 3: Flask Development Server (Optional - For Data Collection)

Only needed if you want to collect new data or use the legacy API:

```bash
python src/server/app.py
# Visit http://localhost:5000
```

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

## Game Architecture

The game in `/web/index.html` is **fully client-based** with no server or database dependencies:
- All district data is loaded from static JSON files
- Game logic runs entirely in the browser
- Leaderboard uses stub data (placeholder for future implementation)
- No external API calls or database connections

## API Endpoints (Flask Server - Optional)

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
