# Belarus Districts Map - Regional Management Tool

This is a **client-based** regional management tool that allows you to create and manage custom groupings of Belarusian districts.

## Features

- Interactive SVG map of Belarus districts
- Click districts to select them
- Create custom regional groupings
- View statistics for each region (area, population, district count)
- Save regions to browser localStorage (no server required)

## Usage

No server required! Simply open `index.html` in your browser:

```bash
# Option 1: Direct file open
# Just double-click index.html or open it in your browser

# Option 2: Use a simple HTTP server (recommended)
python3 -m http.server 8000
# Then visit http://localhost:8000
```

## Data Sources

- `districts.json` - District information (area, population, names)
- `mappings.csv` - District code mappings
- `assets/beldist.svg` - SVG map of Belarus districts

## Storage

Regions are saved to browser localStorage (key: `belmap-regions`). No database or server required.

