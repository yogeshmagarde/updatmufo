
from . import consumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/chats/<str:room_code>/', consumer.ChatConsumer.as_asgi()),
    path('ws/chats2/<str:room_code>/', consumer.ChatConsumer2.as_asgi()),
    path('ws/chats_sdp/<str:room_code>/', consumer.ChatConsumer_sdp.as_asgi()),
    path('ws/notif/', consumer.NotifConsumer.as_asgi()),
    path('ws/test/', consumer.TestConsumer.as_asgi()),
    path("ws/chatmessage/<str:room_name>/", consumer.OnetoOneChatConsumer.as_asgi()),
    # path('ws/chatmessage/<int:user_id>/', consumer.ChatConsumer1.as_asgi()),
    
]
