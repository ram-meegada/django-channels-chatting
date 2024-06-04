from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User
from react_app.serializer_file import CreateUserSerializer
from rest_framework.permissions import IsAuthenticated

class SignUpView(APIView):
    def post(self, request):
        try:
            print(request.data, type(request.data), '-------------------------------')
            serializer = CreateUserSerializer(data=request.data)
            if serializer.is_valid():
                user_obj = serializer.save()
                user_obj.set_password(request.data["password"])
                user_obj.save()
                return Response({"data": serializer.data, "message": "Registration done successfully", "status": 201})
            else:
                errs = serializer.errors
                for i, j in serializer.errors.items():
                    err_message = j[0]
                    break
                return Response({"data": serializer.errors, "message": err_message, "status": 400})
        except Exception as err:
            return Response({"data": str(type(err)), "message": str(err), "status": 500})
    
class LoginView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
        except:    
            return Response({"data": None, "message": "Email not found", "status": 400})
        verify_password = check_password(request.data["password"], user.password)
        if verify_password:
            data = {}
            token = RefreshToken.for_user(user)
            data["token"] = str(token.access_token)
            return Response({"data": data, "message": "Logged In successfully", "status": 200})
        return Response({"data": None, "message": "Incorrect password", "status": 400})

class HomePageView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"data": {}, "message": "Home page fetched successfully", "status": 200})

