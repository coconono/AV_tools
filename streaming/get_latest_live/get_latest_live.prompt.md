# YouTube Latest Live Stream Checker

## Overview
Create a tool to check a YouTube channel for the latest scheduled live stream and return its details.

## Files to Create

### 1. get_latest_live.py
A Python script that:
- Checks a specified YouTube channel for the latest scheduled live stream
- Returns the title and URL of the stream if found
- Returns a message indicating no scheduled streams if none exist
- Uses the YouTube Data API v3

**Requirements:**
- Create a `requirements.txt` with necessary dependencies (google-api-python-client, python-dotenv, etc.)
- Support API key configuration via environment variables or config file
- Handle errors gracefully (API errors, network issues, invalid channel)
- Format output clearly (JSON or plain text)

### 2. get_latest_live.sh
A shell script that:
- Activates the virtual environment (creates if it doesn't exist)
- Checks if dependencies are installed
- Installs dependencies from `requirements.txt` if needed
- Runs the `get_latest_live.py` script
- Deactivates the virtual environment on completion
- Handles errors at each step

### 3. .gitignore
Update to exclude:
- Virtual environment folder (`venv/`, `env/`, `.venv/`)
- Python cache files (`__pycache__/`, `*.pyc`)
- Environment configuration files (`.env`)
- IDE/editor files (`.vscode/`, `.idea/`)

### 4 README.md
Add a section with:
- Instructions on setting up the environment and running the scripts
- Example usage
- Configuration details for API keys and channel settings 

### 5. config.yaml.example
A sample configuration file that:
- Shows how to set the YouTube API key
- Allows users to specify the channel ID or username to check for live streams

## Configuration
- Store YouTube API key securely (environment variable or `.env` file)
- Make channel ID/username configurable