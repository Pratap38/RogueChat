import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from mainapp.routing import websocket_urlpatterns

# Make sure settings are loaded
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instabid.settings')

# Standard HTTP ASGI app
django_asgi_app = get_asgi_application()

# Full Protocol Router for HTTP + WebSocket
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
