from . import views
from django.urls import path 
from imagetopdf.views import *

urlpatterns = [
    path('img-to-pdf/', ConvertImgToPdfView.as_view())
]