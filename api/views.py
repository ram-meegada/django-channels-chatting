from django.shortcuts import render
from .models import User, ChatBotModel, QuestionAndAnswer, SaveChatOneToOneRoomModel, OneToOneChatRoomModel,\
                    SessionIdStoreModel, ChatStorageWithSessionIdModel
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from .serializers import CreateChatbotSerializer, QASerializer, UserSerializer, ChatSerializer
from rest_framework import status
import string, random, json
from api.utils import get_all_chats
from api.tasks import add, send_apikey_to_mail
import ast
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password
from .producer import publish_message
import jwt
from abstractbaseuser_project.settings import SECRET_KEY as secret_key
import base64
# from zeep import Client
# from zeep.transports import Transport
import requests
from django.conf import settings
from webpush import send_user_notification
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
from io import BytesIO

# Create your views here.
class GetAllUsers(APIView):
    def get(self, request):
        users = User.objects.all().values()
        return Response(users)
    
class ChatbotView(TemplateView):
    def get(self, request):
        return render(request, 'homepage.html')
    
class ChannelLayersView(TemplateView):
    def get(self, request, group_name):
        return render(request, 'index.html', context={'groupname':group_name})
    
class CreateChatbot(APIView):
    def post(self, request):
        serializer = CreateChatbotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'data':None})
    
class ApiKeyView(APIView):
    def post(self, request, format=None):
        generated_api_key = self.generate_api_key_func()
        print(generated_api_key, '==============generated_api_key============')
        serializer = CreateChatbotSerializer(data=request.data)
        user_details = User.objects.get(id=request.data['user'])
        print(user_details.email, '============user_details.email======')
        if serializer.is_valid():
            obj = serializer.save()
            obj.api_key = generated_api_key
            obj.save()
            serialized_data = serializer.data
            send_apikey_to_mail.delay(user_details.email, generated_api_key)
            # x = add.apply_async(args=[3, 5])
            print('=================value======================')
            return Response({"data":serialized_data, "code":status.HTTP_200_OK, "message": "Your unique api key is successfully sent your mail"})    
        return Response({"data":serializer.errors, "code":status.HTTP_400_BAD_REQUEST, "message": "Something went wrong. Please try again"})    

    def generate_api_key_func(self):
        characters = list(string.ascii_letters + string.digits)
        key = ''.join(random.choices(characters, weights=None, k=32))
        return key    
    
class UserUploadFileView(APIView):
    def post(self, request):
        user = request.data.get('user_id')
        data_set = request.data.get('user_id')
        pass


class UserAddQuestionView(APIView):
    def post(self, request):
        question = request.data.get('question')
        answer = request.data.get('answer')
        user_id = request.data.get('user_id')
        user_obj = None
        try:
            user_obj = QuestionAndAnswer.objects.get(user_id=user_id)
        except:
            pass
        if user_obj:
            data = ast.literal_eval(user_obj.data_set)
            data.append({f"question":question, "answer":answer})
            user_obj.data_set = data
            user_obj.save()
        elif user_obj is None:
            data = []
            data.append({"question1":question, "answer":answer})
            user_obj = QuestionAndAnswer.objects.create(user_id_id=user_id, data_set=data)    
        return Response({"data":None, "message":"Added succesfully"})
    
class EditQuestionsByUser(APIView):
    def get(self, request):
        user_id = request.data.get('user_id')
        try:
            user_obj = QuestionAndAnswer.objects.get(user_id=user_id)
        except:
            return Response({"data":None, "message":"User not found"})

    def put(self, request):
        question_num = request.data.get('question_number')
        question = request.data.get('question')
        answer = request.data.get('answer')
        user_id = request.data.get('user_id')
        user_obj = None
        try:
            user_obj = QuestionAndAnswer.objects.get(user_id=user_id)
        except:
            return Response({"data":None, "message":"User not found"})
        if user_obj:
            data_set = user_obj.data_set
            data = ast.literal_eval(data_set)
            data[question_num-1] = {"question":question, "answer":answer}
            user_obj.data_set = data
            user_obj.save()
        return Response({"data":None, "message":"Edited succesfully"})
    

class DeleteQuestionsByUser(APIView):
    def delete(self, request):
        question_num = request.data.get('question_number')
        user_id = request.data.get('user_id')
        user_obj = None
        try:
            user_obj = QuestionAndAnswer.objects.get(user_id=user_id)
        except:
            return Response({"data":None, "message":"User not found"})
        if user_obj:
            data = ast.literal_eval(user_obj.data_set)
            del data[question_num-1]
            user_obj.data_set = data
            user_obj.save()
        return Response({"data":None, "message":"deleted succesfully"})
    
    
        
    
    

class CheckingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pass

class LoginUser(TemplateView):
    template_name = 'login.html'
    def post(self,request):
        print('came to post ')
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('all-chats'), locals())
        else:
            messages.error(request, f"the credentials u entered r incorrect")   
            return HttpResponseRedirect(reverse('login'))    

class ChattingView(TemplateView):
    template_name = "homepage.html"
    def get(self, request, user1, user2):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        logged_in_user = User.objects.get(email=request.user)
        sender = logged_in_user.first_name
        try:
            room = OneToOneChatRoomModel.objects.get(room_name=f'chat_{user1}_{user2}')
            all_messages = SaveChatOneToOneRoomModel.objects.filter(room_id = room.id)
        except:
            pass
        return render(request, self.template_name, locals())
        
class DisplayAllchats(TemplateView):
    # permission_classes = [IsAuthenticated]
    template_name = "all_chats.html"
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        user_id = User.objects.get(email=request.user).id
        all_chats = get_all_chats(user_id)
        # data = {'email':user_email, 'all_chats':all_chats}
        return render(request, self.template_name, locals())
    
    
class CheckRabbitMqApi(APIView):
    def get(self, request):
        publish_message("success")
        return Response({'data':None, 'message':'done'})    
    

class RegistrationApi(APIView):
    def post(self, request):
        print(request.data, 'came here=======================')
        password = request.data['password']
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            x = serializer.save()
            x.set_password(password)
            x.save()
            # publish_message('user_created', request.data)
            return Response({'data':serializer.data})
        return Response({"data":serializer.errors})

class UpdateUserAPI(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, id):
        access_token = request.headers['Authorization'].split(' ')[-1] 
        decoded_token = jwt.decode(access_token, key=secret_key, algorithms=['HS256'])
        print(decoded_token, '===============decoded_token===============')
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            x = serializer.save()
            # publish_message('user_details_updated', serializer.data)
            return Response({'data':serializer.data})
        return Response({"data":serializer.errors})

class DeleteUserAPI(APIView):
    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        # publish_message('user_deleted', {"id":id})
        return Response({'data':None})
    
class LoginApiView(APIView):
    def post(self, request):
        email = request.data['email']
        password= request.data['password']
        try:
            print('came here')
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

class GetUserByIdView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({'data':None, 'status':status.HTTP_404_NOT_FOUND})    
        serializer = UserSerializer(user)
        # publish_message(serializer.data)
        return Response({'data':serializer.data, 'status':status.HTTP_200_OK})

class IsAdminUserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({'data':None, 'status':status.HTTP_404_NOT_FOUND})    
        if user.is_superuser:
            return Response({'data':None, 'status':status.HTTP_200_OK})
        return Response({'data':None, 'status':status.HTTP_403_FORBIDDEN})
    


    
class LoginUser2(TemplateView):
    template_name = 'login.html'
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            print(user, user.role_of_user, user.id, '=============user=============--------------')
            login(request, user)
            if user.role_of_user == "2":
                print(22222222222222222, user.id)
                return HttpResponseRedirect(reverse('customer_all_chats', args=[user.id]))
            elif user.role_of_user == "3":
                return HttpResponseRedirect(reverse('agentallcustomerchats'))
            elif user.role_of_user == "1":
                return HttpResponseRedirect(reverse('queuedsession'))
        else:
            messages.error(request, f"the credentials u entered r incorrect")   
            return HttpResponseRedirect(reverse('login2'))    

class LoginAgent(TemplateView):
    template_name = 'login.html'
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('agentallcustomerchats'))
        else:
            messages.error(request, f"the credentials u entered r incorrect")   
            return HttpResponseRedirect(reverse('login2'))    

class LogoutUser(TemplateView):    
    def get(self, request):
        logout(request)
        return render(request, 'logout.html')

class LogoutAgentUser(TemplateView):    
    def get(self, request):
        logout(request)
        return render(request, 'logout.html')
    
class GetAllQueuedChatsToAdminView(TemplateView):
    template_name = "all_queued_sessions.html"
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login2'))
        try:
            user = User.objects.get(email=request.user)
        except:
            return HttpResponse('NO USER FOUND==================')    
        if user.is_superuser:
            queued_sessions = SessionIdStoreModel.objects.filter(is_queued=True)
            all_agents = User.objects.filter(role_of_user='3')
            return render(request, self.template_name, locals())
        else:
            return HttpResponse('no access')
        
class AdminAssignAgentToUserSessionView(TemplateView):
    template_name = "all_queued_sessions.html"
    def get(self, request, session, user):
        if request.user.is_authenticated and request.user.role_of_user == '1':
            get_user = User.objects.get(email=user).id
            get_session = SessionIdStoreModel.objects.get(session_id=session)
            get_session.agent_id = get_user
            get_session.is_queued = False
            get_session.save()
            return HttpResponseRedirect(reverse('queuedsession'))    
        return HttpResponseRedirect(reverse('login2'))

class AgentAllCustomerChatsView(TemplateView):    
    template_name = "agent_all_chats.html"
    def get(self, request):
        if request.user.is_authenticated and request.user.role_of_user == '3':
            all_agent_chats = SessionIdStoreModel.objects.filter(agent_id=request.user.id, is_queued=False, is_resolved=False)
            user = request.user.first_name
            return render(request, self.template_name, locals())
        return HttpResponseRedirect(reverse('login2'))

class CreateNewSessionForUserView(TemplateView):
    template_name = "notification.html"
    def get(self, request, user_id):
        username_in_chatting = request.user.first_name
        session_id = self.create_session_id()
        print(session_id, '--------------create_session_for_customer------------------')
        save_session_of_customer = SessionIdStoreModel.objects.create(session_id=session_id, user_id=user_id)
        print(save_session_of_customer.session_id, '--------------------------------save_session_of_customer=======================')
        return HttpResponseRedirect(reverse('notification', args=[user_id, session_id]))

    def create_session_id(self):
        id = base64.b64encode(str(random.randint(100000, 999999)).encode()).decode()
        return id
    
class ChatWithChatbotAndAgentView(TemplateView):
    template_name = "notification.html"
    def get(self, request, user_id, session_id):
        print(request.user, '-------------request.user---------')

        if request.user.is_authenticated and (request.user.id == user_id or request.user.role_of_user == '3'):
            profile_picture = request.user.profile_picture
            print(profile_picture, '------------profile_pictureprofile_pictureprofile_picture-------------')
            get_session_foreign_key = SessionIdStoreModel.objects.get(session_id=session_id)
            get_chat_of_customer_session = ChatStorageWithSessionIdModel.objects.filter(session_id=get_session_foreign_key).values('user_input')
            username_in_chatting = request.user.first_name
            return render(request, self.template_name, locals())
        return HttpResponseRedirect(reverse('login2'))

class GetAllCustomerChatsView(TemplateView):
    template_name = "customerConversations.html"
    def get(self, request, user_id):
        if request.user.is_authenticated and request.user.role_of_user == '2':
            all_user_sessions = SessionIdStoreModel.objects.filter(user_id=user_id)[::-1]
            user = request.user.id
            payload = {'head': request.user.email, 'body': 'your chats fetcheded successfully'}
            user_obj = get_object_or_404(User, pk=request.user.id)
            send_user_notification(user=user_obj, payload=payload, ttl=1000)
            print('push notification is implemented-----------------+++++++++++++++')
            return render(request, self.template_name, locals())
        return HttpResponseRedirect(reverse('login2'))


class GeneratePDF(APIView):
    def post(self, request):
        json_data = request.data
        # Create a PDF response
        response = FileResponse(self.create_pdf(json_data))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline; filename="output.pdf"'
        return response

    def create_pdf(self, json_data):
        # Create a PDF document
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)

        # Load JSON data and draw it on the PDF
        c.drawString(100, 750, "JSON Data:")
        for key, value in json_data.items():
            c.drawString(100, 750, f"{key}: {value}")

        # Save the PDF
        c.showPage()
        c.save()

        # Move the buffer's cursor to the beginning
        buffer.seek(0)
        return buffer
