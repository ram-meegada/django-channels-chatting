from django.urls import path
from . import consumers
from .consumers import *

websocket_urlpatterns = [
    path('ws/sc/<str:groupname>/', MySyncConsumer.as_asgi()),
    # path('ws/ac/', MyAsyncWebsocketConsumer.as_asgi()),

    path('ws/chatbot/<str:key>/', MyChatBot.as_asgi()),
    path('ws/sync-chatbot/<str:key>/', MySyncChatBot.as_asgi()),

    path('ws/async-we-chatbot/<str:key>/', MyAsyncWebsocketConsumer.as_asgi()),
    #########################
    path('ws/chatting/<int:user1>/<int:user2>/', UserChattingWithFriendConsumer.as_asgi()),


    path('ws/agentuserchatting/<int:user_id>/<str:key>/<str:session>/', AgentChatbotUserChatting.as_asgi()),

    path('ws/chat/<int:id>/', ReactChatIntegrationConsumer.as_asgi()),

]
