#!/bin/sh

# Example Shell script for running the app

# Exit the script if an error occurs
set -e

# Fetch & pull from GitHub to run the latest version
git fetch
git pull

# Change the working directory
cd /home/pi/radio-stream-recorder

# Create a virtual Python envoriment, if it doesn't already exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  source .venv/bin/activate
fi

# Install the required packages
./.venv/bin/pip3 install -r requirements.txt

# Execute the main Python script (the -u switch is important for logging)
./.venv/bin/python3 -u src/radio_stream_recorder/main.py --config-file configuration.properties
