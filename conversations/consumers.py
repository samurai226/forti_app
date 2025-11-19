# conversations/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from .models import Conversation, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for chat functionality"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = None
        self.user_id = None
        self.group_name = None
        
        # Get token from query string
        token = self.scope.get('query_string', b'').decode().split('token=')[-1]
        
        if not token:
            await self.close(code=4001)  # Unauthorized
            return
        
        # Authenticate user
        try:
            self.user = await self.authenticate_user(token)
            if self.user is None or isinstance(self.user, AnonymousUser):
                print(f"❌ ChatConsumer: Authentication failed - Invalid user")
                await self.close(code=4001)  # Unauthorized
                return
            
            self.user_id = self.user.id
            print(f"✅ ChatConsumer: User authenticated - {self.user.username} (ID: {self.user_id})")
            
        except Exception as e:
            print(f"❌ ChatConsumer: Authentication error - {e}")
            await self.close(code=4001)  # Unauthorized
            return
        
        # Join general notifications group
        self.group_name = 'general_chat_notifications'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"✅ ChatConsumer: WebSocket connected for user {self.user.username}")
        
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'connection_status',
            'status': 'connected',
            'user_id': self.user_id,
            'username': self.user.username,
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if self.group_name:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        print(f"🔌 ChatConsumer: User {self.user_id} disconnected (code: {close_code})")
    
    @database_sync_to_async
    def authenticate_user(self, token):
        """Authenticate user using JWT token"""
        try:
            # Validate token
            UntypedToken(token)
            
            # Get user from token
            valid_data = JWTAuthentication().get_validated_token(token)
            user_id = valid_data['user_id']
            user = User.objects.get(id=user_id)
            
            return user
        except (TokenError, InvalidToken) as e:
            print(f"❌ ChatConsumer: Token error - {e}")
            return None
        except User.DoesNotExist:
            print(f"❌ ChatConsumer: User not found")
            return None
        except Exception as e:
            print(f"❌ ChatConsumer: Authentication exception - {e}")
            return None
    
    async def receive(self, text_data):
        """Handle incoming messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            print(f"📥 ChatConsumer: Received message type '{message_type}' from user {self.user_id}")
            
            # Handle different message types
            if message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': data.get('timestamp'),
                }))
            
            elif message_type == 'join_conversation':
                conversation_id = data.get('conversation_id')
                await self.join_conversation(conversation_id)
            
            elif message_type == 'leave_conversation':
                conversation_id = data.get('conversation_id')
                await self.leave_conversation(conversation_id)
            
            elif message_type == 'new_message':
                await self.handle_new_message(data)
            
            elif message_type == 'typing':
                await self.handle_typing(data)
            
            elif message_type == 'read_receipt':
                await self.handle_read_receipt(data)
            
        except json.JSONDecodeError:
            print(f"❌ ChatConsumer: Invalid JSON received")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format',
            }))
        except Exception as e:
            print(f"❌ ChatConsumer: Error processing message - {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e),
            }))
    
    async def join_conversation(self, conversation_id):
        """Join conversation group for real-time updates"""
        group_name = f'chat_{conversation_id}'
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        print(f"✅ ChatConsumer: User {self.user_id} joined conversation {conversation_id}")
    
    async def leave_conversation(self, conversation_id):
        """Leave conversation group"""
        group_name = f'chat_{conversation_id}'
        await self.channel_layer.group_discard(
            group_name,
            self.channel_name
        )
        print(f"🔌 ChatConsumer: User {self.user_id} left conversation {conversation_id}")
    
    async def handle_new_message(self, data):
        """Handle new message"""
        # This would typically be handled by the HTTP endpoint
        # and broadcasted via WebSocket
        pass
    
    async def handle_typing(self, data):
        """Handle typing indicator"""
        conversation_id = data.get('conversation_id')
        is_typing = data.get('is_typing', False)
        
        # Broadcast typing indicator to conversation group
        if conversation_id:
            group_name = f'chat_{conversation_id}'
            await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'typing_indicator',
                    'user_id': self.user_id,
                    'username': self.user.username,
                    'is_typing': is_typing,
                    'conversation_id': conversation_id,
                }
            )
    
    async def handle_read_receipt(self, data):
        """Handle read receipt"""
        conversation_id = data.get('conversation_id')
        message_id = data.get('message_id')
        
        # Broadcast read receipt to conversation group
        if conversation_id and message_id:
            group_name = f'chat_{conversation_id}'
            await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'read_receipt',
                    'user_id': self.user_id,
                    'message_id': message_id,
                    'conversation_id': conversation_id,
                }
            )
    
    # Handler methods for group messages
    async def chat_message(self, event):
        """Handle chat_message from group"""
        await self.send(text_data=json.dumps(event['message']))
    
    async def new_message(self, event):
        """Handle new_message notification"""
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'conversation_id': event.get('conversation_id'),
            'message': event.get('message'),
        }))
    
    async def typing_indicator(self, event):
        """Handle typing indicator"""
        await self.send(text_data=json.dumps({
            'type': 'typing_indicator',
            'conversation_id': event.get('conversation_id'),
            'user_id': event.get('user_id'),
            'username': event.get('username'),
            'is_typing': event.get('is_typing', False),
        }))
    
    async def read_receipt(self, event):
        """Handle read receipt"""
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'conversation_id': event.get('conversation_id'),
            'message_id': event.get('message_id'),
            'user_id': event.get('user_id'),
        }))
    
    async def conversation_update(self, event):
        """Handle conversation update"""
        await self.send(text_data=json.dumps({
            'type': 'conversation_update',
            'conversation_id': event.get('conversation_id'),
            'action': event.get('action'),
            'data': event.get('data'),
        }))

