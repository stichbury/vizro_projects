#!/bin/bash
# Automated setup script for Vizro Dashboard
# This script prepares all necessary data and dependencies

set -e  # Exit on error

echo "==================================="
echo "Vizro Dashboard Setup"
echo "==================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_CMD="python3.11"

if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Error: Python 3.11 not found"
    echo "Please install Python 3.11 and try again"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Get script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

# Install dependencies
echo "Installing Python dependencies..."
$PYTHON_CMD -m pip install -q pandas vizro pyarrow
echo "✓ Dependencies installed"
echo ""

# Prepare data
echo "Preparing dashboard data..."
$PYTHON_CMD scripts/prepare_vizro_data.py
echo ""

# Extract transcripts
echo "Extracting conversation transcripts..."
mkdir -p outputs/anonymized_files
if [ -f "data/en_conversations.zip" ]; then
    unzip -q -o data/en_conversations.zip -d outputs/anonymized_files/
    echo "✓ Extracted $(ls -1 outputs/anonymized_files/*.txt 2>/dev/null | wc -l) transcript files"
else
    echo "⚠ Warning: data/en_conversations.zip not found"
fi
echo ""

echo "==================================="
echo "✅ Setup Complete!"
echo "==================================="
echo ""
echo "To start the dashboard:"
echo "  cd vizro"
echo "  python3.11 app.py"
echo ""
echo "Then open your browser to:"
echo "  http://127.0.0.1:8050/"
echo ""
