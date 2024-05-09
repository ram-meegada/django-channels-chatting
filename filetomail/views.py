from django.shortcuts import render
from rest_framework.views import APIView
from api.models import User
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from abstractbaseuser_project import settings
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from filetomail.utils import send_image_to_mail, send_pdf_to_mail
# from api.models import ImgToPdfModel
import os


class ImageSendToMailView(APIView):
    def get(self, request):
        user_profile = User.objects.get(id=2)
        print(user_profile.profile_picture.url, '---------user_profile.profile_picture.url---------')
        send_image_to_mail(user_profile.profile_picture.url, user_profile.first_name)
        return Response({"data":None, "message":"done"})

class PdfSendToMailView(APIView):
    def get(self, request):
        pdf_file = request.data.get("pdf")
        user = ImgToPdfModel.objects.get(user_id=2)
        pdf_path = f"{os.getcwd()}/media/{str(user.pdf_file)}"
        for i in range(len(pdf_path)-1, -1, -1):
            if pdf_path[i] == '/':
                pdf_loc = pdf_path[:i]
                pdf_name = pdf_path[i+1:].split('.')[-2]
                break
        send_pdf_to_mail(pdf_loc, pdf_name)
        return Response({"data":str(user.pdf_file), "message":"retreived"})   