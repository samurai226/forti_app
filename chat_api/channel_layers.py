# chat_api/channel_layers.py

import os
from channels_redis.core import RedisChannelLayer

def get_channel_layer():
    """
    Get the appropriate channel layer based on environment
    """
    try:
        redis_url = os.getenv('REDIS_URL')
        
        if redis_url:
            # Production: Use Redis
            return RedisChannelLayer(
                host=redis_url,
                capacity=1500,
                expiry=60,
            )
        else:
            # Development: Use in-memory layer
            from channels.layers import InMemoryChannelLayer
            return InMemoryChannelLayer()
    except Exception as e:
        # Fallback to in-memory if Redis is not available
        print(f"⚠️ Channel Layer: Redis not available, using in-memory layer: {e}")
        from channels.layers import InMemoryChannelLayer
        return InMemoryChannelLayer()

# Export the channel layer
channel_layer = get_channel_layer()




