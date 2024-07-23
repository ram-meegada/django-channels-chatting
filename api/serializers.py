from rest_framework import serializers
from .models import ChatBotModel, QuestionAndAnswer, User
import os

class CreateChatbotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotModel
        fields = ['id', 'bot_name', 'user', 'api_key']
        extra_kwargs = {'api_key': {'write_only':True}}        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', "first_name", "last_name"]

class GetUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'profile_picture', 'last_name']
    def get_profile_picture(self, obj):
        return str(obj.profile_picture)

# class ApiKeySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatBotModel
#         fields = ('id', 'user_id', 'bot_name', 'bot_photo', 'api_key', 'default_language')
#         extra_kwargs = {'api_key': {'write_only':True}}        

class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAndAnswer
        fields = ['id', 'user_id', 'data_set']

class ChatSerializer(serializers.ModelSerializer):
    chat_links = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'chat_links']        