from django.shortcuts import render
from api.models import ChatBotModel, GroupModel, SessionIdStoreModel, ChatStorageWithSessionIdModel, OneToOneChatRoomModel, SaveChatOneToOneRoomModel, User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework import status
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import random, base64
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password
from .serializers import GetAllUserSessionsSerializer, GetAllQueuedSessionsSerializer, ChatStorageSerializer

class GetAllQueuedChatsToAdminView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.role_of_user == '1':
            queued_sessions = SessionIdStoreModel.objects.filter(is_queued=True)
            all_agents = User.objects.filter(role_of_user='3')
            serializer = GetAllQueuedSessionsSerializer(queued_sessions, many=True)
            return Response({'data':serializer.data, 'message':'all queued sessions', 'status': status.HTTP_200_OK})
        else:
            return Response({'data':None, 'message':'you dont have access', 'status': status.HTTP_403_FORBIDDEN})
        
class AdminAssignAgentToUserSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, session):
        if request.user.role_of_user == '1':
            get_session = SessionIdStoreModel.objects.get(session_id=session)
            get_session.agent_id = request.data.get('agent_id')
            get_session.is_queued = False
            get_session.is_assigned = True
            get_session.save()
            return Response({'data':None, 'message':'agent assigned successfully', 'status': status.HTTP_200_OK})    
        return Response({'data':None, 'message':'you dont have access', 'status': status.HTTP_403_FORBIDDEN})

class AgentAllCustomerChatsView(APIView):  
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        if request.user.role_of_user == '3':
            all_agent_chats = SessionIdStoreModel.objects.filter(agent_id=request.user.id, is_queued=False, is_resolved=False)
            serializer = GetAllUserSessionsSerializer(all_agent_chats, many=True)
            user = request.user.first_name
            return Response({'data':serializer.data, 'message':'Your assigned chats', 'status': status.HTTP_200_OK})
        return HttpResponseRedirect(reverse('login2'))

class CreateNewSessionForUserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, chatbot_id):
        existing_conversations = SessionIdStoreModel.objects.filter(chatbot_id=chatbot_id, is_resolved=False)
        print(existing_conversations, 'existing_conversations------------------==============')
        for i in existing_conversations: 
            i.is_resolved=True 
            i.save()
        session_id = self.create_session_id()
        save_session_of_customer = SessionIdStoreModel.objects.create(chatbot_id=chatbot_id, session_id=session_id, user_id=request.user.id)
        return Response({'data':{"session_id":session_id}, 'message':'session successfully created'})

    def create_session_id(self):
        id = base64.b64encode(str(random.randint(100000, 999999)).encode()).decode()
        return id
    
class ChatWithChatbotAndAgentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, session_id):
        obj = SessionIdStoreModel.objects.filter(session_id = session_id)[0]
        if obj.agent is None: agent = 0 
        else: agent = obj.agent.id
        if obj.user_id == request.user.id or request.user.id == agent:
            get_session_foreign_key = SessionIdStoreModel.objects.get(session_id=session_id)
            get_chat_of_customer_session = ChatStorageWithSessionIdModel.objects.filter(session_id=get_session_foreign_key).values('user_input')
            username_in_chatting = request.user.first_name
            # apikey = (obj.chatbot.production_api_key).split('prod_')[1]
            return Response({
                'websocket_url':f"ws://127.0.0.1:8000/ws/openaiagentuser/{ request.user.id }/{ session_id }/",
                'username_in_chatting': f'{username_in_chatting}',
                'previous_chat_of_customer_session': f'{get_chat_of_customer_session}'
                })
        return Response({'data':None, 'message':'something went wrong'})

class GetAllCustomerChatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user, '======================resquest.user================')
        if request.user.role_of_user == '2':
            all_user_sessions = SessionIdStoreModel.objects.filter(user_id=request.user.id).order_by('-created_at')
            print(all_user_sessions, '---------------------allusersessions----------------')
            serializer = GetAllUserSessionsSerializer(all_user_sessions, many=True)
            # user = request.user.id
            # payload = {'head': request.user.email, 'body': 'your chats fetcheded successfully'}
            # user_obj = get_object_or_404(User, pk=request.user.id)
            # send_user_notification(user=user_obj, payload=payload, ttl=1000)
            # print('push notification is implemented-----------------+++++++++++++++')
            return Response({'data':serializer.data, 'message':'successfuly', 'status':status.HTTP_200_OK})
        return Response({'data':None, 'message':'NO ACCESS', 'status':status.HTTP_403_FORBIDDEN})

class GetAllUsersView(APIView):
    def get(self, request):
        all_users = User.objects.all().values('id', 'first_name', 'email')
        return Response({'data': all_users, 'message':'all user details'}) 
    
class LoginUser(APIView):
    def post(self, request):
        email = request.data['email']
        password= request.data['password']
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            data = {"user":"some error"}
            return Response(data)   
        chk_pwd = check_password(password, user.password)
        if chk_pwd:
            token = RefreshToken.for_user(user)
            data = {"user":user.email,"access_token":str(token.access_token),"refresh_token":str(token)}
            return Response({"data":data})
        else:
            data = {"user":user.email,'message':"wrong password"}
            return Response(data)    
        
class DisplayPreviousChatsView(APIView):
    def get(self, request, session):
        session_id = get_object_or_404(SessionIdStoreModel, session_id=session)
        print(session_id, '----------------session------------')
        all_chats = ChatStorageWithSessionIdModel.objects.all().order_by('timestamp')
        serializer = ChatStorageSerializer(all_chats, many=True)
        return Response({"data":serializer.data,'message':"all chats of this session"})