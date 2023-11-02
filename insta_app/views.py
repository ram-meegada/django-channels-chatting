from django.shortcuts import render
from rest_framework.views import APIView
from insta_app.models import UserFollowersFollowingModel
from insta_app.serializers import GetAllUserFollowersSerializer, GetAllUserFollowingSerializer
from rest_framework.response import Response

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