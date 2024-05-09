from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
# class UserAdmin(UserAdmin):
#     list_display = ('email', 'first_name', 'last_name')

class ChatStorageWithSessionIdModelAdmin(admin.ModelAdmin):
    list_display = ('session', 'user_input', 'timestamp')

class SaveMessageModelAdmin(admin.ModelAdmin):
    list_display = ('room', 'user_message', 'sent_time')

# admin.site.register(ImgToPdfModel)
admin.site.register(ChatBotModel)
# admin.site.register(OneToOneChatRoomModel)
admin.site.register(User)
# admin.site.register(QuestionAndAnswer)
admin.site.register(SaveChatOneToOneRoomModel, SaveMessageModelAdmin)
admin.site.register(ChatStorageWithSessionIdModel, ChatStorageWithSessionIdModelAdmin)
# admin.site.register(GroupModel)
admin.site.register(SessionIdStoreModel)
# admin.site.register(RoleModel)
# admin.site.register(PermissionModel)