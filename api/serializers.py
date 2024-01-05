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
    
class BorrowersSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowers
        fields = ("id","borrower")

class LendersSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageLender
        fields = ("id","lender")

class CollateralSizeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CollateralModel
        fields = ("id","collateral_type")

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateRealEstate
        fields = ("id","state")                


class CreNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreNotesModel
        fields = ['id', 'notes', 'cre', 'created_at']              

class CommercialRealEstateSerializer(serializers.ModelSerializer):
    borrower = BorrowersSizeSerializer()
    lender = LendersSizeSerializer()
    collateral_type = CollateralSizeSerializer()
    state = StateSerializer()
    notes = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    class Meta:
        model = CommercialRealEstate
        fields = ("id","loan_amount","borrower","lender","origination_date","maturity_date","collateral_type","street_address","city","state","notes", "is_bookmarked", "county")

    # def get_borrower(self,obj):
    #     borrower = Borrowers.objects.get(id = obj.borrower.id)
    #     serializer = BorrowersSizeSerializer(borrower)
    #     return serializer.data
    
    # def get_lender(self,obj):
    #     borrower = MortgageLender.objects.get(id = obj.lender.id)
    #     serializer = LendersSizeSerializer(borrower)
    #     return serializer.data
    
    # def get_collateral_type(self,obj):
    #     borrower = CollateralModel.objects.get(id = obj.collateral_type.id)
    #     serializer = CollateralSizeSerializer(borrower)
    #     return serializer.data
    
    # def get_state(self,obj):
    #     state = StateRealEstate.objects.get(id = obj.state.id)
    #     serializer = StateSerializer(state)
    #     return serializer.data
    
    def get_notes(self, obj):
        try:
            print(111111111111)
            notes = CreNotesModel.objects.filter(cre = obj.id)
            serializer = CreNotesSerializer(notes, many=True)
            return serializer.data
        except:
            return []
    def get_is_bookmarked(self, obj):
        try:
            user_id = self.context.get("user_id")
            print(obj.id, '---------obj.id----------', obj.id)
            get_save_cre_lead_for_this_user = SaveCreLeads.objects.get(cre_user_id = 1, cre_lead_id = obj.id)
            print(get_save_cre_lead_for_this_user, '-----------------')                                                                                
            return  True
        except:
            return False    