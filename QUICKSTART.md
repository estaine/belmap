# Quick Start Guide

## 🎮 Play the Game

The easiest way to start:

```bash
cd /home/estaine/IdeaProjects/belmap/web
python3 -m http.server 8000
```

Then open your browser and visit: **http://localhost:8000**

That's it! The game is fully functional with:
- ✅ All district data loaded locally
- ✅ Full gameplay (20 rounds)
- ✅ Scoring system
- ✅ Stub leaderboard (sample data)

## 🗺️ Use the Regional Management Tool

```bash
cd /home/estaine/IdeaProjects/belmap/src/web
python3 -m http.server 8001
```

Visit: **http://localhost:8001**

Features:
- ✅ Click districts to select them
- ✅ Create custom regions
- ✅ View statistics
- ✅ Save to browser storage

## What Changed?

- ❌ **Removed**: Airtable database integration
- ✅ **Added**: Stub leaderboard with sample data
- ✅ **Added**: localStorage for regional management
- ✅ **Result**: No server or database needed!

## Leaderboard Stub

The leaderboard shows sample data:
- 20 sample scores from 1850 to 720 points
- Sample Belarusian names
- Top-10 shown in game over screen
- Top-20 shown in side panel

**Note**: Score submission is stubbed (logs to console only)

## Need to Restore Database?

See `/home/estaine/IdeaProjects/belmap/MIGRATION_SUMMARY.md` for details on implementing a real leaderboard with:
- Firebase
- Supabase
- Custom backend
- LocalStorage persistence

## Questions?

All changes are documented in `MIGRATION_SUMMARY.md`

