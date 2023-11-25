from . import views
from django.urls import path 
from imagetopdf.views import *

urlpatterns = [
    path('img-to-pdf/', ConvertImgToPdfView.as_view()),
    path('get-pdf/<int:pdf_id>/', GetPdfByIdView.as_view(), name='GetPdfById'),
    path('download/pdf/<int:pdf_id>/', DownloadPdfFileView.as_view(), name="downloadpdf")
]