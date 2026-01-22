# Vizro Call Center Analytics Dashboard

An interactive analytics dashboard for call center data visualization, built with [Vizro](https://vizro.readthedocs.io/).

![Python 3.11](https://img.shields.io/badge/python-3.11-blue)
![Vizro](https://img.shields.io/badge/vizro-latest-green)

## Features

- 📊 **Call Center Summary** - KPIs, trends, quality metrics, geographic distribution
- 📝 **Call Transcripts** - Browse and read full conversation transcripts
- 🔍 **Interactive Filters** - Drill down by agent, caller, tone, city, and more
- 📈 **Custom Visualizations** - Donut charts, radar plots, butterfly charts, maps

## Quick Start

```bash
pip install -r requirements.txt
bash scripts/setup_dashboard.sh
cd vizro
python3.11 app.py
```

Open your browser to **http://127.0.0.1:8050/**

## Requirements

- **Python 3.11** (required for compatibility)
- Dependencies: `pandas`, `vizro`, `pyarrow`

## Installation Steps

### Option 1: Automated Setup (Recommended)

```bash
git clone <repository-url>
cd vizro-call-center-dashboard
bash scripts/setup_dashboard.sh
cd vizro
python3.11 app.py
```

### Option 2: Manual Setup

```bash
git clone <repository-url>
cd vizro-call-center-dashboard

# Install dependencies
pip install -r requirements.txt

# Prepare data
python3.11 scripts/prepare_vizro_data.py

# Extract transcripts
mkdir -p outputs/anonymized_files
unzip data/en_conversations.zip -d outputs/anonymized_files/

# Run dashboard
cd vizro
python3.11 app.py
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 3 steps
- **[vizro/README.md](vizro/README.md)** - Detailed setup and usage guide


## Sample Data

The project includes **10 English call center conversations** with:

- ✅ Call metadata (dates, times, IDs)
- ✅ Quality scores and metrics
- ✅ Geographic distribution (US cities)
- ✅ Agent performance data
- ✅ Full conversation transcripts
- ⚠️ Audio files not included (optional feature)

## Dashboard Pages

### 1. Call Center Summary

View comprehensive analytics:
- **KPIs**: Upsale success rate, concerns addressed, total calls
- **Trends**: Call volume over time
- **Quality Metrics**: Communication scores by agent
- **Geographic Map**: Call distribution across US cities
- **Filters**: Agent ID, Caller ID, Client Tone, Communication Score, Caller City

### 2. Call Transcripts

Interactive transcript viewer:
- Browse all call records in a searchable table
- Click any row to view full conversation transcript
- Filter by Agent ID and Caller ID
- Formatted with speaker labels and timestamps

## Project Structure

```
vizro-call-center-dashboard/
├── README.md                  # This file
├── QUICKSTART.md             # Quick start guide
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
│
├── data/                    # Sample data files
│   ├── en_metadata.parquet
│   ├── en_ground_truths.parquet
│   ├── en_dataframe.parquet
│   ├── en_clients.json
│   ├── sqlite.db
│   └── en_conversations.zip
│
├── scripts/                 # Automation scripts
│   ├── prepare_vizro_data.py
│   └── setup_dashboard.sh
│
├── vizro/                   # Dashboard application
│   ├── README.md
│   ├── app.py
│   ├── custom_components.py
│   ├── custom_charts.py
│   └── assets/
│       └── vizro_dashboard_styles.css
│
└── outputs/                 # Generated files
    └── anonymized_files/    # Extracted transcripts
```

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'vizro'`  
**Solution:** Install dependencies: `pip install -r requirements.txt`

**Issue:** `FileNotFoundError: data.csv not found`  
**Solution:** Run data preparation: `python3.11 scripts/prepare_vizro_data.py`

**Issue:** Transcripts not displaying  
**Solution:** Extract transcripts: `unzip data/en_conversations.zip -d outputs/anonymized_files/`

**Issue:** Python version mismatch  
**Solution:** Ensure Python 3.11 is installed and active: `python3.11 --version`

### Get Help

- Check [vizro/README.md](vizro/README.md) for detailed troubleshooting
- Review [CHANGES.md](CHANGES.md) for technical implementation details
- Ensure all setup steps completed successfully

## Development

This dashboard uses:
- **Vizro** - Dashboard framework
- **Plotly** - Interactive charts
- **Pandas** - Data manipulation
- **Dash AG Grid** - Interactive tables


## Acknowledgments

Based on an example for [MLRun](https://github.com/mlrun/demo-call-center).
