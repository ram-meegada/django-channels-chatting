from django.urls import path
from . import consumers
from .consumers import *

websocket_urlpatterns = [
    path('ws/agentuserchatting/<int:user_id>/<str:session>/', AgentChatbotUserChatting.as_asgi()),
]