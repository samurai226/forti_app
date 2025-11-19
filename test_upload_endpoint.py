#!/usr/bin/env python3
"""
Test script to verify the profile picture upload endpoint
"""

import requests
import os
from pathlib import Path

def test_upload_endpoint():
    print("🧪 Testing profile picture upload endpoint...")
    
    # Backend URL
    base_url = "https://forti-app.onrender.com"
    upload_url = f"{base_url}/api/v1/accounts/files/profile-picture"
    
    # Create a test image file
    test_image_path = "test_image.jpg"
    
    # Create a simple test image (1x1 pixel JPEG)
    test_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x08\x01\x01\x00\x00?\x00\x00\xff\xd9'
    
    try:
        # Write test image
        with open(test_image_path, 'wb') as f:
            f.write(test_image_data)
        
        print(f"✅ Test image created: {test_image_path}")
        
        # Test the upload endpoint
        print(f"🌐 Testing upload to: {upload_url}")
        
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test_image.jpg', f, 'image/jpeg')}
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
    finally:
        # Clean up test file
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            print(f"🧹 Cleaned up test file: {test_image_path}")

if __name__ == "__main__":
    test_upload_endpoint()











