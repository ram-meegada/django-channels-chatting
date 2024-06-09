from django.shortcuts import render
from rest_framework.views import APIView
import json
import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from rest_framework.response import Response
from io import BytesIO
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

GOOGLE_API_KEY = "AIzaSyApwDN75wOUGFHt3WMhyb1BhQJQWRBqo6g"
google_api_key = GOOGLE_API_KEY

def extract_text_another_func(file_link):
    image = Image.open(file_link)
    text = pytesseract.image_to_string(image)
    return text

def to_markdown(text):
    text = text.replace('*', '')
    intent_text=(textwrap.indent(text, '', predicate=lambda _: True))
    return intent_text

def extract_text(file_link):
        pdf_text = ""
        with file_link.open() as f:
            pdf_stream = BytesIO(f.read())
            pdf_reader = PdfReader(pdf_stream)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
        return pdf_text

class get_assignment_solution(APIView):
    def gemini_solution(self, request):
        file_link = request.FILES.get("file_link")
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyApwDN75wOUGFHt3WMhyb1BhQJQWRBqo6g")
        if int(request.data["type"]) == 1:
            text_data = extract_text(file_link)
            message = HumanMessage(
                content=[
                    {"type": "text",
                        "text": "You are a teacher. Generate questions and answers based on the data I provide to you. Format should be proper Python Javascript object notation list of dictionaries where every dictionary contains keys as 'question', 'answer' and 'options'(if available)."},
                    {"type": "text", "text":text_data}
                ]
            )
            response = llm.invoke([message])
            result = to_markdown(response.content)
            return result
        elif int(request.data["type"]) == 2:
            gemini_result = []
            for file_image in dict(request.data)["file_link"]:
                text_data = extract_text_another_func(file_image)
                message = HumanMessage(
                    content=[
                        {"type": "text",
                            "text": "You are a teacher. Generate questions and answers based on the data I provide to you. Format should be proper Python Javascript object notation list of dictionaries where every dictionary contains keys as 'question', 'answer' and 'options'(if available)."},
                        {"type": "text", "text":text_data}
                    ]
                )
                response = llm.invoke([message])
                result = to_markdown(response.content)
                temp = self.format_final_response(result)
                gemini_result += temp
            return gemini_result

    def post(self, request):
        # file_link = request.FILES.get("file_link")
        # print(request.data,"kdfahlkjsdhflakjshdflakjshdflkjh")
        try:
            result = self.gemini_solution(request)
            if int(request.data["type"]) == 1:
                final_response = self.format_final_response(result)
            else:
                final_response = result
            if not final_response:
                return Response({"data": "empty response", "message": "Please upload the file again", "status": 200})
            return Response({"data": final_response, "record_id": "final_data.id", "message": "RESPONSE", "status": 200})
        except Exception as e:
            return Response({"data": str(e), "message": "Please upload the file again", "status": 400})

    def format_final_response(self, result):
        final_response = ""
        try:
            for i in range(len(result)-1, -1, -1):
                if result[i] == "}":
                    break
            final_response = result[result.index("["): i+1] + "]"
            final_response = json.loads(final_response)
        except:
            pass
        try:
            for i in final_response:
                if not i.get("options"):
                    i["question_type"] = 1
                elif not i["options"]:
                    i["question_type"] = 1
                elif i["options"]:
                    i["question_type"] = 2
        except:
            pass    
        return final_response