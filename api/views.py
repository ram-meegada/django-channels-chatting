from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from .serializers import *
from rest_framework import status
import string, random, json
from api.utils import get_all_chats
from api.tasks import *
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
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
import json
import io
from io import BytesIO
from reportlab.pdfgen import canvas
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer
from firebase_admin.messaging import Message, Notification
from pyfcm import FCMNotification
from rest_framework.throttling import UserRateThrottle
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from datetime import datetime, time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from api.utils import *
from django.test import TestCase
# from api.models import SaveCsvFileModel
# from .models import QuestionModel
from api.models import *
import logging
from django.db import transaction
import threading

logger = logging.getLogger(__name__)

AWS_ACCESS_KEY_ID = 'AKIATJK2JOPO73GBMCWR'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'backendbucket1101'
AWS_S3_REGION_NAME = 'eu-north-1'
import boto3

class MediaView(APIView):
    def post(self, request):
        print(222222222222222222)
        s3 = boto3.client("s3", region_name = AWS_S3_REGION_NAME)
        media = dict(request.data)['media'][0]
        print(media,'-----')
        print(media.name)
        print(media.size)
        print(media.content_type)
        try:
            s3.upload_fileobj(media, 
                            AWS_STORAGE_BUCKET_NAME, 
                            media.name) 
                            # ExtraArgs = {"ACL": "public-read", "ContentType": media.content_type})
            s3_location = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.eu-north-1.amazonaws.com/{media.name}"
            print(s3_location)
            media_obj = UploadMedia()
            media_obj.media_file_url = s3_location
            media_obj.media_file_name = media.name
            media_obj.file_type = media.content_type
            media_obj.save()
            return Response({"data":"", "status": 200})
        except Exception as error:
            return Response({"data": str(error), "status": 400})

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
    
class CreateQuestion(TemplateView):
    template_name = "question.html"
    def post(self, request):
        create_question = QuestionModel.objects.create(question = request.POST["question"])
        return HttpResponse("question is created succesfully")
    
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
            return HttpResponseRedirect(reverse('login2'))
        logged_in_user = User.objects.get(email=request.user.email)
        sender = logged_in_user.first_name
        try:
            room = OneToOneChatRoomModel.objects.get(room_name=f'chat_{user1}_{user2}')
            all_messages = SaveChatOneToOneRoomModel.objects.filter(room_id = room.id)
        except:
            pass
        return render(request, self.template_name, locals())
        
class DisplayAllchats(TemplateView):
    permission_classes = [IsAuthenticated]
    template_name = "all_chats.html"
    def get(self, request):
        print(request.user, '--------------------')
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
        print('-----------------')
        start = datetime.now()
        password = request.data['password']
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            x = serializer.save()
            x.set_password(password)
            x.save()
            # send_html_mail('this is subject', 'this is content', [request.data["email"]])
            end = datetime.now()
            return Response({'data':serializer.data, 'time-taken': end-start})
        return Response({"data":serializer.errors})

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer  # Import your UserSerializer


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
        print(request.session.get('counter'), '-------------request.session.get(counter)--------------')
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            if user.role_of_user == "2":
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
    
class GetAllUsersView(APIView):
    def get(self, request):
        print(request.session.get('counter'), '-----------------request.session.get(counter)---------')
        all_users = User.objects.all().values('first_name', 'email')
        return Response({'data': all_users, 'message':'all user details'})    
    
class GetAllQueuedChatsToAdminView(TemplateView):
    template_name = "all_queued_sessions.html"
    def get(self, request):
        print(request.user.first_name, '---------------sdasdad--------------')
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login2'))
        try:
            user = User.objects.get(email=request.user)
        except:
            return HttpResponse('NO USER FOUND==================')    
        if user.role_of_user == '1':
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
            # send_user_notification(user=user_obj, payload=payload, ttl=1000)
            print('push notification is implemented-----------------+++++++++++++++')
            return render(request, self.template_name, locals())
        return HttpResponseRedirect(reverse('login2'))


# class GeneratePDF(APIView):
#     def post(self, request):
#         json_data = request.data
#         # Create a PDF response
#         response = FileResponse(self.create_pdf(json_data))
#         response['Content-Type'] = 'application/pdf'
#         response['Content-Disposition'] = 'inline; filename="output.pdf"'
#         return response

#     def create_pdf(self, json_data):
#         # Create a PDF document
#         buffer = BytesIO()
#         c = canvas.Canvas(buffer, pagesize=letter)

#         # Load JSON data and draw it on the PDF
#         c.drawString(100, 750, "JSON Data:")
#         for key, value in json_data.items():
#             c.drawString(100, 750, f"{key}: {value}")

#         # Save the PDF
#         c.showPage()
#         c.save()

#         # Move the buffer's cursor to the beginning
#         buffer.seek(0)
#         return buffer

# class PDFGenerateView(APIView):
#     def post(self, request):
#         json_data = request.data
#         # Create a PDF response
#         # response = FileResponse(self.create_pdf(json_data))
#         # response['Content-Type'] = 'application/pdf'
#         # response['Content-Disposition'] = 'inline; filename="output.pdf"'
#         response = self.create_pdf(json_data)
#         return response
#     def create_pdf(self, json_data):
#         buffer = io.BytesIO()
#         p = canvas.Canvas(buffer)
#         y = 800
#         for i,j in json_data.items():
#             p.drawString(50, y, f"{i}:- {j}")
#             y -= 20
#         p.showPage()
#         p.save()
#         buffer.seek(0)
#         print(buffer, '-----------------buffer content---------------')
#         with open('new.pdf', 'wb') as file:
#             file.write(buffer.read())
#         return FileResponse(buffer, as_attachment=True)
    

class GeneratescidQrcode(APIView):
    def post(self, request):
        obj = ScidModel.objects.create(scid = request.data['scid'])
        return Response({'data':'done'})
    
class CheckPushNotificationView(APIView):
    def post(self, request):
        # push_service = FCMNotification(api_key="AAAAsxujhoE:APA91bGgl9ncVQfQB6uNOhgnxDY-mFCeVLSv4BgSBLhxiNeHL2TFykIzl0N44O68uOIC-rxL1ni7oVAK3j3hAUXXXzf-Hn6E40byMG2f1mNXzm-3WVp3t0ZDNXLZvOfcfCMO4wAG4NrR")
        push_service = FCMNotification(api_key="AAAAQWx5X2Y:APA91bGkQC9y-vJ1-vi1itciZoDbS0HRO6poPv-gjowD2dMjqAd1FrZnzcHXMo6Du5K1CuAHDF1w05XbwJtulKXOaQwJ3REZizCYuIeABBGkG7-xpuls0lACd9UoXNs1PhW7JxRk1DX7")
        # Send the notification
        result = push_service.notify_single_device(
        registration_id="c5Hcm35JFDkKw2znKunEPy:APA91bFnZ5O6un_phJ8W2Rl5mwNht3nJxRSitpWT6kM49OcVGzdWJHSvnjTQY-5G97A8oQmpxOfPCnKZtFpxwm1tW5gU2OKIxgbuvlA7DC9O-SrDmVZ5aIAfZNprRfjiOcyaeNbwU4vh",
        message_title="message title",
        message_body="working!!!!!!!!!!!!!!",
        )
        return Response({"data":"done"})

        
class TestingPurposeView(APIView):
    # throttle_classes = [UserRateThrottle]
    def get(self, request):
        start_time = datetime.now()
        # users = cache.get('users')
        # if users is None:
        users = "hello"
            # x = add.delay(11,15)
            # cache.set("users", users, timeout=30)
        end_time = datetime.now()
        return Response({"data": users, "message": "random number", "code":200, "time-taken": end_time-start_time})

class SendMailsAsynchronouslyView(APIView):
    def get(self, request):
        try:
            lst = ["kane9014@yopmail.com"]
            start_time = datetime.now()    
            send_html_mail('this is a subject', 'this is asynchronous testing mail22222', lst)
            end_time = datetime.now()
            return Response({'time_taken':str(end_time-start_time), 'message':'message sent successfully'})
        except:
            return Response({'data':None, 'message':'something went wrong'})
        
class SendMailToRecipients(APIView):
    def get(self, request):
        start_time = datetime.now()
        recipient_list = ["kane9014@yopmail.com"]
        context = {'subject': 'this is subbbb', 'html_content':'smfkmfls'}
        temp = render_to_string('send_mul_mails.html', context)
        msg = EmailMultiAlternatives(f"this is for testing purpose", temp, settings.DEFAULT_FROM_EMAIL, recipient_list)
        msg.content_subtype = 'html'
        msg.send()        
        end_time = datetime.now()
        return Response({'time_taken':str(end_time-start_time), 'message':'message sent successfully'})
    
import pandas as pd    
class SaveCsvFileView(APIView):
    def post(self, request):
        file = request.FILES.get('csv_file')
        content = pd.read_csv(file)
        df_no_duplicates = content.drop_duplicates()
        file_path = f"/home/apptunix/Desktop/ram_projects/django-project/django-channels-chatting/media/csv_files/random.csv"
        df_no_duplicates.to_csv(file_path)
        save_obj = SaveCsvFileModel.objects.create(csv_file = f"file_save.csv")
        return Response({"data":None, "message":"done"})
    
class GetCsvFileView(APIView):
    def get(self, request):
        get_obj = SaveCsvFileModel.objects.last()
        print(get_obj.csv_file.path, '-------------get_obj.csv_file.path------------')
        with open(get_obj.csv_file.path, 'r') as file:
            content = pd.read_csv(file)
        return Response({"data":content, "message":"done"})

class SendMailCeleryView(APIView):
    def get(self, request):
        print('------------send0000000000000')
        # send_apikey_to_mail.delay("stefenwarner13@yopmail.com")
        add_task.apply_async(args=[1, 2])
        return Response({"data":"None", "message":"done"})

import ast
class ReadCsvView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            if 'csv_file' not in request.FILES:
                raise ValueError("CSV file is missing in the request.")
            file = request.FILES['csv_file']
            content = pd.read_excel(file, engine='openpyxl')
            df_no_duplicates = content.drop_duplicates()
            df_no_duplicates.rename(columns={"MORTGAGE LENDER": "lender_id"}, inplace=True)
            df_no_duplicates.rename(columns={"BORROWER": "borrower_id"}, inplace=True)
            df_no_duplicates.rename(columns={"COLLATERAL TYPE": "collateral_type_id"}, inplace=True)
            df_no_duplicates.rename(columns={"ORIG. LOAN AMOUNT": "loan_amount"}, inplace=True)
            df_no_duplicates.rename(columns={"ORIGINATION DATE": "origination_date"}, inplace=True)
            df_no_duplicates.rename(columns={"MATURITY DATE": "maturity_date"}, inplace=True)
            df_no_duplicates.rename(columns={"ADDRESS": "street_address"}, inplace=True)
            df_no_duplicates.rename(columns={"CITY": "city"}, inplace=True)
            df_no_duplicates.rename(columns={"STATE": "state_id"}, inplace=True)
            df_no_duplicates.rename(columns={"COUNTY": "county"}, inplace=True)

            df_no_duplicates['loan_amount'] = df_no_duplicates['loan_amount'].replace('[\$,]', '', regex=True).astype(float)
            borrower_data = df_no_duplicates[['borrower_id']].to_dict(orient='records')
            county = df_no_duplicates[['county']].to_dict(orient='records')
            mortgage_lender_data = df_no_duplicates[['lender_id']].to_dict(orient='records')
            state_data = df_no_duplicates[['state_id']].to_dict(orient='records')
            collateral_data = df_no_duplicates[['collateral_type_id']].to_dict(orient='records')
            df_no_duplicates['origination_date'] = pd.to_datetime(df_no_duplicates['origination_date'], format='%d/%m/%y', errors='coerce')
            df_no_duplicates['origination_date'] = pd.to_datetime(df_no_duplicates['origination_date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d %H:%M:%S.%f%z').fillna('1970-01-01 00:00:00.000000+0000')
            df_no_duplicates['maturity_date'] = pd.to_datetime(df_no_duplicates['maturity_date'], format='%d/%m/%y', errors='coerce')
            df_no_duplicates['maturity_date'] = pd.to_datetime(df_no_duplicates['maturity_date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d %H:%M:%S.%f%z').fillna('2050-01-01 00:00:00.000000+0000')
            commercial_real_estate_data = df_no_duplicates.to_dict(orient='records')

            read_csv_task.apply_async(args = [commercial_real_estate_data, borrower_data, state_data, mortgage_lender_data, collateral_data])
            return Response({"data": None, "message": "done"})
        except Exception as error:    
            return Response({"data": None, "message": str(error)})
        
# class ThreadTestingView(APIView):
#     def get(self, request):
#         borrowers_thread = CustomThread("get_borrowers")
#         lenders_thread = CustomThread("get_lenders")
#         borrowers_thread.start()
#         lenders_thread.start()
#         borrowers_thread.join()
#         lenders_thread.join()
#         print(borrowers_thread.result, '------------borrowers---------------')
#         print(lenders_thread.result)
#         return Response({"data":None, "message":"done"})

class ThreadTestingView(APIView):
    def get(self, request):
        borrowers = Borrowers.objects.all()
        lenders = MortgageLender.objects.all()
        print(borrowers)
        print(lenders)
        return Response({"data":None, "message":"done"})
    
class CloneReadCsvView(APIView):
    def post(self, request, format=None):
        try:
            first_start_time = datetime.now()
            # Check if 'csv_file' is present in the request.FILES
            if 'csv_file' not in request.FILES:
                raise ValueError("CSV file is missing in the request.")

            file = request.FILES['csv_file']
            content = pd.read_excel(file, engine='openpyxl')
            df_no_duplicates = content.drop_duplicates()
            df_no_duplicates.rename(columns={"MORTGAGE LENDER": "lender"}, inplace=True)
            df_no_duplicates.rename(columns={"BORROWER": "borrower"}, inplace=True)
            df_no_duplicates.rename(columns={"COLLATERAL TYPE": "collateral_type"}, inplace=True)
            df_no_duplicates.rename(columns={"ORIG. LOAN AMOUNT": "loan_amount"}, inplace=True)
            df_no_duplicates.rename(columns={"ORIGINATION DATE": "origination_date"}, inplace=True)
            df_no_duplicates.rename(columns={"MATURITY DATE": "maturity_date"}, inplace=True)
            df_no_duplicates.rename(columns={"ADDRESS": "street_address"}, inplace=True)
            df_no_duplicates.rename(columns={"CITY": "city"}, inplace=True)
            df_no_duplicates.rename(columns={"STATE": "state"}, inplace=True)
            df_no_duplicates.rename(columns={"COUNTY": "county"}, inplace=True)

            df_no_duplicates['loan_amount'] = df_no_duplicates['loan_amount'].replace('[\$,]', '', regex=True).astype(float)
            borrower_data = df_no_duplicates[['borrower']].to_dict(orient='records')
            county = df_no_duplicates[['county']].to_dict(orient='records')
            mortgage_lender_data = df_no_duplicates[['lender']].to_dict(orient='records')
            state_data = df_no_duplicates[['state']].to_dict(orient='records')
            collateral_data = df_no_duplicates[['collateral_type']].to_dict(orient='records')
            df_no_duplicates['origination_date'] = pd.to_datetime(df_no_duplicates['origination_date'], format='%d/%m/%y', errors='coerce')
            df_no_duplicates['origination_date'] = pd.to_datetime(df_no_duplicates['origination_date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d %H:%M:%S.%f%z').fillna('1970-01-01 00:00:00.000000+0000')
            df_no_duplicates['maturity_date'] = pd.to_datetime(df_no_duplicates['maturity_date'], format='%d/%m/%y', errors='coerce')
            df_no_duplicates['maturity_date'] = pd.to_datetime(df_no_duplicates['maturity_date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d %H:%M:%S.%f%z').fillna('2050-01-01 00:00:00.000000+0000')
            # print(borrower_data, type(borrower_data), "------borrower_data-----borrower_data--------------")
            print(datetime.now()- first_start_time, '================fiirst time taken=============')
            # with transaction.atomic():
            #     state_time = datetime.now()
            #     existing_borrowers = set(Borrowers.objects.values_list('borrower', flat=True))
            #     result_records = []
            #     for i in borrower_data:
            #         if i not in result_records:
            #             result_records.append(i)
            #     new_borrower_instances = [Borrowers(borrower=data['borrower_id']) for data in result_records if data['borrower_id'] not in existing_borrowers]
            #     borrower_instances = Borrowers.objects.bulk_create(new_borrower_instances, 1000)

            #     existing_states = set(StateRealEstate.objects.values_list('state', flat=True))
            #     state_result_records = []
            #     for i in state_data:
            #         if i not in state_result_records:
            #             state_result_records.append(i)
            #     new_state_instances = [StateRealEstate(state=data['state_id']) for data in state_result_records if data['state_id'] not in existing_states]
            #     state_instances = StateRealEstate.objects.bulk_create(new_state_instances, 1000)
                
            #     existing_lenders = set(MortgageLender.objects.values_list('lender', flat=True))
            #     lender_result_records = []
            #     for i in mortgage_lender_data:
            #         if i not in lender_result_records:
            #             lender_result_records.append(i)
            #     new_lender_instances = [MortgageLender(lender=data['lender_id']) for data in lender_result_records if data['lender_id'] not in existing_lenders]
            #     print(new_lender_instances, '-------------new_lender_instances-------new_lender_instances-----------')
            #     mortgage_lender_instances = MortgageLender.objects.bulk_create(new_lender_instances, 1000)
                
            #     existing_collaterals = set(CollateralModel.objects.values_list('collateral_type', flat=True))
            #     collateral_result_records = []
            #     for i in collateral_data:
            #         if i not in collateral_result_records:
            #             collateral_result_records.append(i)
            #     new_collateral_instances = [CollateralModel(collateral_type=data['collateral_type_id']) for data in collateral_result_records if data['collateral_type_id'] not in existing_collaterals]
            #     collateral_instances = CollateralModel.objects.bulk_create(new_collateral_instances, 1000)

            #     print(datetime.now()-state_time, '------------time taken----------------')
            # Create Records in CommercialRealEstate
            commercial_real_estate_data = df_no_duplicates.to_dict(orient='records')
            with transaction.atomic():
                starting_time = datetime.now()
                CloneCommercialRealEstate.objects.bulk_create([CloneCommercialRealEstate(**data) for data in commercial_real_estate_data], 1000)
            #     for data in commercial_real_estate_data:
            #         try:
            #             data['borrower_id'] = Borrowers.objects.get(borrower=data['borrower_id']).id
            #         except:
            #             obj = Borrowers.objects.create(borrower=data['borrower_id'])
            #             data['borrower_id'] = obj.id
            #         try:
            #             data['lender_id'] = MortgageLender.objects.get(lender=data['lender_id']).id
            #         except:
            #             obj = MortgageLender.objects.create(lender=data['lender_id'])    
            #             data['lender_id'] = obj.id
            #         state_instance = StateRealEstate.objects.filter(state=data['state_id']).first()

            #         if state_instance:
            #             data['state_id'] = state_instance.id
            #         else:
            #             data['state_id'] = StateRealEstate.objects.create(state=data['state_id']).id
            #         try:    
            #             data['collateral_type_id'] = CollateralModel.objects.get(collateral_type=data['collateral_type_id']).id
            #         except:
            #             data['collateral_type_id'] = CollateralModel.objects.create(collateral_type=data['collateral_type_id']).id    
            #     print(datetime.now() - starting_time, '=====================2nd process time=============')
            # print(datetime.now() - first_start_time, '=====================full process time=============')
            result = {"data": None, "message": "done", "code": status.HTTP_200_OK}
            return Response(result, status=status.HTTP_200_OK)

        except ValueError as ve:
            print(f"ValueError: {ve}")
            result = {"data": None, "message": str(ve)}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            result = {"data": None, "message": "Internal Server Error"}
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateSourceView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.user)
        serializer = CreateSourceSerializer(data = request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GetAllSourceView(APIView):
    def get(self, request):
        sources = SourceModel.objects.all()
        serializer = GetSourceSerializer(sources, many = True)
        return Response(serializer.data)

class GetAllPostsView(APIView):
    def get(self, request):
        sources = Post.objects.all()
        serializer = PostSerializer(sources, many = True)
        return Response(serializer.data)
from api.cron import my_cron_job        
# from background_task import background

class CronTabView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            if 'csv_file' not in request.FILES:
                raise ValueError("CSV file is missing in the request.")
            file = request.FILES['csv_file']
            content = pd.read_excel(file, engine='openpyxl')
            df_no_duplicates = content.drop_duplicates()
            df_no_duplicates.rename(columns={"MORTGAGE LENDER": "lender_id"}, inplace=True)
            df_no_duplicates.rename(columns={"BORROWER": "borrower_id"}, inplace=True)
            df_no_duplicates.rename(columns={"COLLATERAL TYPE": "collateral_type_id"}, inplace=True)
            df_no_duplicates.rename(columns={"ORIG. LOAN AMOUNT": "loan_amount"}, inplace=True)
            df_no_duplicates.rename(columns={"ORIGINATION DATE": "origination_date"}, inplace=True)
            df_no_duplicates.rename(columns={"MATURITY DATE": "maturity_date"}, inplace=True)
            df_no_duplicates.rename(columns={"ADDRESS": "street_address"}, inplace=True)
            df_no_duplicates.rename(columns={"CITY": "city"}, inplace=True)
            df_no_duplicates.rename(columns={"STATE": "state_id"}, inplace=True)
            df_no_duplicates.rename(columns={"COUNTY": "county"}, inplace=True)

            df_no_duplicates['loan_amount'] = df_no_duplicates['loan_amount'].replace('[\$,]', '', regex=True).astype(float)
            borrower_data = df_no_duplicates[['borrower_id']].to_dict(orient='records')
            county = df_no_duplicates[['county']].to_dict(orient='records')
            mortgage_lender_data = df_no_duplicates[['lender_id']].to_dict(orient='records')
            state_data = df_no_duplicates[['state_id']].to_dict(orient='records')
            collateral_data = df_no_duplicates[['collateral_type_id']].to_dict(orient='records')
            df_no_duplicates['origination_date'] = pd.to_datetime(df_no_duplicates['origination_date'], format='%d/%m/%y', errors='coerce')
            df_no_duplicates['origination_date'] = pd.to_datetime(df_no_duplicates['origination_date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d %H:%M:%S.%f%z').fillna('1970-01-01 00:00:00.000000+0000')
            df_no_duplicates['maturity_date'] = pd.to_datetime(df_no_duplicates['maturity_date'], format='%d/%m/%y', errors='coerce')
            df_no_duplicates['maturity_date'] = pd.to_datetime(df_no_duplicates['maturity_date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d %H:%M:%S.%f%z').fillna('2050-01-01 00:00:00.000000+0000')
            commercial_real_estate_data = df_no_duplicates.to_dict(orient='records')

            # read_csv_task.apply_async(args = [commercial_real_estate_data, borrower_data, state_data, mortgage_lender_data, collateral_data])
            # my_cron_job(commercial_real_estate_data, borrower_data, state_data, mortgage_lender_data, collateral_data)
            read_csv_task(commercial_real_estate_data, borrower_data, state_data, mortgage_lender_data, collateral_data)
            return Response({"data": None, "message": "done"})
        except Exception as error:    
            return Response({"data": None, "message": str(error)})
        


from .serializers import *
from .customPagination import CustomPaginationMobileView, CustomPagination         
class GetCreLeadsByPagination(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        print(request.data,"=========req=====data=====")
        cre_obj = CommercialRealEstate.objects.all()
        custom_pagination_obj = CustomPagination()
        search_keys = ['loan_amount__icontains']
        search_type = 'or'

        response = custom_pagination_obj.custom_pagination(request, CommercialRealEstate, search_keys, search_type, CommercialRealEstateSerializer,cre_obj)

        if response['response_object']:
            print(len(response['response_object']), type(response['response_object']), '-----------responseeeeeeeeeee]')
            return Response({"data": response['response_object'], "recordsTotal": len(response['response_object']),"recordsFiltered": response['total_records'],"code": status.HTTP_200_OK, "message": "OK"})
        else:
            return Response({"data": response['response_object'], "recordsTotal": response['total_records'],"recordsFiltered": response['total_records'],"code": status.HTTP_204_NO_CONTENT, "message": "RECORD_NOT_FOUND"})
        
class GetCreLeads(APIView):
    def get(self, request, format=None):
        try:
            print(request.user.id, '-------------request.user.id-----------')
            cre_obj = CommercialRealEstate.objects.all()
            serializer = CommercialRealEstateSerializer(cre_obj, many=True, context={"user_id":request.user.id})
            return Response({"data":serializer.data, "code":status.HTTP_200_OK, "message": "OK"})
        except CommercialRealEstate.DoesNotExist:
            return Response({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message": "BAD_REQUEST"})
        
class GetUserLenders(APIView):    
    permission_classes = (IsAuthenticated, )    
    def get(self, request,format  = None):
        try:
            user_id = request.user.id  # Assuming you have user information in the request
            count_of_lenders = SaveCreLeads.objects.filter(cre_user_id=user_id)
            lender_count = {}
            for i in count_of_lenders:
                if i.cre_lender_id is None:
                    continue
                if i.cre_lender_id not in lender_count:
                    lender_count[i.cre_lender_id] = 1
                else:
                    lender_count[i.cre_lender_id] += 1
            lenders = MortgageLender.objects.filter(id__in=list(lender_count.keys()))
            serializer = MortgagelenderSerializer(lenders, many=True, context={"lender_count": lender_count})
            data = list(serializer.data)
            result = sorted(data, key=lambda v: v["count"], reverse=True)
            return Response({"data": result, "code": status.HTTP_200_OK, "message": "OK"})
        except SaveCreLeads.DoesNotExist:
            return Response({"data": None, "code": status.HTTP_400_BAD_REQUEST, "message": "BAD_REQUEST"})
        
class GetAllBorrowers(APIView):
    permission_classes = (IsAuthenticated, )    
    def get(self, request, format=None):
        try:
            Borrowers_obj = Borrowers.objects.all()
            serializer = BorrowersSizeSerializer(Borrowers_obj, many=True)
            return Response({"data":serializer.data, "code":status.HTTP_200_OK, "message":"OK"})
        except Borrowers.DoesNotExist:
            return Response({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"BAD_REQUEST"})
        
class GetAllLenders(APIView):        
    permission_classes = (IsAuthenticated, )    
    def get(self, request, format=None):
        try:
            lenders_obj = MortgageLender.objects.all()
            serializer = LendersSizeSerializer(lenders_obj, many=True)
            return Response({"data":serializer.data, "code":status.HTTP_200_OK, "message":"OK"})
        except MortgageLender.DoesNotExist:
            return Response({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"BAD_REQUEST"})        
        
class GetCreLeadsById(APIView):        
    def get(self,request,pk,format = None):
        user_id = request.user.id
        try:
            cre_obj = CommercialRealEstate.objects.get(id = pk)
            serializer = CommercialRealEstateSerializer(cre_obj, context = {"user_id":user_id})
            return Response({"data":serializer.data, "code":status.HTTP_200_OK, "message":"OK"})
        except CommercialRealEstate.DoesNotExist:
            return Response({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"BAD_REQUEST"})        
        
class GetLeadDetailsByLenderId(APIView):        
    def get(self,request,lender_id,format = None):
        try:
            print(request.user.id, '--------------------')
            cre_obj = SaveCreLeads.objects.filter(cre_lender_id=lender_id, cre_user_id=request.user)
            print(cre_obj, '-----------------cre-------------')
            serializer = GetCreLeadsSerialzer(cre_obj, many=True)
            return Response({"data":serializer.data, "code":status.HTTP_200_OK, "message":"OK"})
        except SaveCreLeads.DoesNotExist:
            print('-------------came here--------------------')
            return Response({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"BAD_REQUEST"})        
        
class GetbookmarkedCreLeads(APIView):        
    def get(self, request, bookmarked_cre_id):
        print('came here--------get_bookmarked_cre_by_id-----------------')
        try:
            cre_obj = SaveCreLeads.objects.get(id = bookmarked_cre_id)
        except Exception as e:
            print(e, '------eeeeeeeeee')
            return({"data":None, "code":status.HTTP_204_NO_CONTENT, "message":"RECORD_NOT_FOUND"})
        serializer = GetCreLeadSerializer(cre_obj)
        print(serializer.data, '--------------')
        return Response({"data":serializer.data, "code":status.HTTP_200_OK, "message":"OK"})        
    
class GetCreFiltersView(APIView):    
    def post(self,request, format = None):
        queryset = CommercialRealEstate.objects.all()
        filters_data = request.data.get("filters")
        sorting_key = request.data.get("sort_with")
        try:
            search_values = (request.data['search']['value']).strip()
        except:
            search_values = None    
        if filters_data:
            for key, value in filters_data.items():
                print(f"Applying filter: {key} = {value}")
                if key == "loan_amount_start":
                    queryset = queryset.filter(loan_amount__gte=int(value))
                elif key == "loan_amount_end":
                    queryset = queryset.filter(loan_amount__lte=int(value))
                elif key == "origination_date_start":
                    queryset = queryset.filter(origination_date__gte=datetime.strptime(value, "%Y-%m-%d"))
                elif key == "origination_date_end":
                    queryset = queryset.filter(origination_date__lte=datetime.strptime(value, "%Y-%m-%d"))
                elif key == "maturity_date_start":
                    queryset = queryset.filter(maturity_date__gte=datetime.strptime(value, "%Y-%m-%d"))
                elif key == "maturity_date_end":
                    queryset = queryset.filter(maturity_date__lte=datetime.strptime(value, "%Y-%m-%d"))
                elif key == "collateral_type":
                    # queryset = queryset.filter(collateral_type=value)
                    queryset = queryset.filter(collateral_type__collateral_type__icontains = value)
                elif key == "street_address":
                    queryset = queryset.filter(street_address=value)
                elif key == "city":
                    queryset = queryset.filter(city=value)
                elif key == "state":
                    queryset = queryset.filter(state__id=value)
                elif key == "borrower":
                    # queryset = queryset.filter(borrower__id=value)
                    # results = CommercialRealEstate.objects.filter(borrower__borrower__icontains = "rio")
                    queryset = queryset.filter(borrower__borrower__icontains = value)

                elif key == "lender":
                    # queryset = queryset.filter(lender__id=value)
                    # results = CommercialRealEstate.objects.filter(lender__lender__icontains = "rio")
                    queryset = queryset.filter(lender__lender__icontains = value)

                print(f"After {key} filter: {queryset.count()} records")
        if sorting_key:
            if sorting_key == 2:
                queryset = queryset.order_by("-loan_amount")
            elif sorting_key == 3:
                queryset = queryset.order_by("loan_amount")
            elif sorting_key == 4:
                print(datetime.now(), '============datetime.now()============')
                queryset = queryset.filter(maturity_date__gt = datetime.now())
            elif sorting_key == 5:
                print(datetime.now(), '============datetime.now()============')
                queryset = queryset.filter(maturity_date__lt = datetime.now())

        if search_values:
            print(queryset, '=====================queryset===========')
            borrower_name = Borrowers.objects.filter(borrower__icontains = search_values)
            filtered_borrower_list = [i.id for i in borrower_name]
            print(filtered_borrower_list, '----------filtered_borrower_list---------')
            lenders_name = MortgageLender.objects.filter(lender__icontains = search_values)
            filtered_lender_list = [i.id for i in lenders_name]
            if filtered_lender_list:
                queryset = queryset.filter(lender__in = filtered_lender_list)
            elif filtered_borrower_list:    
                queryset = queryset.filter(borrower__in = filtered_borrower_list)
            print(queryset, '========2===========2222222222====')

        custom_pagination_class = CustomPagination() 
        search_keys = ['borrower__borrower__icontains', 'lender__lender__icontains']
        search_type = 'or'

        response = custom_pagination_class.custom_pagination(request, CommercialRealEstate, search_keys, search_type, CommercialRealEstateSerializer,queryset)

        if response['response_object']:
            return Response({"data": response['response_object'], "recordsTotal": len(response['response_object']),"recordsFiltered": response['total_records'],"code": status.HTTP_200_OK, "message": "OK"})
        else:
            return Response({"data": response['response_object'], "recordsTotal": response['total_records'],"recordsFiltered": response['total_records'],"code": status.HTTP_200_OK, "message": "RECORD_NOT_FOUND"})



        
class UploadVideoView(TemplateView):
    template_name = "upload_video.html"
    def post(self, request):
        file = dict(request.FILES)["video_file"][0]
        print(file.name, '--name---')
        print(file.content_type, '--content_type---')
        print(file.size, '---size--')
        up = VideoModel.objects.create(video = file)
        return HttpResponse("this is a response")        
    
class RunVideoView(TemplateView):
    template_name = "run_video.html"
    def get(self, request):
        vid = VideoModel.objects.first()
        return render(request, self.template_name, locals())    
    
class VideoView(APIView):
    def post(self, request):
        print(request.data,'-----')
        print(request.FILES,'-----')
        serializer = VideoSeializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})    
        return Response({"data": serializer.errors})    