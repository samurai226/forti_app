#!/usr/bin/env python
"""
Test script to verify Flutter authentication integration with Django backend
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_api.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
import json

User = get_user_model()

def test_flutter_auth_integration():
    """Test the authentication endpoints that Flutter will use"""
    client = Client()
    
    print("🧪 Testing Flutter Authentication Integration")
    print("=" * 60)
    
    # Test 1: User Registration (Flutter format)
    print("\n1. Testing User Registration (Flutter format)...")
    register_data = {
        'email': 'flutter_test@example.com',
        'password': 'FlutterTest123!',
        'first_name': 'Flutter',
        'last_name': 'User'
    }
    
    try:
        response = client.post('/api/v1/accounts/auth/register', 
                             data=json.dumps(register_data),
                             content_type='application/json')
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Registration successful")
            response_data = response.json()
            print(f"   User ID: {response_data.get('user', {}).get('id', 'N/A')}")
            print(f"   Access Token: {'Present' if 'access' in response_data else 'Missing'}")
            print(f"   Refresh Token: {'Present' if 'refresh' in response_data else 'Missing'}")
        else:
            print(f"   ❌ Registration failed: {response.content}")
            
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
    
    # Test 2: User Login (Flutter format)
    print("\n2. Testing User Login (Flutter format)...")
    login_data = {
        'email': 'flutter_test@example.com',
        'password': 'FlutterTest123!'
    }
    
    try:
        response = client.post('/api/v1/accounts/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Login successful")
            response_data = response.json()
            print(f"   Access Token: {'Present' if 'access' in response_data else 'Missing'}")
            print(f"   Refresh Token: {'Present' if 'refresh' in response_data else 'Missing'}")
            print(f"   User Data: {'Present' if 'user' in response_data else 'Missing'}")
            
            # Store tokens for next tests
            access_token = response_data.get('access')
            refresh_token = response_data.get('refresh')
        else:
            print(f"   ❌ Login failed: {response.content}")
            access_token = None
            refresh_token = None
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        access_token = None
        refresh_token = None
    
    # Test 3: Get User Profile
    print("\n3. Testing Get User Profile...")
    if access_token:
        try:
            response = client.get('/api/v1/accounts/users/me',
                                HTTP_AUTHORIZATION=f'Bearer {access_token}')
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Profile retrieval successful")
                profile_data = response.json()
                print(f"   User ID: {profile_data.get('id', 'N/A')}")
                print(f"   Username: {profile_data.get('username', 'N/A')}")
                print(f"   Email: {profile_data.get('email', 'N/A')}")
                print(f"   First Name: {profile_data.get('first_name', 'N/A')}")
                print(f"   Last Name: {profile_data.get('last_name', 'N/A')}")
            else:
                print(f"   ❌ Profile retrieval failed: {response.content}")
        except Exception as e:
            print(f"   ❌ Profile retrieval error: {e}")
    else:
        print("   ⏭️ Skipping profile test (no access token)")
    
    # Test 4: Token Refresh
    print("\n4. Testing Token Refresh...")
    if refresh_token:
        try:
            response = client.post('/api/v1/accounts/auth/refresh',
                                 data=json.dumps({'refresh': refresh_token}),
                                 content_type='application/json')
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Token refresh successful")
                refresh_data = response.json()
                print(f"   New Access Token: {'Present' if 'access' in refresh_data else 'Missing'}")
                print(f"   User Data in Refresh: {'Present' if 'user' in refresh_data else 'Missing'}")
            else:
                print(f"   ❌ Token refresh failed: {response.content}")
        except Exception as e:
            print(f"   ❌ Token refresh error: {e}")
    else:
        print("   ⏭️ Skipping token refresh test (no refresh token)")
    
    # Test 5: Logout
    print("\n5. Testing Logout...")
    if access_token:
        try:
            response = client.post('/api/v1/accounts/auth/logout',
                                 HTTP_AUTHORIZATION=f'Bearer {access_token}')
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Logout successful")
                logout_data = response.json()
                print(f"   Response: {logout_data}")
            else:
                print(f"   ❌ Logout failed: {response.content}")
        except Exception as e:
            print(f"   ❌ Logout error: {e}")
    else:
        print("   ⏭️ Skipping logout test (no access token)")
    
    print("\n" + "=" * 60)
    print("🎯 Flutter Authentication Integration Test Complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_flutter_auth_integration()





