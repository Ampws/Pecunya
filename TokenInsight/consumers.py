import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TokenInsightConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

    async def send_notification(self, event):
        await self.send(json.dumps(event))
