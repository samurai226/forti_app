# WebSocket Setup Summary

## Overview
Added full WebSocket support to the FortiFun Django backend to enable real-time chat functionality with the Flutter app.

## Files Created

### 1. `/conversations/consumers.py`
- **ChatConsumer**: AsyncWebsocketConsumer for handling WebSocket connections
- Features:
  - JWT authentication via query string token
  - Connection/disconnection handling
  - Message broadcasting to conversation groups
  - Typing indicators
  - Read receipts
  - Ping/pong heartbeat mechanism
- Group management for real-time notifications

### 2. `/conversations/routing.py`
- WebSocket URL patterns:
  - `ws/chat/` - General chat WebSocket
  - `ws/conversations/<id>/` - Specific conversation WebSocket

### 3. `/chat_api/asgi.py`
- ASGI application configuration
- Protocol routing (HTTP + WebSocket)
- Authentication middleware for WebSocket
- AllowedHostsOriginValidator for security

## Files Modified

### 1. `/requirements.txt`
Added WebSocket dependencies:
```
channels>=4.0.0
channels-redis>=4.2.0
daphne>=4.0.0
```

### 2. `/chat_api/channel_layers.py`
- Enhanced error handling
- Fallback to in-memory layer if Redis unavailable
- Support for both development and production environments

### 3. `/chat_api/settings.py` (already configured)
- `ASGI_APPLICATION = 'chat_api.asgi.application'`
- Channel layers configuration
- In-memory layer for development, Redis for production

## WebSocket Features

### Authentication
- Uses JWT tokens passed as query parameter: `?token=<jwt_token>`
- Validates token using Django REST Framework SimpleJWT
- Returns appropriate error codes for authentication failures

### Message Types
1. **ping** - Heartbeat to keep connection alive
2. **join_conversation** - Join a specific conversation group
3. **leave_conversation** - Leave a conversation group
4. **new_message** - Send a new message (handled by HTTP API)
5. **typing** - Send typing indicator
6. **read_receipt** - Mark message as read

### Broadcasting
- Messages broadcast to conversation groups
- Real-time notifications to all connected clients
- Support for multiple concurrent connections

## Running the Server

### Development (with in-memory layer)
```bash
daphne -b 0.0.0.0 -p 8000 chat_api.asgi:application
```

### Production (with Redis)
```bash
# Set REDIS_URL environment variable
export REDIS_URL=redis://localhost:6379
daphne -b 0.0.0.0 -p 8000 chat_api.asgi:application
```

## Testing WebSocket

### From Python
```python
import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:8000/ws/chat/?token=YOUR_JWT_TOKEN"
    async with websockets.connect(uri) as websocket:
        # Send ping
        await websocket.send(json.dumps({
            "type": "ping",
            "timestamp": "2024-01-01T00:00:00Z"
        }))
        
        # Receive response
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.run(test())
```

### From Browser Console
```javascript
const token = 'YOUR_JWT_TOKEN';
const ws = new WebSocket(`ws://localhost:8000/ws/chat/?token=${token}`);

ws.onopen = () => console.log('Connected');
ws.onmessage = (event) => console.log('Received:', JSON.parse(event.data));
ws.onerror = (error) => console.error('Error:', error);
ws.onclose = () => console.log('Disconnected');

// Send ping
ws.send(JSON.stringify({
    type: 'ping',
    timestamp: new Date().toISOString()
}));
```

## Flutter Integration

The Flutter app already has `UnifiedWebSocketService` that connects to:
- URL: `ws://<base_url>/ws/chat/?token=<jwt_token>`
- Handles connection, reconnection, and message routing
- Supports conversation-specific connections

## Next Steps

1. ✅ Backend WebSocket support added
2. ⏳ Test WebSocket connection from Flutter app
3. ⏳ Deploy to Render with WebSocket support
4. ⏳ Configure Redis for production scaling

## Security Notes

- WebSocket connections require valid JWT tokens
- AllowedHostsOriginValidator prevents unauthorized origins
- Authentication middleware validates user on connection
- Close code 4001 for unauthorized connections

## Troubleshooting

### Connection refused
- Ensure Daphne server is running
- Check firewall settings
- Verify port 8000 is accessible

### Authentication failed
- Verify JWT token is valid and not expired
- Check token is being passed correctly in query string
- Ensure user exists in database

### Messages not broadcasting
- Check channel layer configuration
- Verify Redis is running (production)
- Check server logs for errors

