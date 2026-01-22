# Vizro Dashboard Setup Guide

This guide will help you set up and run the Vizro call center analytics dashboard using the sample data provided in this repository.

## Prerequisites

- **Python 3.11** (required for compatibility with all dependencies)
- Git (to clone the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd demo-call-center
```

### 2. Install Python Dependencies

```bash
pip install pandas vizro pyarrow
```

**Required packages:**
- `pandas` - Data manipulation
- `vizro` - Dashboard framework
- `pyarrow` - Required for reading Parquet files

### 3. Prepare the Data

The repository includes sample data files in the `data/` directory. You need to:

#### a. Generate `data.csv`

Run the following Python script from the project root directory:

```bash
python3.11 scripts/prepare_vizro_data.py
```

This will create `vizro/data.csv` from the sample Parquet and JSON files.

#### b. Extract Transcript Files

Extract the conversation transcripts to the correct location:

```bash
mkdir -p outputs/anonymized_files
unzip data/en_conversations.zip -d outputs/anonymized_files/
```

### 4. Run the Dashboard

Navigate to the `vizro` directory and start the application:

```bash
cd vizro
python3.11 app.py
```

The dashboard will start on **http://127.0.0.1:8050/**

## Using the Dashboard

The dashboard has two main pages:

### 1. Call Center Summary
- View KPIs (upsale success, concerns addressed, call volume)
- Interactive charts showing call patterns over time
- Quality scores and communication metrics
- Geographic distribution of calls
- Filter by Agent ID, Caller ID, Client Tone, Communication Score, and Caller City

### 2. Call Transcripts
- Browse call records in a table
- Click any row to view the full conversation transcript
- Filter by Agent ID and Caller ID

## Troubleshooting

### Issue: Module not found errors
**Solution:** Ensure you're using Python 3.11 and all dependencies are installed:
```bash
pip install --upgrade pandas vizro pyarrow
```

### Issue: "data.csv not found" error
**Solution:** Make sure you ran the data preparation script from step 3a above.

### Issue: Transcripts not displaying when clicking rows
**Solution:** Verify that transcript files were extracted:
```bash
ls outputs/anonymized_files/
```
You should see 10 `.txt` files. If not, re-run step 3b.

### Issue: FutureWarning messages
**Solution:** These are deprecation warnings and don't affect functionality. They can be safely ignored.

## Project Structure

```
demo-call-center/
├── data/                          # Sample data files
│   ├── en_conversations.zip       # Transcript texts
│   ├── en_metadata.parquet        # Call metadata
│   ├── en_ground_truths.parquet   # Quality scores
│   ├── en_dataframe.parquet       # File references
│   └── en_clients.json            # Client information
├── outputs/
│   └── anonymized_files/          # Extracted transcripts
├── vizro/
│   ├── app.py                     # Main dashboard application
│   ├── custom_components.py       # Custom Vizro components
│   ├── custom_charts.py           # Custom chart functions
│   ├── data.csv                   # Generated data file
│   └── README.md                  # This file
└── scripts/
    └── prepare_vizro_data.py      # Data preparation script
```

## Notes

- The sample data includes 10 English call center conversations
- Audio files are not included in the sample data, so the audio player will not function
- The dashboard uses development mode and should not be used in production without proper deployment configuration
