from . import views
from django.urls import path 
from .views import *

urlpatterns = [
    path('users/', GetAllUsers.as_view()),
    path('chatbot/', ChatbotView.as_view(),name='homepage'),

    ###################
    path('login/', LoginUser.as_view(), name='login'),
    path('user/all-chats/', DisplayAllchats.as_view(), name='all-chats'),
    path('user/checking/', CheckingView.as_view(), name='checking'),

    path('client/create-chatbot/', CreateChatbot.as_view()),
    path('channel-layers/<str:group_name>/', ChannelLayersView.as_view()),

    path('user/generate-key/', ApiKeyView.as_view()),
    path('user/upload-file/', UserUploadFileView.as_view()),
    path('user/create-question/', UserAddQuestionView.as_view()),
    path('user/update-question/', EditQuestionsByUser.as_view()),
    path('user/delete-question/', DeleteQuestionsByUser.as_view()),
    path('login2/', LoginUser2.as_view(), name='login2'),
    path('loginagent/', LoginAgent.as_view(), name='loginagent'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('agent/logout/', LogoutAgentUser.as_view(), name='logoutagent'),

    path('checking/', CheckRabbitMqApi.as_view(), name='checking'),
    path('registration/', RegistrationApi.as_view(), name='registration'),
    path('user/update/<int:id>/', UpdateUserAPI.as_view(), name='UpdateUser'),
    path('user/delete/<int:id>/', DeleteUserAPI.as_view(), name='DeleteUser'),
    
    path('user/login/', LoginApiView.as_view(), name='loginapiview'),
    path('user/<int:user_id>/', GetUserByIdView.as_view(), name='user_detail'),
    path('admin-user/<int:user_id>/', IsAdminUserView.as_view(), name='isadmin'),


    path('user/chatting/<int:user1>/<int:user2>/', ChattingView.as_view(), name='chatting'),


    path('user/create-new-session/<int:user_id>/', CreateNewSessionForUserView.as_view(), name='create_new_session'),
    path('user/all-chat-sessions/<int:user_id>/', GetAllCustomerChatsView.as_view(), name='customer_all_chats'),


    path('user/chat-with-chatbot/<int:user_id>/<str:session_id>/', ChatWithChatbotAndAgentView.as_view(), name='notification'),
    path('queued-session-chats/', GetAllQueuedChatsToAdminView.as_view(), name='queuedsession'),
    path('assign-agent-to-user-session/<str:session>/<str:user>/', AdminAssignAgentToUserSessionView.as_view(), name='assignagent'),
    path('agent/all-customer-chats/', AgentAllCustomerChatsView.as_view(), name="agentallcustomerchats"),
]