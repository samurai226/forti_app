# conversations/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # WebSocket URL for chat functionality
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
    
    # WebSocket URL for specific conversations
    re_path(r'ws/conversations/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]

