import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import api.routing
import channels_backend.routing
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abstractbaseuser_project.settings')

wsgi_application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": wsgi_application,
        "websocket": AuthMiddlewareStack
        (
            URLRouter(
                # api.routing.websocket_urlpatterns,
                channels_backend.routing.websocket_urlpatterns
            )
        )
    }
)