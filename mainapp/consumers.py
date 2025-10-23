import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "global_chat"

        # Join chat group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle message received from WebSocket"""
        data = json.loads(text_data)
        username = data.get('username', 'Anonymous')
        message = data.get('message', '')

        if message.strip():
            await self.save_message(username, message)

            # Broadcast the message to all connected clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username': username,
                    'message': message
                }
            )

    async def chat_message(self, event):
        """Send message to WebSocket"""
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message']
        }))

    @sync_to_async
    def save_message(self, username, message):
        """Save message to the database"""
        user, _ = User.objects.get_or_create(username=username)
        Message.objects.create(user=user, content=message)
