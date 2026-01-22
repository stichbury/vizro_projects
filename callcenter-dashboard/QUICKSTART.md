# Vizro Dashboard - Quick Start Guide

Get the call center analytics dashboard running in 3 simple steps!

## Prerequisites

- Python 3.11 installed on your system
- Git (to clone the repository)

## Installation

### Step 1: Clone and Setup

```bash
git clone <repository-url>
cd demo-call-center
pip install pandas vizro pyarrow
```

### Step 2: Prepare Data

```bash
python3.11 scripts/prepare_vizro_data.py
mkdir -p outputs/anonymized_files
unzip data/en_conversations.zip -d outputs/anonymized_files/
```

### Step 3: Run Dashboard

```bash
cd vizro
python3.11 app.py
```

Open your browser to **http://127.0.0.1:8050/**

## What You'll See

### 📊 Call Center Summary Page
- Key performance indicators (KPIs)
- Call volume trends over time
- Quality scores and communication metrics
- Geographic distribution of calls
- Interactive filters for deep analysis

### 📝 Call Transcripts Page
- Table of all call records
- Click any row to view full conversation transcript
- Filter by agent or caller

## Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'vizro'`  
**Solution:** Install dependencies: `pip install pandas vizro pyarrow`

**Issue:** "data.csv not found"  
**Solution:** Run: `python3.11 scripts/prepare_vizro_data.py`

**Issue:** Transcripts not showing  
**Solution:** Extract transcripts: `unzip data/en_conversations.zip -d outputs/anonymized_files/`

## More Information

- Full documentation: See `vizro/README.md`
- Technical changes: See `CHANGES.md`
- Sample data: 10 English call center conversations in `data/` folder

---

**Note:** The dashboard runs in development mode. For production use, please configure a proper WSGI server.
