#!/bin/bash

echo "=============================================="
echo " Bilingual Stroop Experiment - Setup & Run"
echo "=============================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed! Please install Python 3.9+."
    exit 1
fi

echo "Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

echo "Activating virtual environment and installing dependencies..."
source .venv/bin/activate
pip install -r requirements.txt

echo ""
echo "Launching the experiment..."
echo ""
python run_experiment.py
