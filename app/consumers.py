from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json


class UpdateConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        if str(self.scope['user']) == 'AnonymousUser' and str(self.scope['client'][0]) == '127.0.0.1':
            self.room_group_name = 'server'
        else:
            self.room_group_name = 'client'
            await self.channel_layer.group_send(
            'server',
            {
                'type': 'send.message',
                'data': {
                    'message_type': 'sessions',
                    'username': str(self.scope['user']),
                    'ip_address': '%s.%s' % (self.scope['client'][0], self.scope['client'][1]),
                    'user_role': 'sessions_manager'
                },
            }
        )

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_add(
            '%s.%s' % (self.scope['client'][0], self.scope['client'][1]),
            self.channel_name
        )
        await self.accept()
        

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        sender = text_data['sender']
        data = text_data['data']
        recipient_ip = data['recipient_ip']
        data['sender_ip'] = '%s.%s' % (self.scope['client'][0], self.scope['client'][1])
        if sender == 'python':
            if recipient_ip == 'all':
                target_room_name = 'client'
            else:
                target_room_name = recipient_ip

        elif sender == 'UI':
            target_room_name = 'server'

        await self.channel_layer.group_send(
            target_room_name,
            {
                'type': 'send.message',
                'data': data,
            }
        )


    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            'data': event['data']
        }))


    async def disconnect(self, close_code):
        self.connected = False
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            '%s.%s' % (self.scope['client'][0], self.scope['client'][1]),
            self.channel_name
        )
