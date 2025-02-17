from asgiref.sync import async_to_sync
# Create your views here.
# views.py
from channels.layers import get_channel_layer
from django.shortcuts import render


def notify_user(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",  # Group name
        {
            'type': 'send_notification',
            'message': message
        }
    )
