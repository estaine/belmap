# Migration to Client-Based Architecture

## Summary

This document describes the migration from a server-dependent application to a **fully client-based** architecture. The game and regional management tool now run entirely in the browser with no database or server requirements.

## Changes Made

### 1. Main Game (`/web/index.html`)

**Removed:**
- Airtable API integration
- Personal Access Token (PAT) exposure
- All external database calls

**Added:**
- Stub leaderboard data (20 sample entries)
- Local data processing for leaderboards
- Simulated async loading (300ms delay)

**Changes:**
- `STUB_LEADERBOARD`: Array of 20 sample scores with Belarusian names
- `submitScoreToAirtable()`: Now a stub that logs to console
- `fetchLeaderboardAndShow()`: Uses local stub data
- `fetchTop20Leaderboard()`: Uses local stub data

### 2. Regional Management Tool (`/src/web/`)

**Modified Files:**
- `app.js`: Changed from API calls to local file loading
- `index.html`: Updated button IDs to match JavaScript

**Data Files Copied:**
- `districts.json` (from root)
- `mappings.csv` (from root)

**Changes:**
- District data loading: `/api/districts` → `districts.json`
- Mappings loading: `/data/mappings.csv` → `mappings.csv`
- Save functionality: POST to `/api/regions` → localStorage

**New Storage:**
- Regions saved to: `localStorage['belmap-regions']`

### 3. Documentation Updates

**README.md:**
- Updated project description to highlight client-based architecture
- Reorganized project structure section
- Added clear usage instructions for both applications
- Marked Flask server as optional (for data collection only)
- Added "Game Architecture" section

**New Files:**
- `/src/web/README.md`: Detailed guide for regional management tool

## What Still Works

✅ **Game Features:**
- All 20 rounds of gameplay
- Scoring system
- Timer and attempts tracking
- Distance-based hints
- Game over screen
- Leaderboard UI (with stub data)

✅ **Regional Management:**
- District selection
- Region creation
- Statistics calculation
- Local storage persistence

✅ **Data Collection (Optional):**
- Flask server still available for data scraping
- Collector scripts unchanged

## What Was Removed

❌ **Database Features:**
- Airtable integration
- Online leaderboard synchronization
- Cross-device score sharing
- Real-time leaderboard updates

## Migration Benefits

1. **Security**: No exposed API keys or tokens
2. **Privacy**: No data sent to external services
3. **Performance**: Faster load times (no API latency)
4. **Reliability**: No dependency on external services
5. **Portability**: Can be hosted anywhere (GitHub Pages, local file system)
6. **Offline**: Works without internet connection (after initial load)

## Future Implementation Notes

The leaderboard stub can be replaced with:
- **localStorage**: Local browser storage (per-device)
- **Firebase**: Free tier with authentication
- **Supabase**: Open-source alternative
- **Custom backend**: Your own API server
- **IndexedDB**: Advanced browser storage

## Testing

To test the changes:

```bash
# Test the game
cd web
python3 -m http.server 8000
# Visit http://localhost:8000

# Test the regional management tool
cd src/web
python3 -m http.server 8001
# Visit http://localhost:8001
```

## Files Modified

1. `/web/index.html` - Removed Airtable integration, added stubs
2. `/src/web/app.js` - Changed to local file loading
3. `/src/web/index.html` - Fixed button IDs
4. `/README.md` - Updated documentation
5. `/src/web/README.md` - New file

## Files Added

1. `/src/web/districts.json` - Copied from root
2. `/src/web/mappings.csv` - Copied from root
3. `/src/web/README.md` - New documentation

## No Changes Required

- `/groupings/index.html` - Already client-based
- All data collection scripts
- Flask server (still available if needed)
- Python dependencies

