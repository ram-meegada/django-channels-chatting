from rest_framework import serializers
from .models import *
from . import google
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed


class CreateChatbotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotModel
        fields = ['id', 'bot_name', 'user', 'api_key']
        extra_kwargs = {'api_key': {'write_only':True}}        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name']

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


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)        
    
class CreateSourceSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    p_name = serializers.CharField(source = "name")
    class Meta:
        model = SourceModel
        fields = ("id", "p_name", "user")

class GetSourceSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source = "user.email", allow_null = True)
    class Meta:
        model = SourceModel
        fields = ("id", "name", "user_email")

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text')

class PostParentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get("depth", 0)

class PostSerializer(PostParentSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'user')        