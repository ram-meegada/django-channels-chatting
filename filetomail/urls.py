from . import views
from django.urls import path 
from filetomail.views import *

urlpatterns = [
    path('img-to-mail/', ImageSendToMailView.as_view(), name="imgtomail"),
    path('pdf-to-mail/', PdfSendToMailView.as_view(), name="pdftomail")
]