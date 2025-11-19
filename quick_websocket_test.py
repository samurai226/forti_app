#!/usr/bin/env python
"""
Quick WebSocket Test
Tests ws://localhost:8000/ws/chat/?token={token}
"""
import asyncio
import websockets
import json
from datetime import datetime

async def test_websocket():
    """Quick WebSocket test"""
    print("🧪 Quick WebSocket Test")
    print("=" * 30)
    
    # Test URL
    ws_url = "ws://localhost:8000/ws/chat/?token=test_token_123"
    print(f"🔗 Testing: {ws_url}")
    
    try:
        async with websockets.connect(ws_url) as websocket:
            print("✅ Connected!")
            
            # Send ping
            ping = {"type": "ping", "timestamp": datetime.now().isoformat()}
            await websocket.send(json.dumps(ping))
            print("📤 Sent ping")
            
            # Wait for response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                print(f"📥 Received: {response}")
            except asyncio.TimeoutError:
                print("⚠️ No response (timeout)")
            
            print("✅ Test completed!")
            
    except ConnectionRefusedError:
        print("❌ Connection refused - server not running")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    asyncio.run(test_websocket())





