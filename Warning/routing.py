from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.AsyncConsumer.as_asgi()),
    re_path(r'^ws/msg/(?P<room_name>[^/]+)/$', consumers.AsyncConsumer.as_asgi()),
]