from . import views
from django.urls import path 
from .views import *

urlpatterns = [
    path('get-all-users/', GetAllUsersView.as_view(), name='getallusers2'),
    path('login/', LoginUser.as_view(), name='login22'),

    
    path('user/all-chat-sessions/', GetAllCustomerChatsView.as_view(), name='customer_all_chats2'),
    path('user/create-new-session/<int:chatbot_id>/', CreateNewSessionForUserView.as_view(), name='create_new_session2'),
    path('user/chat-with-chatbot/<str:session_id>/', ChatWithChatbotAndAgentView.as_view(), name='notification2'),
    path('queued-session-chats/', GetAllQueuedChatsToAdminView.as_view(), name='queuedsession2'),
    path('assign-agent-to-user-session/<str:session>/', AdminAssignAgentToUserSessionView.as_view(), name='assignagent2'),

    path('agent/all-customer-chats/', AgentAllCustomerChatsView.as_view(), name="agentallcustomerchats2"),
    path('display-previous-chats/<str:session>/', DisplayPreviousChatsView.as_view(), name='displayoldchats'),
]