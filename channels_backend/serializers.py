from rest_framework import serializers
from api.models import SessionIdStoreModel


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
            return obj.user.email
        except:
            return None    