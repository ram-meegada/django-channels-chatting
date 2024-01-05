from django.db import models
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
import qrcode, random
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File
import pyqrcode
import png, os
from pyqrcode import QRCode
from datetime import datetime
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
        
#         return self.create_user(email, password, **extra_fields)

# ROLE_CHOICES = [('1', 'admin'), ('2', 'customer'), ('3', 'agent')]
# class User(models.Model):ma
#     id = models.BigAutoField(primary_key=True)
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=255, default=None, blank=True, null=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     role = models.CharField(max_length=30, default='1')
#     password = models.CharField(max_length=255)
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']


USER_ROLE_CHOICES = [('1', 'admin'), ('2', 'customer'), ('3', 'agent'), ('4', 'None'), ('5', 'client')]
AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}
class User(AbstractUser):
    username = models.CharField(max_length=255,blank=True, null=True)
    first_name = models.CharField(max_length=255,blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    email = models.EmailField(unique=True, max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    role_of_user = models.CharField(choices=USER_ROLE_CHOICES, default='4', max_length=100)
    bot_subscription = models.IntegerField(blank=True, null=True, help_text="1.six months, 2.one year, 3.two years")

    trail_period = models.IntegerField(blank=True, null=True, help_text="1.six months, 2.one year, 3.two years")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # auth_provider = models.CharField(
    #     max_length=255, blank=False,
    #     null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        db_table = 'user_table'
        # indexes = [
        #     models.Index(fields=['first_name'])
        # ]

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=560, null = True, blank= True)
    user_auth_token = models.TextField(null = True, blank= True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)

class QuestionAndAnswer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) 
    data_set = models.TextField(default='[]')    

class GroupModel(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


    

############### one to one chat #################
class OneToOneChatRoomModel(models.Model):
    room_name = models.CharField(max_length=100)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mainuser')    
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='frienduser')    
    def __str__(self):
        return self.room_name
    
class SaveChatOneToOneRoomModel(models.Model):
    room = models.ForeignKey(OneToOneChatRoomModel, on_delete=models.CASCADE, related_name='savechat')
    user_message = models.TextField(default='')
    sent_time = models.DateTimeField(auto_now=True)

# class singleOneToOneRoom(models.Model):
#     first_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="first_user")
#     second_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="second_user")
#     room_name = models.CharField(max_length=200, blank=True, unique=True)

# class messages(models.Model):
#     room = models.ForeignKey(singleOneToOneRoom, on_delete=models.CASCADE, related_name="messages")
#     message_body = models.TextField()
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_sender")
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_receiver")
#     date_sent = models.DateTimeField(auto_now_add=True)      
#   
# from .fields import ExternalDatabaseForeignKey

# class MyModel(models.Model):
#     name = models.CharField(max_length=100)
#     external_reference = ExternalDatabaseForeignKey(
#         'ProductMicroServiceModel', 
#         on_delete=models.CASCADE, 
#         db_name='product_microservice'
#     )

class ChatBotModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bot_name = models.CharField(max_length=254, null=True, blank=True)
    test_api_key = models.CharField(max_length=222, blank=True, null=True)
    production_api_key = models.CharField(max_length=222, blank=True, null=True)
    data_set = models.FileField()

    def __str__(self):
        return self.user.email


class SessionIdStoreModel(models.Model):
    chatbot = models.ForeignKey(ChatBotModel, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255)
    agent = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='chatting_agent')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='chatting_user')
    is_queued = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.session_id
    # class Meta:
    #     db_table = 'session_model'
    #     indexes = [
    #         models.Index(fields=['session_id'])
    #     ]

class ChatStorageWithSessionIdModel(models.Model):
    session = models.ForeignKey(SessionIdStoreModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    user_input = models.TextField(default='', null=True, blank=True)
    # reply = models.TextField(default='', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.session.session_id
    
#########################################################################3
class RoleModel(models.Model):
    role_name = models.CharField(max_length=265)
    def __str__(self):
        return self.role_name

class PermissionModel(models.Model):
    permission_name = models.CharField(max_length=255)
    def __str__(self):
        return self.permission_name

class SuperAdminAssignPermissionModel(models.Model):
    pass

class ImgToPdfModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    def save(self,*args,**kwargs):
        img = Image.open(self.image)
        pdf_buffer = BytesIO()
        img.save(pdf_buffer, format='PDF')
        self.pdf_file.save(f"{self.image.name.split('.')[-2]}.pdf", File(pdf_buffer), save=False)
        print(self.pdf_file.url, '--------------self.pdf_file.url----------------')
        super(ImgToPdfModel, self).save(*args, **kwargs)

    class Meta:
        db_table = "imgtopdfmodel"
    def __str__(self):
        return self.image.name


# class ScidModel(models.Model):
#     scid = models.CharField(max_length=100, null=True, blank=True)
#     qr_code = models.ImageField(upload_to="qr_codes/", null=True, blank=True)
#     def save(self,*args,**kwargs):
#         # url = f'http://127.0.0.1:8000/qrcode/{self.product_name}/'
#         url=f'{self.scid}'
#         # lst = [self.product_name, self.cost, self.sale_price]
#         qrcode_img=qrcode.make(url)
#         canvas=Image.new("RGB", (300,300),"white")
#         draw=ImageDraw.Draw(canvas)
#         canvas.paste(qrcode_img)
#         buffer=BytesIO()
#         canvas.save(buffer,"PNG")
#         self.qr_code.save(f'image{random.randint(0,9999)}.png',File(buffer),save=False)
#         canvas.close()
#         super(ScidModel, self).save(*args,**kwargs)


class SaveCsvFileModel(models.Model):
    csv_file = models.FileField(upload_to="csv_files", null=True, blank=True)        

class RandomModel(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = "random_model"
        indexes = [
            models.Index(fields=['id'])
        ]

class QuestionModel(models.Model):
    question = models.CharField(max_length=255, blank=True, null=True)
    




class Borrowers(models.Model):
    id = models.AutoField(primary_key=True)
    borrower = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)
    class Meta:
        db_table = "borrowers_model"
        indexes = [
            models.Index(fields=['borrower'])
        ]

class MortgageLender(models.Model):
    id = models.AutoField(primary_key=True)
    lender = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)
    class Meta:
        db_table = "lenders_model"
        indexes = [
            models.Index(fields=['lender'])
        ]

class CollateralModel(models.Model):
    id = models.AutoField(primary_key=True)
    collateral_type = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)    
    class Meta:
        db_table = "collateral_model"
        indexes = [
            models.Index(fields=['collateral_type'])
        ]

class StateRealEstate(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)    
    class Meta:
        db_table = "state_model"
        indexes = [
            models.Index(fields=['state'])
        ]

class CommercialRealEstate(models.Model):
    id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE, blank=True, null=True)
    lender = models.ForeignKey(MortgageLender, on_delete=models.CASCADE, blank=True, null=True)
    origination_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    maturity_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    collateral_type = models.ForeignKey(CollateralModel, on_delete=models.CASCADE, blank=True, null=True)
    street_address  = models.CharField(max_length=200, blank=True, null=True)
    city  = models.CharField(max_length=200, blank=True, null=True)
    state  = models.ForeignKey(StateRealEstate, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField()
    notes_created_at = models.DateTimeField(default=timezone.now) 
    county = models.CharField(max_length=200, blank=True, null=True)
    is_booked = models.BooleanField(default=False, blank=True, null=True)    
    class Meta:
        db_table = "commercial_realestate_model"
        indexes = [
            models.Index(fields=['id'])
        ]

class CreNotesModel(models.Model):
    notes = models.TextField()
    cre = models.ForeignKey(CommercialRealEstate, on_delete = models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = 'cre_notes'
        indexes = [
            models.Index(fields=['cre'])
        ]

class SaveCreLeads(models.Model):
    id = models.AutoField(primary_key=True)
    cre_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="cre_user")
    cre_lead = models.ForeignKey(CommercialRealEstate,on_delete=models.CASCADE, blank=True, null=True,related_name="cre_lead")
    cre_lender = models.ForeignKey(MortgageLender, on_delete=models.CASCADE, blank=True, null=True,related_name="cre_lender")

    is_bookmarked = models.BooleanField(default=True, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = 'save_cre_leads'
        indexes = [
            models.Index(fields=['cre_lender'])
        ]

















class CloneCommercialRealEstate(models.Model):
    id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    borrower = models.CharField(max_length=200, blank=True, null=True)
    lender = models.CharField(max_length=200, blank=True, null=True)
    origination_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    maturity_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    collateral_type = models.CharField(max_length=200, blank=True, null=True)
    street_address  = models.CharField(max_length=200, blank=True, null=True)
    city  = models.CharField(max_length=200, blank=True, null=True)
    state  = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField()
    notes_created_at = models.DateTimeField(default=timezone.now) 
    county = models.CharField(max_length=200, blank=True, null=True)
    is_booked = models.BooleanField(default=False, blank=True, null=True)    
    class Meta:
        db_table = "clone_commercial_realestate_model"
        indexes = [
            models.Index(fields=['borrower', 'lender'])
        ]