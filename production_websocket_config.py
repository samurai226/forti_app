"""
Production WebSocket Configuration for FortiFun
Optimized for free hosting platforms
"""
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from conversations.routing import websocket_urlpatterns

# Django ASGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_api.settings')
django_asgi_app = get_asgi_application()

# Production WebSocket configuration
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})

# Production settings for different platforms
PRODUCTION_SETTINGS = {
    'railway': {
        'ALLOWED_HOSTS': ['*.railway.app', '*.up.railway.app'],
        'CORS_ALLOWED_ORIGINS': [
            'https://*.railway.app',
            'https://*.up.railway.app',
        ],
        'WEBSOCKET_URL': 'wss://your-app.railway.app/ws/chat/',
    },
    'render': {
        'ALLOWED_HOSTS': ['*.onrender.com'],
        'CORS_ALLOWED_ORIGINS': [
            'https://*.onrender.com',
        ],
        'WEBSOCKET_URL': 'wss://your-app.onrender.com/ws/chat/',
    },
    'heroku': {
        'ALLOWED_HOSTS': ['*.herokuapp.com'],
        'CORS_ALLOWED_ORIGINS': [
            'https://*.herokuapp.com',
        ],
        'WEBSOCKET_URL': 'wss://your-app.herokuapp.com/ws/chat/',
    },
    'fly': {
        'ALLOWED_HOSTS': ['*.fly.dev'],
        'CORS_ALLOWED_ORIGINS': [
            'https://*.fly.dev',
        ],
        'WEBSOCKET_URL': 'wss://your-app.fly.dev/ws/chat/',
    }
}

# Environment-specific configuration
def get_production_config():
    """Get production configuration based on environment"""
    if 'RAILWAY_ENVIRONMENT' in os.environ:
        return PRODUCTION_SETTINGS['railway']
    elif 'RENDER' in os.environ:
        return PRODUCTION_SETTINGS['render']
    elif 'HEROKU' in os.environ:
        return PRODUCTION_SETTINGS['heroku']
    elif 'FLY' in os.environ:
        return PRODUCTION_SETTINGS['fly']
    else:
        return PRODUCTION_SETTINGS['railway']  # Default to Railway

# WebSocket URL for Flutter app
WEBSOCKET_BASE_URL = get_production_config()['WEBSOCKET_URL']

print(f"🌐 Production WebSocket URL: {WEBSOCKET_BASE_URL}")




