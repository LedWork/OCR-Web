#!/usr/bin/env python3
"""
Simple script to download checked cards from the OCR Web API.
"""

import requests
import json
import os
import sys
from typing import Optional


def download_checked_cards(api_key: str, base_url: str = "http://localhost:5000") -> Optional[dict]:
    """
    Download checked cards from the retraining API endpoint.
    
    Args:
        api_key (str): The API key required for authentication
        base_url (str): The base URL of the API server
        
    Returns:
        Optional[dict]: The JSON response with checked cards, or None if failed
    """
    url = f"{base_url}/api/retraining/"
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"Making GET request to: {url}")
        response = requests.get(url, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Successfully downloaded checked cards")
            
            # Check if response has content
            if not response.content:
                print("⚠️  Response is empty")
                return []
            
            try:
                json_data = response.json()
                print(f"📊 Received data type: {type(json_data)}")
                if isinstance(json_data, list):
                    print(f"📊 Number of cards: {len(json_data)}")
                return json_data
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"Response content: {response.text[:200]}...")
                return None
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None


def save_to_file(data: dict, filename: str = "checked_cards.json") -> bool:
    """
    Save the downloaded data to a JSON file.
    
    Args:
        data (dict): The data to save
        filename (str): The filename to save to
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Data saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False


def main():
    """Main function to run the script."""
    # Get API key from environment variable or prompt user
    api_key = os.getenv('MODEL_API_KEY')
    
    if not api_key:
        print("⚠️  MODEL_API_KEY environment variable not set")
        api_key = input("Please enter your API key: ").strip()
        
        if not api_key:
            print("❌ No API key provided. Exiting.")
            sys.exit(1)
    
    # Get base URL from environment or use default
    base_url = os.getenv('API_BASE_URL', 'http://localhost:5000')
    
    print(f"🔗 Using API base URL: {base_url}")
    print(f"🔑 Using API key")
    
    # Download the data
    data = download_checked_cards(api_key, base_url)
    
    if data:
        # Save to file
        filename = "checked_cards.json"
        if save_to_file(data, filename):
            print(f"📊 Downloaded {len(data) if isinstance(data, list) else 'data'} items")
            print(f"💾 File saved as: {filename}")
        else:
            print("❌ Failed to save data to file")
    else:
        print("❌ Failed to download data")
        sys.exit(1)


if __name__ == "__main__":
    main() 
