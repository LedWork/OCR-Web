# OCR Web API - Card Downloader

A simple Python script to download checked cards from the OCR Web API.

## Features

- Downloads checked cards from the `/retraining/` endpoint
- Saves data to a JSON file
- Handles API authentication with API key
- Configurable base URL

## Setup

1. Install dependencies:
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

2. Set up your API key (one of these methods):
   - Set environment variable: `export MODEL_API_KEY="your_api_key_here"`
   - Or the script will prompt you to enter it when run

3. (Optional) Set custom API base URL:
   - Set environment variable: `export API_BASE_URL="http://your-server:5000"`
   - Default is `http://localhost:5000`

## Usage

Run the script:
```bash
python download_cards.py
```

The script will:
1. Download checked cards from the API
2. Save them to `checked_cards.json`
3. Display success/error messages
