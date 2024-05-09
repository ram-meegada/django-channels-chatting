from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from api.models import ImgToPdfModel
import img2pdf 
from PIL import Image 
import os 
import io
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import FileResponse, HttpResponse
from django.views.generic import TemplateView


class ConvertImgToPdfView(APIView):
    def post(self, request):
        try:
            print(request.data['image'], '----------------image---------')
            create_obj = ImgToPdfModel.objects.create(image=request.data.get('image'))
            # response = self.convert_img_to_pdf(request.data.get("image"))
            # if buffer:
            #     response = HttpResponse(content_type='application/pdf')
            #     response['Content-Disposition'] = 'attachment; filename=output.pdf'
            #     response.write(buffer.read())
            return Response({"data":None, "message":"done", "status":200})
            # else:
            #     return HttpResponse("Image to PDF conversion failed.", status=500)
        except Exception as e:
            print(e, 'eeeeeeeeeeeeeeeeeeeee')
            return Response({"data":str(e), "message":"not done", "status":400})

    def convert_img_to_pdf(self, img_path):
        # for file in os.listdir(source_dir):
        #     if file.split('.')[-1] == "jpg":
        image = Image.open(img_path)
        image_converted = image.convert('RGB')
        image_converted.save(os.path.join("./", f"kane11.pdf"))
        return "done"
        # try:
        #     # Create a BytesIO buffer from the contents of the InMemoryUploadedFile
        #     image_buffer = BytesIO(img_path.read())

        #     # Open the image from the BytesIO buffer
        #     image = Image.open(image_buffer)

        #     # Create a new BytesIO buffer to store the PDF data
        #     pdf_buffer = BytesIO()

        #     # Convert image to PDF and write to the PDF buffer
        #     pdf_bytes = img2pdf.convert(image)

        #     # Write the PDF bytes to the buffer
        #     pdf_buffer.write(pdf_bytes)

        #     # Set the position of the PDF buffer to the beginning
        #     pdf_buffer.seek(0)

        #     return pdf_buffer

        # except Exception as e:
        #     # Handle the exception (e.g., log the error)
        #     print(f"Error converting image to PDF: {e}")
        #     return None


class GetPdfByIdView(TemplateView):
    template_name = "getPdf.html"
    def get(self, request, pdf_id):
        pdf = ImgToPdfModel.objects.get(id=pdf_id)
        print(pdf.id, '--------------------pdf------------------')
        return render(request, self.template_name, locals())
    
class DownloadPdfFileView(TemplateView):    
    template_name = "getPdf.html"
    def get(self, request, pdf_id):
        print('came hereeeeeeeeeeeeeeeeee11111111111111')
        uploaded_file = ImgToPdfModel.objects.get(id=pdf_id)
        print(uploaded_file.pdf_file,'--------------------')
        response = HttpResponse(uploaded_file.pdf_file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.pdf_file.name}"'
        print('-------------- came here --------------')
        return response    
    