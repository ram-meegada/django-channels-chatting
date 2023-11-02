from rest_framework import serializers
from insta_app.models import UserFollowersFollowingModel

class GetAllUserFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowersFollowingModel
        fields = ['id', 'user', 'followers']

class GetAllUserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowersFollowingModel
        fields = ['id', 'user', 'following']