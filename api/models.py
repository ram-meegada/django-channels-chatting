import os
from django.db import models
import random
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser

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


USER_ROLE_CHOICES = [('1', 'admin'), ('2', 'customer'),
                     ('3', 'agent'), ('4', 'None')]


class User(AbstractUser):
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    email = models.EmailField(
        unique=True, max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    role_of_user = models.CharField(
        choices=USER_ROLE_CHOICES, default='4', max_length=100)
    otp_verified = models.BooleanField(default=True)
    otp = models.CharField(max_length=4, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # class Meta:
    #     db_table = 'user_table'
    #     indexes = [
    #         models.Index(fields=['id'])
    #     ]


class ChatBotModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    bot_name = models.CharField(max_length=254, null=True, blank=True)
    api_key = models.CharField(max_length=222, blank=True, null=True)
    data_set = models.FileField()


class QuestionAndAnswer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    data_set = models.TextField(default='[]')


class GroupModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


################################
class OneToOneChatRoomModel(models.Model):
    room_name = models.CharField(max_length=100)
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mainuser')
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='frienduser')

    def __str__(self):
        return self.room_name


class SaveChatOneToOneRoomModel(models.Model):
    room = models.ForeignKey(OneToOneChatRoomModel,
                             on_delete=models.CASCADE, related_name='savechat')
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


class SessionIdStoreModel(models.Model):
    session_id = models.CharField(max_length=255)
    agent = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                              null=True, blank=True, related_name='chatting_agent')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='chatting_user')
    is_queued = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.session_id


class ChatStorageWithSessionIdModel(models.Model):
    session = models.ForeignKey(SessionIdStoreModel, on_delete=models.CASCADE)
    user_input = models.TextField(default='', null=True, blank=True)
    # reply = models.TextField(default='', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session.session_id

# 3


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


def get_upload_to(instance, filename):
    return os.path.join('DATASET/train', instance.name, f"{random.randint(1000, 9000)}_{filename}")


class SkinImagesModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_upload_to, blank=True, null=True)


class Books(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()


class SendOtpModel(models.Model):
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    device_id = models.CharField(max_length=1000, blank=True)
    otp = models.CharField(max_length=100, blank=True)
    otp_verified = models.BooleanField(default=False)

class TestModl(models.Model):
    text = models.JSONField(default=list)