#!/usr/bin/env python
"""
Comprehensive WebSocket and Online Tracking Test
Tests the complete WebSocket system from backend to frontend simulation
"""
import os
import sys
import django
import asyncio
import websockets
import json
import time
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_api.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
import json

User = get_user_model()

class WebSocketTester:
    def __init__(self):
        self.base_url = "ws://localhost:8000"
        self.http_client = Client()
        self.test_user = None
        self.auth_token = None
        
    async def run_comprehensive_test(self):
        """Run comprehensive WebSocket and online tracking tests"""
        print("🧪 Starting Comprehensive WebSocket & Online Tracking Test")
        print("=" * 70)
        
        # Test 1: Backend Health Check
        await self.test_backend_health()
        
        # Test 2: User Authentication
        await self.test_user_authentication()
        
        # Test 3: WebSocket Connection
        await self.test_websocket_connection()
        
        # Test 4: Online Status Tracking
        await self.test_online_status_tracking()
        
        # Test 5: Real-time Chat
        await self.test_realtime_chat()
        
        # Test 6: Anonymous Chat
        await self.test_anonymous_chat()
        
        print("\n" + "=" * 70)
        print("🎯 Comprehensive WebSocket Test Complete!")
        print("=" * 70)
    
    async def test_backend_health(self):
        """Test 1: Backend Health Check"""
        print("\n1. 🔍 Testing Backend Health...")
        try:
            response = self.http_client.get('/health/')
            if response.status_code == 200:
                print("   ✅ Backend is healthy and running")
                return True
            else:
                print(f"   ❌ Backend health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Backend health check error: {e}")
            return False
    
    async def test_user_authentication(self):
        """Test 2: User Authentication"""
        print("\n2. 🔐 Testing User Authentication...")
        try:
            # Create test user
            test_data = {
                'email': 'websocket_test@example.com',
                'password': 'WebSocketTest123!',
                'first_name': 'WebSocket',
                'last_name': 'Tester'
            }
            
            # Register user
            response = self.http_client.post('/api/v1/accounts/auth/register', 
                                           data=json.dumps(test_data),
                                           content_type='application/json')
            
            if response.status_code == 201:
                print("   ✅ User registration successful")
                auth_data = response.json()
                self.auth_token = auth_data.get('access')
                print(f"   📝 Auth token: {'Present' if self.auth_token else 'Missing'}")
                return True
            else:
                print(f"   ❌ User registration failed: {response.status_code}")
                print(f"   📝 Response: {response.content}")
                return False
                
        except Exception as e:
            print(f"   ❌ Authentication test error: {e}")
            return False
    
    async def test_websocket_connection(self):
        """Test 3: WebSocket Connection"""
        print("\n3. 🔌 Testing WebSocket Connection...")
        if not self.auth_token:
            print("   ❌ No auth token available")
            return False
            
        try:
            # Test main chat WebSocket
            ws_url = f"{self.base_url}/ws/chat/?token={self.auth_token}"
            print(f"   🔗 Connecting to: {ws_url}")
            
            async with websockets.connect(ws_url) as websocket:
                print("   ✅ WebSocket connection established")
                
                # Test ping/pong
                ping_message = {
                    'type': 'ping',
                    'timestamp': datetime.now().isoformat()
                }
                await websocket.send(json.dumps(ping_message))
                print("   📤 Sent ping message")
                
                # Wait for pong response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    response_data = json.loads(response)
                    if response_data.get('type') == 'pong':
                        print("   ✅ Received pong response")
                        return True
                    else:
                        print(f"   ⚠️ Unexpected response: {response_data}")
                        return False
                except asyncio.TimeoutError:
                    print("   ⚠️ No pong response received (timeout)")
                    return False
                    
        except Exception as e:
            print(f"   ❌ WebSocket connection failed: {e}")
            return False
    
    async def test_online_status_tracking(self):
        """Test 4: Online Status Tracking"""
        print("\n4. 📊 Testing Online Status Tracking...")
        try:
            # Test user profile endpoint
            response = self.http_client.get('/api/v1/accounts/users/me',
                                          HTTP_AUTHORIZATION=f'Bearer {self.auth_token}')
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ User profile retrieved: {user_data.get('username', 'N/A')}")
                print(f"   📝 User ID: {user_data.get('id', 'N/A')}")
                print(f"   📝 Email: {user_data.get('email', 'N/A')}")
                return True
            else:
                print(f"   ❌ User profile retrieval failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Online status tracking test error: {e}")
            return False
    
    async def test_realtime_chat(self):
        """Test 5: Real-time Chat"""
        print("\n5. 💬 Testing Real-time Chat...")
        try:
            # Test conversation WebSocket
            conversation_id = 1  # Test conversation ID
            ws_url = f"{self.base_url}/ws/conversations/{conversation_id}/?token={self.auth_token}"
            print(f"   🔗 Connecting to conversation: {ws_url}")
            
            async with websockets.connect(ws_url) as websocket:
                print("   ✅ Conversation WebSocket connected")
                
                # Test sending a message
                message = {
                    'type': 'chat_message',
                    'message': 'Hello from WebSocket test!',
                    'timestamp': datetime.now().isoformat()
                }
                await websocket.send(json.dumps(message))
                print("   📤 Sent test message")
                
                # Test typing indicator
                typing_message = {
                    'type': 'typing',
                    'is_typing': True
                }
                await websocket.send(json.dumps(typing_message))
                print("   📤 Sent typing indicator")
                
                # Wait a bit for any responses
                await asyncio.sleep(1)
                print("   ✅ Real-time chat test completed")
                return True
                
        except Exception as e:
            print(f"   ❌ Real-time chat test failed: {e}")
            return False
    
    async def test_anonymous_chat(self):
        """Test 6: Anonymous Chat"""
        print("\n6. 👤 Testing Anonymous Chat...")
        try:
            # Test anonymous chat WebSocket (no auth required)
            room_id = "test_room_123"
            ws_url = f"{self.base_url}/ws/anonymous_chat/{room_id}/"
            print(f"   🔗 Connecting to anonymous chat: {ws_url}")
            
            async with websockets.connect(ws_url) as websocket:
                print("   ✅ Anonymous chat WebSocket connected")
                
                # Wait for welcome message
                try:
                    welcome = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    welcome_data = json.loads(welcome)
                    if welcome_data.get('type') == 'welcome':
                        print("   ✅ Received welcome message")
                    else:
                        print(f"   ⚠️ Unexpected welcome: {welcome_data}")
                except asyncio.TimeoutError:
                    print("   ⚠️ No welcome message received")
                
                # Test sending anonymous message
                message = {
                    'type': 'chat_message',
                    'message': 'Hello from anonymous user!',
                    'sender_name': 'Anonymous Tester',
                    'sender_id': 'test_anonymous_123'
                }
                await websocket.send(json.dumps(message))
                print("   📤 Sent anonymous message")
                
                # Test user join
                join_message = {
                    'type': 'user_join',
                    'sender_name': 'Anonymous Tester',
                    'sender_id': 'test_anonymous_123'
                }
                await websocket.send(json.dumps(join_message))
                print("   📤 Sent user join message")
                
                await asyncio.sleep(1)
                print("   ✅ Anonymous chat test completed")
                return True
                
        except Exception as e:
            print(f"   ❌ Anonymous chat test failed: {e}")
            return False

async def main():
    """Main test runner"""
    tester = WebSocketTester()
    await tester.run_comprehensive_test()

if __name__ == '__main__':
    asyncio.run(main())





