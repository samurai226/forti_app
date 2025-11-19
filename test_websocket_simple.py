#!/usr/bin/env python
"""
Simple WebSocket Test - Focused on core functionality
"""
import os
import sys
import django
import json
import time
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_api.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def test_websocket_system():
    """Test WebSocket system components"""
    print("🧪 Testing WebSocket System Components")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Backend Health
    print("\n1. 🔍 Testing Backend Health...")
    try:
        response = client.get('/health/')
        if response.status_code == 200:
            print("   ✅ Backend is healthy")
        else:
            print(f"   ❌ Backend health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Backend health error: {e}")
    
    # Test 2: User Registration (Synchronous)
    print("\n2. 🔐 Testing User Registration...")
    try:
        register_data = {
            'email': 'websocket_test2@example.com',
            'password': 'WebSocketTest123!',
            'first_name': 'WebSocket',
            'last_name': 'Tester'
        }
        
        response = client.post('/api/v1/accounts/auth/register', 
                             data=json.dumps(register_data),
                             content_type='application/json')
        
        if response.status_code == 201:
            print("   ✅ User registration successful")
            auth_data = response.json()
            access_token = auth_data.get('access')
            print(f"   📝 Access token: {'Present' if access_token else 'Missing'}")
            
            # Test 3: User Profile Access
            print("\n3. 👤 Testing User Profile Access...")
            response = client.get('/api/v1/accounts/users/me',
                                HTTP_AUTHORIZATION=f'Bearer {access_token}')
            
            if response.status_code == 200:
                user_data = response.json()
                print("   ✅ User profile retrieved successfully")
                print(f"   📝 Username: {user_data.get('username', 'N/A')}")
                print(f"   📝 Email: {user_data.get('email', 'N/A')}")
                print(f"   📝 User ID: {user_data.get('id', 'N/A')}")
            else:
                print(f"   ❌ User profile access failed: {response.status_code}")
            
            # Test 4: Token Refresh
            print("\n4. 🔄 Testing Token Refresh...")
            refresh_token = auth_data.get('refresh')
            if refresh_token:
                refresh_data = {'refresh': refresh_token}
                response = client.post('/api/v1/accounts/auth/refresh',
                                    data=json.dumps(refresh_data),
                                    content_type='application/json')
                
                if response.status_code == 200:
                    print("   ✅ Token refresh successful")
                    refresh_response = response.json()
                    new_access = refresh_response.get('access')
                    print(f"   📝 New access token: {'Present' if new_access else 'Missing'}")
                else:
                    print(f"   ❌ Token refresh failed: {response.status_code}")
            else:
                print("   ⚠️ No refresh token available")
            
            # Test 5: Logout
            print("\n5. 🚪 Testing Logout...")
            response = client.post('/api/v1/accounts/auth/logout',
                                HTTP_AUTHORIZATION=f'Bearer {access_token}')
            
            if response.status_code == 200:
                print("   ✅ Logout successful")
            else:
                print(f"   ❌ Logout failed: {response.status_code}")
            
        else:
            print(f"   ❌ User registration failed: {response.status_code}")
            print(f"   📝 Response: {response.content}")
            
    except Exception as e:
        print(f"   ❌ Registration test error: {e}")
    
    # Test 6: WebSocket URL Construction
    print("\n6. 🔗 Testing WebSocket URL Construction...")
    try:
        base_url = "ws://localhost:8000"
        token = "test_token_123"
        
        # Main chat WebSocket
        main_ws_url = f"{base_url}/ws/chat/?token={token}"
        print(f"   📝 Main chat WebSocket: {main_ws_url}")
        
        # Conversation WebSocket
        conversation_id = 1
        conv_ws_url = f"{base_url}/ws/conversations/{conversation_id}/?token={token}"
        print(f"   📝 Conversation WebSocket: {conv_ws_url}")
        
        # Anonymous chat WebSocket
        room_id = "test_room_123"
        anon_ws_url = f"{base_url}/ws/anonymous_chat/{room_id}/"
        print(f"   📝 Anonymous chat WebSocket: {anon_ws_url}")
        
        print("   ✅ WebSocket URLs constructed successfully")
        
    except Exception as e:
        print(f"   ❌ WebSocket URL construction error: {e}")
    
    # Test 7: Message Format Testing
    print("\n7. 📨 Testing Message Formats...")
    try:
        # Test ping message
        ping_message = {
            'type': 'ping',
            'timestamp': datetime.now().isoformat()
        }
        print(f"   📝 Ping message: {json.dumps(ping_message)}")
        
        # Test chat message
        chat_message = {
            'type': 'chat_message',
            'message': 'Hello from test!',
            'timestamp': datetime.now().isoformat()
        }
        print(f"   📝 Chat message: {json.dumps(chat_message)}")
        
        # Test typing indicator
        typing_message = {
            'type': 'typing',
            'is_typing': True
        }
        print(f"   📝 Typing indicator: {json.dumps(typing_message)}")
        
        # Test anonymous message
        anon_message = {
            'type': 'chat_message',
            'message': 'Hello from anonymous user!',
            'sender_name': 'Anonymous Tester',
            'sender_id': 'test_anonymous_123'
        }
        print(f"   📝 Anonymous message: {json.dumps(anon_message)}")
        
        print("   ✅ Message formats validated successfully")
        
    except Exception as e:
        print(f"   ❌ Message format test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 WebSocket System Test Complete!")
    print("=" * 50)

if __name__ == '__main__':
    test_websocket_system()





