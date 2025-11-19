#!/usr/bin/env python3
"""
Test script to verify the profile picture upload endpoint with a real image
"""

import requests
import os
from pathlib import Path

def test_upload_with_real_image():
    print("🧪 Testing profile picture upload endpoint with real image...")
    
    # Backend URL
    base_url = "https://forti-app.onrender.com"
    upload_url = f"{base_url}/api/v1/accounts/files/profile-picture"
    
    # Check if we have any existing images in the seed_assets folder
    seed_assets_path = Path("seed_assets/profiles")
    if seed_assets_path.exists():
        image_files = list(seed_assets_path.glob("*.jpg")) + list(seed_assets_path.glob("*.jpeg")) + list(seed_assets_path.glob("*.png"))
        if image_files:
            test_image_path = str(image_files[0])
            print(f"✅ Using existing image: {test_image_path}")
        else:
            print("❌ No images found in seed_assets/profiles")
            return False
    else:
        print("❌ seed_assets/profiles folder not found")
        return False
    
    try:
        # Test the upload endpoint
        print(f"🌐 Testing upload to: {upload_url}")
        
        with open(test_image_path, 'rb') as f:
            files = {'file': (os.path.basename(test_image_path), f, 'image/jpeg')}
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'Test-Upload/1.0'
            }
            
            response = requests.post(upload_url, files=files, headers=headers, timeout=30)
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            print(f"📊 Response Body: {response.text}")
            
            if response.status_code == 200:
                print("✅ Upload successful!")
                return True
            else:
                print(f"❌ Upload failed with status {response.status_code}")
                return False
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_upload_with_real_image()











