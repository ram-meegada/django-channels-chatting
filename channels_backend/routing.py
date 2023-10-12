from django.urls import path
from . import consumers
from .consumers import *

websocket_urlpatterns = [
    path('ws/agentuserchatting/<int:user_id>/<str:session>/', AgentChatbotUserChatting.as_asgi()),
    path('ws/openaiagentuser/<int:user_id>/<str:session>/', UserChattingWithOpenAIAgent.as_asgi()),
    path('ws/basicbot-agent-user/<int:user_id>/<str:session>/', UserChattingWithBasicBotAgent.as_asgi()),
]