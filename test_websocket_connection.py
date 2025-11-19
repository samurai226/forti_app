#!/usr/bin/env python
"""
Direct WebSocket Connection Test
Tests the specific WebSocket endpoint: ws://localhost:8000/ws/chat/?token={token}
"""
import asyncio
import websockets
import json
import time
from datetime import datetime

async def test_websocket_connection():
    """Test WebSocket connection to ws://localhost:8000/ws/chat/?token={token}"""
    print("🧪 Testing WebSocket Connection")
    print("=" * 50)
    
    # Test with a sample token (you can replace this with a real token)
    test_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozNjksImV4cCI6MTczMjM2NzQ4NSwiZW1haWwiOiJ3ZWJzb2NrZXRfdGVzdDJAZXhhbXBsZS5jb20ifQ.test_signature"
    
    # WebSocket URL
    ws_url = f"ws://localhost:8000/ws/chat/?token={test_token}"
    print(f"🔗 Connecting to: {ws_url}")
    
    try:
        # Connect to WebSocket
        async with websockets.connect(ws_url) as websocket:
            print("✅ WebSocket connection established!")
            
            # Test 1: Send ping message
            print("\n📤 Sending ping message...")
            ping_message = {
                "type": "ping",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(ping_message))
            print(f"   Sent: {json.dumps(ping_message)}")
            
            # Wait for pong response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                response_data = json.loads(response)
                print(f"📥 Received: {response_data}")
                
                if response_data.get('type') == 'pong':
                    print("✅ Ping/Pong test successful!")
                else:
                    print(f"⚠️ Unexpected response type: {response_data.get('type')}")
                    
            except asyncio.TimeoutError:
                print("⚠️ No response received (timeout)")
            
            # Test 2: Send a test message
            print("\n📤 Sending test message...")
            test_message = {
                "type": "test_message",
                "content": "Hello from WebSocket test!",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(test_message))
            print(f"   Sent: {json.dumps(test_message)}")
            
            # Wait for any response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                response_data = json.loads(response)
                print(f"📥 Received: {response_data}")
            except asyncio.TimeoutError:
                print("   No response to test message")
            
            # Test 3: Send typing indicator
            print("\n📤 Sending typing indicator...")
            typing_message = {
                "type": "typing",
                "is_typing": True,
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(typing_message))
            print(f"   Sent: {json.dumps(typing_message)}")
            
            # Wait a bit for any responses
            await asyncio.sleep(1)
            
            print("\n✅ WebSocket connection test completed!")
            
    except websockets.exceptions.ConnectionClosed as e:
        print(f"❌ WebSocket connection closed: {e}")
    except websockets.exceptions.InvalidURI as e:
        print(f"❌ Invalid WebSocket URI: {e}")
    except ConnectionRefusedError:
        print("❌ Connection refused - is the Django server running?")
        print("   Make sure to run: python manage.py runserver 0.0.0.0:8000")
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")

async def test_with_real_token():
    """Test with a real authentication token"""
    print("\n🔐 Testing with Real Authentication Token")
    print("=" * 50)
    
    # First, get a real token by logging in
    import requests
    
    try:
        # Login to get a real token
        login_data = {
            "email": "websocket_test2@example.com",
            "password": "WebSocketTest123!"
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/accounts/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            auth_data = response.json()
            real_token = auth_data.get('access')
            print(f"✅ Got real token: {real_token[:50]}...")
            
            # Test WebSocket with real token
            ws_url = f"ws://localhost:8000/ws/chat/?token={real_token}"
            print(f"🔗 Connecting to: {ws_url}")
            
            async with websockets.connect(ws_url) as websocket:
                print("✅ WebSocket connection with real token established!")
                
                # Send ping
                ping_message = {
                    "type": "ping",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(ping_message))
                print("📤 Sent ping with real token")
                
                # Wait for response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    response_data = json.loads(response)
                    print(f"📥 Received: {response_data}")
                    print("✅ Real token WebSocket test successful!")
                except asyncio.TimeoutError:
                    print("⚠️ No response received")
                    
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Real token test failed: {e}")

async def main():
    """Main test runner"""
    print("🧪 WebSocket Connection Test Suite")
    print("=" * 60)
    
    # Test 1: Basic connection test
    await test_websocket_connection()
    
    # Test 2: Real token test
    await test_with_real_token()
    
    print("\n" + "=" * 60)
    print("🎯 WebSocket Connection Test Complete!")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())





