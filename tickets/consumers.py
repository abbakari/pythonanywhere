import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Ticket, TicketMessage


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.ticket_group_name = f'ticket_{self.ticket_id}'

        # Join ticket group
        await self.channel_layer.group_add(
            self.ticket_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave ticket group
        await self.channel_layer.group_discard(
            self.ticket_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']

        # Save message to database
        await self.save_message(self.ticket_id, user_id, message)

        # Send message to ticket group
        await self.channel_layer.group_send(
            self.ticket_group_name,
            {
                'type': 'ticket_message',
                'message': message,
                'user_id': user_id,
                'timestamp': text_data_json.get('timestamp', '')
            }
        )

    async def ticket_message(self, event):
        message = event['message']
        user_id = event['user_id']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def save_message(self, ticket_id, user_id, message):
        ticket = Ticket.objects.get(id=ticket_id)
        user = User.objects.get(id=user_id)
        TicketMessage.objects.create(
            ticket=ticket,
            user=user,
            message=message
        )


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'dashboard_updates'

        # Join dashboard group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave dashboard group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle dashboard updates
        pass

    async def dashboard_update(self, event):
        # Send update to WebSocket
        await self.send(text_data=json.dumps(event['data']))
