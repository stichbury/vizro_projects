#!/usr/bin/env python3.11
"""
Prepare data.csv for the Vizro dashboard from sample data files.

This script reads the sample Parquet and JSON files from the data/ directory
and creates a consolidated data.csv file that the Vizro dashboard can use.
"""

import os
import json
import sqlite3
import pandas as pd
from pathlib import Path

# Define column mapping (from src/vizro.py)
COLUMNS_MAPPING = {
    "active_listening": "Active Listening",
    "agent_id": "Agent ID",
    "agent_tone": "Agent Tone",
    "date": "Call Date",
    "client_id": "Caller ID",
    "client_tone": "Client Tone",
    "concern_addressed": "Concern Addressed",
    "customization": "Customization",
    "effective_communication": "Effective Communication",
    "empathy": "Empathy",
    "kindness": "Kindness",
    "professionalism": "Professionalism",
    "summary": "Summary",
    "time": "Time",
    "topic": "Topic",
    "agent_tries_upsale": "Upsale Attempted",
    "agent_succeeds_upsale": "Upsale Success",
    "client_city": "Caller City",
}


def main():
    """Create vizro/data.csv from sample data files."""
    
    # Get script directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_dir = project_root / "data"
    vizro_dir = project_root / "vizro"
    
    print("Preparing Vizro data from sample files...")
    print(f"Project root: {project_root}")
    print(f"Data directory: {data_dir}")
    
    # Check if data directory exists
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    # Load the parquet files
    print("\nLoading data files...")
    metadata_df = pd.read_parquet(data_dir / "en_metadata.parquet")
    print(f"  ✓ Loaded metadata: {len(metadata_df)} rows")
    
    ground_truths_df = pd.read_parquet(data_dir / "en_ground_truths.parquet")
    print(f"  ✓ Loaded ground truths: {len(ground_truths_df)} rows")
    
    dataframe_df = pd.read_parquet(data_dir / "en_dataframe.parquet")
    print(f"  ✓ Loaded dataframe: {len(dataframe_df)} rows")
    
    # Load clients data from SQLite database (which has location data)
    # The JSON file doesn't include latitude/longitude
    db_path = data_dir / "sqlite.db"
    if not db_path.exists():
        raise FileNotFoundError(f"SQLite database not found: {db_path}")
    
    conn = sqlite3.connect(db_path)
    clients_df = pd.read_sql("SELECT * FROM client", conn)
    conn.close()
    
    # If database is empty, load from JSON and add placeholder location data
    if len(clients_df) == 0:
        print("  ⚠ Database is empty, loading from JSON and adding mock location data...")
        with open(data_dir / "en_clients.json", "r") as f:
            clients_data = json.load(f)
        clients_df = pd.DataFrame(clients_data)
        
        # Add mock location data based on common US cities
        mock_cities = [
            ("Phoenix, AZ", 33.4484, -112.0740),
            ("Dallas, TX", 32.7767, -96.7970),
            ("Houston, TX", 29.7604, -95.3698),
            ("San Antonio, TX", 29.4241, -98.4936),
            ("Philadelphia, PA", 39.9526, -75.1652),
            ("San Diego, CA", 32.7157, -117.1611),
            ("Austin, TX", 30.2672, -97.7431),
            ("San Jose, CA", 37.3382, -121.8863),
            ("Fort Worth, TX", 32.7555, -97.3308),
            ("Columbus, OH", 39.9612, -82.9988),
        ]
        clients_df["client_city"] = [city[0] for city in mock_cities[:len(clients_df)]]
        clients_df["latitude"] = [city[1] for city in mock_cities[:len(clients_df)]]
        clients_df["longitude"] = [city[2] for city in mock_cities[:len(clients_df)]]
    
    print(f"  ✓ Loaded clients: {len(clients_df)} rows")
    
    # Merge the data
    print("\nMerging data...")
    
    # Drop duplicate columns from ground_truths before merging
    ground_truths_df = ground_truths_df.drop(columns=["client_id", "agent_id"])
    
    # Merge metadata and ground truths on call_id
    merged_df = pd.merge(metadata_df, ground_truths_df, on="call_id", how="left")
    print(f"  ✓ Merged metadata and ground truths: {len(merged_df)} rows")
    
    # Merge with dataframe_df for audio_file and text_file
    merged_df = pd.merge(merged_df, dataframe_df, on="text_file", how="left")
    print(f"  ✓ Merged with file references: {len(merged_df)} rows")
    
    # Merge with clients_df for location data
    merged_df = pd.merge(
        merged_df,
        clients_df[["client_id", "client_city", "latitude", "longitude"]],
        on="client_id",
        how="left",
    )
    print(f"  ✓ Merged with client data: {len(merged_df)} rows")
    
    # Rename columns using mapping
    vizro_df = merged_df.rename(columns=COLUMNS_MAPPING)
    
    # Ensure Summary column exists
    if "Summary" not in vizro_df.columns:
        vizro_df["Summary"] = ""
    
    # Create vizro directory if it doesn't exist
    vizro_dir.mkdir(exist_ok=True)
    
    # Save to CSV
    output_path = vizro_dir / "data.csv"
    vizro_df.to_csv(output_path, index=False)
    
    print(f"\n✅ Successfully created {output_path}")
    print(f"   Rows: {len(vizro_df)}")
    print(f"   Columns: {len(vizro_df.columns)}")
    print(f"\nColumns included:")
    for col in sorted(vizro_df.columns):
        print(f"   - {col}")
    
    # Verify required columns for transcripts
    required_cols = ["Agent ID", "Caller ID", "Topic", "Summary", "text_file", "audio_file"]
    missing_cols = [col for col in required_cols if col not in vizro_df.columns]
    
    if not missing_cols:
        print("\n✅ All required columns present for transcript display!")
    else:
        print(f"\n⚠️  Warning: Missing columns: {missing_cols}")


if __name__ == "__main__":
    main()
