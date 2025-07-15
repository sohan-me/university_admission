#!/bin/bash

# Set the name of the virtual environment directory
VENV_DIR="venv"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Please install Python3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found!"
    exit 1
fi

# Run the FastAPI app
echo "Starting FastAPI app..."
uvicorn main:app --reload
