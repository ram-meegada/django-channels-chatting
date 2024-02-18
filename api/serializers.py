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
    
    def get_notes(self, obj):
        try:
            user_id = self.context.get("user_id")
            notes = CreNotesModel.objects.filter(cre = obj.id, cre_notes_user_id=user_id)
            serializer = CreNotesSerializer(notes, many=True)
            return serializer.data
        except:
            return None
    def get_is_bookmarked(self, obj):
        try:
            user_id = self.context.get("user_id")
            print(obj.id, '---------obj.id----------', obj.id)
            get_save_cre_lead_for_this_user = SaveCreLeads.objects.get(cre_user_id = user_id, cre_lead_id = obj.id)
            print(get_save_cre_lead_for_this_user, '-----------------')                                                                                
            return True
        except:
            return False    
        
class MortgagelenderSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = MortgageLender
        fields = ['id','lender', 'count']    
    def get_count(self, obj):
        lenders_count = self.context.get("lender_count")
        try:
            return lenders_count[obj.id]
        except:
            return 0        
        
class NewCommercialRealEstateSerializer(serializers.ModelSerializer):
    # borrower = serializers.SerializerMethodField()
    # lender = serializers.SerializerMethodField()
    collateral_type = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = CommercialRealEstate
        fields = ("id","loan_amount","origination_date","maturity_date","collateral_type","street_address","city","state","notes", "is_booked")        
        
class GetCreLeadsSerialzer(serializers.ModelSerializer):
    cre_lead = serializers.SerializerMethodField()
    cre_lender = serializers.SerializerMethodField()
    class Meta:
        model = SaveCreLeads
        fields = ("id","cre_lender","cre_lead","cre_user")
    def get_cre_lead(self, obj):
        try:
            obj = CommercialRealEstate.objects.get(id = obj.cre_lead_id)
            serializer = NewCommercialRealEstateSerializer(obj)
            return serializer.data
        except Exception as error:
            print(error, '-------------error---------------')
            return None     
    def get_cre_lender(self,obj):
        obj = MortgageLender.objects.get(id = obj.cre_lender_id)
        serializer = LendersSizeSerializer(obj)
        return serializer.data            
    
class GetCreLeadSerializer(serializers.ModelSerializer):
    loan_amount = serializers.SerializerMethodField()
    borrower = serializers.SerializerMethodField()
    lender = serializers.SerializerMethodField()
    origination_date = serializers.SerializerMethodField()
    maturity_date = serializers.SerializerMethodField()
    collateral_type = serializers.SerializerMethodField()
    street_address = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()

    class Meta:
        model = SaveCreLeads
        # ("id","loan_amount","borrower","lender","origination_date","maturity_date","collateral_type","street_address","city","state","notes", "is_booked")
        fields = ['id', 'loan_amount', 'borrower', 'cre_user', 'cre_lead', 'lender', 'origination_date', 'maturity_date',
                   'collateral_type', 'street_address', 'city', 'state', 'notes', 'is_bookmarked']
    def get_loan_amount(self, obj):
        try:
            return obj.cre_lead.loan_amount
        except:
            return None    
    def get_borrower(self,obj):
        try:
            borrower = Borrowers.objects.get(id = obj.cre_lead.borrower.id)
            serializer = BorrowersSizeSerializer(borrower)
            return serializer.data
        except:
            return None    
    def get_lender(self,obj):
        try:
            borrower = MortgageLender.objects.get(id = obj.cre_lender.id)
            serializer = LendersSizeSerializer(borrower)
            return serializer.data
        except Exception as error:
            print(error, '-------------------')
            return None    
    def get_origination_date(self, obj):
        try:
            return str(obj.cre_lead.origination_date)    
        except:
            return None    
    def get_maturity_date(self, obj):
        try:
            return str(obj.cre_lead.maturity_date)    
        except:
            return None    
    def get_collateral_type(self, obj):
        borrower = CollateralModel.objects.get(id = obj.cre_lead.collateral_type.id)
        serializer = CollateralSizeSerializer(borrower)
        return serializer.data
    def get_street_address(self, obj):
        try:
            return obj.cre_lead.street_address
        except:
            return None
    def get_city(self, obj):
        try:
            return obj.cre_lead.city
        except:
            return None
    def get_state(self,obj):
        try:
            state = StateRealEstate.objects.get(id = obj.cre_lead.state.id)
            serializer = StateSerializer(state)
            return serializer.data
        except:
            return None
    def get_notes(self, obj):
        try:
            notes = CreNotesModel.objects.filter(cre = obj.cre_lead.id)
            serializer = CreNotesSerializer(notes, many=True)
            return serializer.data
        except:
            return None    
