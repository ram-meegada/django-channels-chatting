from rest_framework import serializers
from api.models import SessionIdStoreModel, ChatStorageWithSessionIdModel


class GetAllUserSessionsSerializer(serializers.ModelSerializer):
    agent = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = SessionIdStoreModel
        fields = ['id', 'session_id', 'agent', 'user', 'is_queued', 'is_resolved', 'created_at']
    def get_agent(self, obj):
        try:
            return obj.agent.email
        except:
            return None    
    def get_user(self, obj):
        try:
            return obj.user.email
        except:
            return None    
        
class GetAllQueuedSessionsSerializer(serializers.ModelSerializer):
    agent = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = SessionIdStoreModel
        fields = ['id', 'session_id', 'agent', 'user', 'is_queued', 'is_resolved', 'created_at']
    def get_agent(self, obj):
        try:
            return obj.agent.email
        except:
            return None    
    def get_user(self, obj):
        try:
            return obj.user.first_name
        except:
            return None    
        

class ChatStorageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = ChatStorageWithSessionIdModel
        fields = ['user', 'user_input', 'timestamp']
    def get_user(self, obj):
        try:
            user_name = obj.user.first_name
            return user_name
        except:
            return None
        
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from api.documents import NewDocument
from channels_backend.models import ElasticSearchModel

class NewDocumentSerializer(DocumentSerializer):
    class Meta:
        model = ElasticSearchModel
        document = NewDocument
        fields = ('title', 'content')

        def get_location(self, obj):
            try:
                return obj.location.to_dict()
            except:
                return {}