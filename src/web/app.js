// Global variables
let selectedDistricts = new Set();
let regions = [];
let districtData = new Map(); // Map to store district codes and their data

// Load and inject SVG map
async function loadSVGMap() {
    try {
        const response = await fetch('/assets/beldist.svg');
        if (!response.ok) {
            console.error('Failed to load SVG:', response.status, response.statusText);
            document.getElementById('map').innerHTML = '<div style="color:red">SVG map failed to load</div>';
            return;
        }
        const svgText = await response.text();
        const mapDiv = document.getElementById('map');
        mapDiv.innerHTML = '';
        mapDiv.innerHTML = svgText;
        console.log('SVG injected successfully');
    } catch (e) {
        console.error('Error loading SVG:', e);
        document.getElementById('map').innerHTML = '<div style="color:red">SVG map failed to load</div>';
    }
}

// Load district data and mappings
async function loadDistricts() {
    try {
        // Load district data from JSON
        const response = await fetch('/api/districts');
        const districts = await response.json();
        
        // Load mappings from CSV
        const csvResponse = await fetch('/data/mappings.csv');
        const csvText = await csvResponse.text();
        
        // Parse CSV and create mapping
        const mappings = parseCSV(csvText);
        
        // Create mapping between district codes and data
        districts.forEach(district => {
            const mapping = mappings.find(m => m.name_en === district.name);
            if (mapping) {
                districtData.set(mapping.code.toLowerCase(), {
                    name: district.name,
                    square: district.square,
                    population: district.population
                });
            }
        });

        initializeMap();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Parse CSV data
function parseCSV(csvText) {
    const lines = csvText.split('\n');
    return lines.map(line => {
        const [name, code] = line.split(',').map(s => s.trim().replace(/"/g, ''));
        return { name, code };
    });
}

// Initialize the map
function initializeMap() {
    const svg = document.querySelector('svg');
    if (!svg) return;

    // Prefer data-district-id, fallback to id
    let districts = svg.querySelectorAll('[data-district-id]');
    if (districts.length === 0) {
        districts = svg.querySelectorAll('[id^="dist-"]');
    }
    districts.forEach(district => {
        let districtId = district.getAttribute('data-district-id');
        if (!districtId && district.id) {
            districtId = district.id.replace('dist-', '');
        }
        if (!districtId) return;
        districtId = districtId.toLowerCase();
        const data = districtData.get(districtId);
        if (data) {
            district.addEventListener('mouseover', (e) => {
                showTooltip(e, data);
            });
            district.addEventListener('mousemove', (e) => {
                moveTooltip(e);
            });
            district.addEventListener('mouseout', () => {
                hideTooltip();
            });
            district.addEventListener('click', () => {
                handleDistrictClick(district, data);
            });
        }
    });
    setupLayerControls();
}

// Show tooltip with district information
function showTooltip(event, data) {
    const tooltip = document.getElementById('tooltip');
    tooltip.innerHTML = `
        <strong>${data.name}</strong><br>
        Area: ${data.square} km²<br>
        Population: ${data.population.toLocaleString()}
    `;
    tooltip.style.display = 'block';
    moveTooltip(event);
}

// Move tooltip with mouse
function moveTooltip(event) {
    const tooltip = document.getElementById('tooltip');
    tooltip.style.left = (event.pageX + 10) + 'px';
    tooltip.style.top = (event.pageY + 10) + 'px';
}

// Hide tooltip
function hideTooltip() {
    const tooltip = document.getElementById('tooltip');
    tooltip.style.display = 'none';
}

// Handle district click
function handleDistrictClick(district, data) {
    const districtId = data.code;
    
    if (selectedDistricts.has(districtId)) {
        selectedDistricts.delete(districtId);
        district.classList.remove('selected');
    } else {
        selectedDistricts.add(districtId);
        district.classList.add('selected');
    }
    
    updateMap();
}

// Create new region from selected districts
function createNewRegion() {
    if (selectedDistricts.size === 0) return;
    
    const regionName = prompt('Enter region name:');
    if (!regionName) return;
    
    const regionDistricts = Array.from(selectedDistricts).map(code => districtData.get(code));
    const stats = calculateRegionStats(regionDistricts);
    
    regions.push({
        name: regionName,
        districts: Array.from(selectedDistricts),
        stats: stats
    });
    
    selectedDistricts.clear();
    updateMap();
    updateStats();
}

// Update map display
function updateMap() {
    const districts = document.querySelectorAll('[id^="dist-"]');
    districts.forEach(district => {
        const districtId = district.id.replace('dist-', '');
        district.classList.remove('selected');
        if (selectedDistricts.has(districtId)) {
            district.classList.add('selected');
        }
    });
}

// Calculate region statistics
function calculateRegionStats(districts) {
    return {
        totalArea: districts.reduce((sum, d) => sum + d.square, 0),
        totalPopulation: districts.reduce((sum, d) => sum + d.population, 0),
        districtCount: districts.length
    };
}

// Update statistics display
function updateStats() {
    const statsTable = document.getElementById('stats-table');
    statsTable.innerHTML = regions.map(region => `
        <tr>
            <td>${region.name}</td>
            <td>${region.stats.districtCount}</td>
            <td>${region.stats.totalArea.toLocaleString()} km²</td>
            <td>${region.stats.totalPopulation.toLocaleString()}</td>
            <td>
                <button onclick="deleteRegion('${region.name}')">Delete</button>
            </td>
        </tr>
    `).join('');
}

// Delete a region
function deleteRegion(regionName) {
    regions = regions.filter(r => r.name !== regionName);
    updateStats();
}

// Set up layer controls
function setupLayerControls() {
    const citiesCheckbox = document.getElementById('toggle-cities');
    const bordersCheckbox = document.getElementById('toggle-borders');
    if (citiesCheckbox) {
        citiesCheckbox.addEventListener('change', (e) => {
            const layer = document.querySelector('.cities-layer');
            if (layer) layer.style.display = e.target.checked ? '' : 'none';
        });
    }
    if (bordersCheckbox) {
        bordersCheckbox.addEventListener('change', (e) => {
            const layer = document.querySelector('.borders-layer');
            if (layer) layer.style.display = e.target.checked ? '' : 'none';
        });
    }
}

// Event listeners
document.getElementById('create-region').addEventListener('click', createNewRegion);
document.getElementById('save-regions').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/regions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(regions)
        });
        
        if (response.ok) {
            alert('Regions saved successfully!');
        } else {
            alert('Error saving regions');
        }
    } catch (error) {
        console.error('Error saving regions:', error);
        alert('Error saving regions');
    }
});

// Main loader
document.addEventListener('DOMContentLoaded', main);

async function main() {
    await loadSVGMap();
    try {
        await loadDistricts();
    } catch (e) {
        console.error('Error in loadDistricts:', e);
    }
} 