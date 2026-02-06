#!/bin/bash
# Wrapper script to run the PDF parser with the correct virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ Error: Virtual environment not found."
    echo "Please run setup first with Python 3.12:"
    echo "  /opt/homebrew/bin/python3.12 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and run the script
source "$SCRIPT_DIR/venv/bin/activate"
python "$SCRIPT_DIR/parse_pdf.py" "$@"
