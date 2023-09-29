from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import img2pdf 
from PIL import Image 
import os 
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.http import HttpResponse

class ConvertImgToPdfView(APIView):
    def post(self, request):
        print(request.data['image'], '===============request=============')
        buffer = self.convert_img_to_pdf(request.data['image'])
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=output.pdf'
        response.write(buffer.read())
        return response
    def convert_img_to_pdf(self, img_path):
        pdf_path = "C:/home/apptunix/Downloads/"
        img = Image.open(img_path) 
        buffer = io.BytesIO()
        pdf_canvas = canvas.Canvas(buffer, pagesize=img.size)
        pdf_canvas.drawInlineImage(img, 0, 0)
        pdf_canvas.save()
        buffer.seek(0)
        with open('img.pdf', 'wb') as file:
            file.write(buffer.getvalue())
        print("Successfully made pdf file")
        return buffer