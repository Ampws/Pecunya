from django.http import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_websocket_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        channel_layer = get_channel_layer()

        # 构建发送到 WebSocket 的事件
        event = {
            "type": "send_notification",
            "message": message,
        }

        async_to_sync(channel_layer.group_send)("token_insight_group", event)

        return HttpResponse("Message sent to WebSocket")
    else:
        return HttpResponse("Invalid request method")
