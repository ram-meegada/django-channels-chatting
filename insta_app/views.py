from django.shortcuts import render
from rest_framework.views import APIView
from insta_app.models import UserFollowersFollowingModel
from insta_app.serializers import GetAllUserFollowersSerializer, GetAllUserFollowingSerializer
from rest_framework.response import Response
import requests

class GetAllUserFollowersView(APIView):
    def get(self, request, user_id):
        try:
            followers = UserFollowersFollowingModel.objects.get(user_id=user_id)
            serializer = GetAllUserFollowersSerializer(followers)
            return Response({"data": serializer.data})
        except:
            return Response({"data": None, "message": "something went wrong"})
        
class GetAllUserFollowingView(APIView):
    def get(self, request, user_id):
        try:
            following = UserFollowersFollowingModel.objects.get(user_id=user_id)
            serializer = GetAllUserFollowingSerializer(following)
            return Response({"data": serializer.data})
        except:
            return Response({"data": None, "message": "something went wrong"})
        
class GetAllMoviesLIstingThirdPartyApi(APIView):
    def get(self, request):
        url = "https://demo.credy.in/api/v1/maya/movies/"
        username = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
        password = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"

        session = requests.Session()
        session.auth = (username, password)

        response = session.get(url, verify=False)

        if response.status_code == 200:
            print(response.json())
            return Response({"data":response.json()})
        else:
            print(f"Error: {response.status_code}")
        