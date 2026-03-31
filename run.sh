#!/bin/bash
# This script provides a standardized way to run the ARMS daily cycle.

# Get the absolute path to the directory containing this script (the project root).
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SRC_DIR="$SCRIPT_DIR/src"

echo "Starting Achelion ARMS Main Cycle from within src..."

# Change into the src directory and run the main script directly.
# This simplifies Python's import path.
cd "$SRC_DIR" || exit
python3 main.py

echo "Achelion ARMS Main Cycle Finished."
