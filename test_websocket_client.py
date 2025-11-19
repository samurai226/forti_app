#!/usr/bin/env python3
"""
WebSocket Test Client for Django Backend
Tests WebSocket connections and chat functionality
"""

import asyncio
import websockets
import json
import time
from datetime import datetime

class WebSocketTestClient:
    def __init__(self, base_url="ws://127.0.0.1:8000"):
        self.base_url = base_url
        self.connections = {}
    
    async def test_main_chat_connection(self):
        """Test main chat WebSocket connection"""
        print("🔗 Testing Main Chat Connection...")
        
        uri = f"{self.base_url}/ws/chat/"
        try:
            async with websockets.connect(uri) as websocket:
                print("✅ Connected to main chat")
                
                # Send ping
                await websocket.send(json.dumps({
                    "type": "ping"
                }))
                
                # Wait for pong
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                print(f"📨 Received: {data}")
                
                return True
        except Exception as e:
            print(f"❌ Main chat connection failed: {e}")
            return False
    
    async def test_anonymous_chat_connection(self):
        """Test anonymous chat WebSocket connection"""
        print("🔗 Testing Anonymous Chat Connection...")
        
        room_id = f"test_room_{int(time.time())}"
        uri = f"{self.base_url}/ws/anonymous-chat/{room_id}/"
        
        try:
            async with websockets.connect(uri) as websocket:
                print(f"✅ Connected to anonymous chat room: {room_id}")
                
                # Wait for welcome message
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                print(f"📨 Welcome message: {data}")
                
                # Send a test message
                await websocket.send(json.dumps({
                    "type": "chat_message",
                    "message": "Hello from test client!",
                    "sender_name": "TestUser",
                    "sender_id": "test_123"
                }))
                
                # Wait for echo
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                print(f"📨 Echo message: {data}")
                
                return True
        except Exception as e:
            print(f"❌ Anonymous chat connection failed: {e}")
            return False
    
    async def test_conversation_connection(self):
        """Test conversation WebSocket connection (requires authentication)"""
        print("🔗 Testing Conversation Connection...")
        
        # This requires JWT authentication, so we'll just test the endpoint
        conversation_id = 1
        uri = f"{self.base_url}/ws/conversations/{conversation_id}/"
        
        try:
            async with websockets.connect(uri) as websocket:
                print(f"✅ Connected to conversation {conversation_id}")
                return True
        except Exception as e:
            print(f"❌ Conversation connection failed (expected without auth): {e}")
            return False
    
    async def test_notifications_connection(self):
        """Test notifications WebSocket connection (requires authentication)"""
        print("🔗 Testing Notifications Connection...")
        
        uri = f"{self.base_url}/ws/notifications/"
        
        try:
            async with websockets.connect(uri) as websocket:
                print("✅ Connected to notifications")
                return True
        except Exception as e:
            print(f"❌ Notifications connection failed (expected without auth): {e}")
            return False
    
    async def run_all_tests(self):
        """Run all WebSocket tests"""
        print("🚀 Starting WebSocket Tests...")
        print("=" * 50)
        
        tests = [
            ("Main Chat", self.test_main_chat_connection),
            ("Anonymous Chat", self.test_anonymous_chat_connection),
            ("Conversations", self.test_conversation_connection),
            ("Notifications", self.test_notifications_connection),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            print(f"\n🧪 Testing {test_name}...")
            try:
                result = await test_func()
                results[test_name] = result
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"{status} - {test_name}")
            except Exception as e:
                results[test_name] = False
                print(f"❌ FAILED - {test_name}: {e}")
        
        print("\n" + "=" * 50)
        print("📊 Test Results Summary:")
        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} - {test_name}")
        
        passed = sum(results.values())
        total = len(results)
        print(f"\n🎯 Overall: {passed}/{total} tests passed")
        
        return results

async def main():
    """Main test function"""
    print("🔧 Django WebSocket Test Client")
    print("=" * 50)
    print("Make sure Django backend is running with:")
    print("daphne -b 127.0.0.1 -p 8000 chat_api.asgi:application")
    print("=" * 50)
    
    client = WebSocketTestClient()
    await client.run_all_tests()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")






