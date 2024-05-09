from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
from datetime import datetime
import asyncio, json
# from .utils import train_data, chatbot_func
from .models import ChatBotModel
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import GroupModel, SessionIdStoreModel, ChatStorageWithSessionIdModel, OneToOneChatRoomModel, \
                    SaveChatOneToOneRoomModel, User
import base64, random
from asgiref.sync import sync_to_async
from pyfcm import FCMNotification
from abstractbaseuser_project import settings

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('websocker connected.....', event)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('message received.....', event)
        if event['text'] == 'stop':
            await self.websocket_disconnect({
                'type': 'websocket.disconnect'
            })

        await self.send({
            'type': 'websocket.send',
            'text': 'this is from server side'
        })

    async def websocket_disconnect(self, event):
        print('websocket disconnected.....', event)
        raise StopConsumer()
    
##################################################################################
        


class MySyncChatBot(SyncConsumer):

    def websocket_connect(self, event):
        key = self.scope['url_route']['kwargs']['key']
        try:
            check_key = self.get_chatbot_model_by_api_key(key)
        except:
            self.websocket_disconnect({
                'type': 'websocket.disconnect'
            }) 
        with open(f"{check_key.data_set}", 'r', encoding='utf-8') as file:
            data_set = json.load(file)    
        self.training = train_data(data_set)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        newMessage = event['text']
        if newMessage == "Talk to human":
            async_to_sync(self.channel_layer.group_add)("chat-with-agent", self.channel_name)
            try:
                check_existing_group = GroupModel.objects.get(name = "chat-with-agent")
                # chats = ChatStorageWithChatbotModel.objects.filter(group_id = check_existing_group)
            except:    
                create_group = GroupModel.objects.create(name = "chat-with-agent")
        chatbot_reply = chatbot_func(newMessage, self.training[0], self.training[1], self.training[2], self.training[3])
        self.send({
            'type': 'websocket.send',
            'text': chatbot_reply
        })

    def websocket_disconnect(self, event):
        print('websocket disconnected.....', event)
        raise StopConsumer()
    
    def get_chatbot_model_by_api_key(self, api_key):
        try:
            return ChatBotModel.objects.get(api_key=api_key)
        except ChatBotModel.DoesNotExist:
            return None
        

class MyChatBot(AsyncConsumer):
    async def websocket_connect(self, event):
        key = self.scope['url_route']['kwargs']['key']
        try:
            check_key = await self.get_chatbot_model_by_api_key(key)
        except:
            await self.websocket_disconnect({
                'type': 'websocket.disconnect'
            }) 
        with open(f"{check_key.data_set}", 'r', encoding='utf-8') as file:
            data_set = json.load(file)    
        print(data_set, '===============data_set=================')
        self.training = train_data(data_set)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        newMessage = event['text']
        chatbot_reply = chatbot_func(newMessage, self.training[0], self.training[1], self.training[2], self.training[3])
        await self.send({
            'type': 'websocket.send',
            'text': chatbot_reply
        })

    async def websocket_disconnect(self, event):
        print('websocket disconnected.....', event)
        raise StopConsumer()
    
    @database_sync_to_async
    def get_chatbot_model_by_api_key(self, api_key):
        try:
            return ChatBotModel.objects.get(api_key=api_key)
        except ChatBotModel.DoesNotExist:
            return None
        
from channels.generic.websocket import AsyncWebsocketConsumer

    

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        # global group
        group = self.scope['url_route']['kwargs']['groupname']
        # try:
        #     check_existing_group = GroupModel.objects.get(name = group)
        #     chats = ChatStorageWithChatbotModel.objects.filter(group_id = check_existing_group)
        # except:    
        #     create_group = GroupModel.objects.create(name = group)
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        group = self.scope['url_route']['kwargs']['groupname']
        # print(self.scope['session'], self.scope['user'], '========= session =========')
        group_id = GroupModel.objects.get(name=group)
        # chat_obj = ChatStorageWithChatbotModel.objects.create(
        #     content = event['text'],
        #     group = group_id 
        # )
        async_to_sync(self.channel_layer.group_send)(group,
        {
            'type': 'chat.message',
            'msg': event['text']
        })

    def websocket_disconnect(self, event):
        print('websocker disconnected.....', event)
        raise StopConsumer()
    
    def chat_message(self, event):
        print(event, '============== event ===============')
        self.send({
            'type': 'websocket.send',
            'text': event['msg']
        })
    


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        key = self.scope['url_route']['kwargs']['key']
        user = self.scope['user']
        print(user.id, self.scope, '============ user ===============')
        try:
            check_key = await database_sync_to_async(self.chatbot_model_by_api_key)(key)
        except:
            self.websocket_disconnect({
                'type': 'websocket.disconnect'
            })  
        self.session_id = self.create_session_id()
        print(self.session_id, '==================== self.session_id ====================')
        with open(f"{check_key.data_set}", 'r', encoding='utf-8') as file:
            data_set = json.load(file)    
        self.training = train_data(data_set)
        await self.accept()

    def chatbot_model_by_api_key(self, api_key):
        try:
            key = ChatBotModel.objects.get(api_key=api_key)
            return key
        except Exception as e:
            return None
        
    async def receive(self, text_data):
        print('message received.....', text_data)
        newMessage = text_data
        if newMessage == "talk to human":
            pass
            # session_id = await self.create_session_id()
            # print(session_id, '=====================')
            # self.channel_layer.group_add(f"{session_id}", self.channel_name)
            # try:
            #     check_existing_group = await database_sync_to_async(GroupModel.objects.get)(name = "chat-with-agent")
            #     chats = await database_sync_to_async(ChatStorageWithChatbotModel.objects.filter)(group_id = check_existing_group)
            # except:    
            #     create_group = await database_sync_to_async(GroupModel.objects.create)(name = "chat-with-agent")
        chatbot_reply = chatbot_func(newMessage, self.training[0], self.training[1], self.training[2], self.training[3])
        # store_chat = await database_sync_to_async(ChatStorageWithChatbotModel.objects.create)(session_id = self.session_id, user_input=newMessage, reply=chatbot_reply)
        await self.send(text_data=chatbot_reply)

    async def disconnect(self, close_code):
        print('websocket disconnected.....', close_code)

    def create_session_id(self):
        id = base64.b64encode(str(random.randint(100000, 999999)).encode()).decode()
        return id
    

from channels.layers import get_channel_layer
class UserChattingWithFriendConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user1 = self.scope['url_route']['kwargs']['user1']
        user2 = self.scope['url_route']['kwargs']['user2']
        if self.scope['user'].id not in (user1, user2):
            await self.close('you have no access for this page')
        self.room_name = f"chat_{user1}_{user2}"
        all_chat_rooms = await database_sync_to_async(self.get_all_chat_rooms)()
        if (self.room_name,) not in all_chat_rooms:
            self.add_room_to_database = await database_sync_to_async(OneToOneChatRoomModel.objects.create)(
                room_name=self.room_name, user1_id=user1, user2_id=user2)
        else:
            self.add_room_to_database = await database_sync_to_async(OneToOneChatRoomModel.objects.get)(room_name=self.room_name)
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
    def get_all_chat_rooms(self):
        all_chats = OneToOneChatRoomModel.objects.all().values_list('room_name')
        print(set(all_chats), '--------all chats =============')
        return set(all_chats)

    async def receive(self, text_data):
        user_name = await database_sync_to_async(self.get_user_name)(self.scope['user'].id)
        save_message = await database_sync_to_async(SaveChatOneToOneRoomModel.objects.create)(room_id=self.add_room_to_database.id, user_message=f'{user_name}: {text_data}')
        await self.channel_layer.group_send(self.room_name,
            {
                'type': 'chat_message',
                'msg': f'{user_name}: {text_data}'
            }                                      
        )
        print(self.scope['user'], '------------- scope user ===============')
        if self.scope['user'].id == self.scope['url_route']['kwargs']['user1']:
            send_notification_to = await database_sync_to_async(self.get_user_to_send_notification)(self.scope['url_route']['kwargs']['user2'])
            print(send_notification_to, '-----send_notification_to1111111111-----------------')                
        else:
            send_notification_to = await database_sync_to_async(self.get_user_to_send_notification)(self.scope['url_route']['kwargs']['user1'])
            print(send_notification_to, '===========send_notification_to22222222222==============')                
        push_service = FCMNotification(api_key=f"{settings.FCM_APIKEY}")
        result = push_service.notify_single_device(
            registration_id = f"{send_notification_to}",
            message_title = f"You have a message from {self.scope['user'].first_name}",
            message_body = f"{text_data}",
        )
    def get_user_to_send_notification(self, user_id):
        try:
            notification_to_user = UserSession.objects.get(user_id=user_id)
            return notification_to_user.device_token
        except:
            return None

    def get_user_name(self, user_id):
        user_name = User.objects.get(id=user_id).first_name
        return user_name

    async def chat_message(self, event):
        await self.send(text_data=event['msg'])
    async def disconnect(self, close_code):
        print('websocket disconnected.....', close_code)

####################################################################################################################################
class AgentChatbotUserChatting(AsyncWebsocketConsumer):
    async def connect(self):
        print('cam to connect websocket----------------')
        self.sender = self.scope['user'].first_name
        print(self.sender, '==================')
        print(self.scope['user'], '==================')
        key = self.scope['url_route']['kwargs']['key']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.get_active_session_with_agent = await database_sync_to_async(self.get_active_session_of_user)(self.scope['url_route']['kwargs']['session'])
        if self.get_active_session_with_agent[1] is not None:
            self.talking_with_agent = True
            self.agent_name = self.get_active_session_with_agent[1]
            await self.channel_layer.group_add(self.get_active_session_with_agent[0], self.channel_name)
            await self.accept()
        else:    
            self.session_id = self.scope['url_route']['kwargs']['session']
            check_key = await database_sync_to_async(self.chatbot_model_by_api_key)(key)
            print(check_key[1], f'-----------You are in {check_key[1]} mode -----------')
            self.talking_with_agent = False
            if check_key is None:
                await self.close('no api key found')
            store_chat = await database_sync_to_async(SessionIdStoreModel.objects.get)(session_id = self.session_id, user_id=self.user_id)
            self.session_foreign_key = store_chat.id
            with open(f"{check_key[0].data_set}", 'r', encoding='utf-8') as file:
                data_set = json.load(file)    
            self.training = train_data(data_set)
            await self.accept()
            
    def get_active_session_of_user(self, session_id):
        try:
            active_session = SessionIdStoreModel.objects.get(session_id=session_id)
            return (active_session.session_id, active_session.agent, active_session.id)
        except:
            return (None, None, None)

    def chatbot_model_by_api_key(self, api_key):
        try:
            key = ChatBotModel.objects.get(production_api_key=f'prod_{api_key}')
            return (key, 'production')
        except ChatBotModel.DoesNotExist:
            key = ChatBotModel.objects.get(test_api_key=f'test_{api_key}')
            return (key, 'testing')
        except:
            return None
        
    async def receive(self, text_data):
        self.username_in_chatting = await database_sync_to_async(self.get_username_in_chatting)(self.user_id)
        newMessage = f"{self.username_in_chatting[1]}:-{text_data}"
        if self.talking_with_agent == True:
            print(f'-------taling with agent --------------')
            try:
                save_customer_conversation = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.session_foreign_key, user_input=f'{self.sender}: {text_data}')
                # message = {'data': f'now you are chatting with {self.sender}'}
                # await self.send(text_data = json.dumps(message))
                await self.channel_layer.group_send(self.session_id,
                {
                    'type': 'chat_message',
                    'msg': f'{self.sender}: {text_data}'
                }                                      
            )
            except:
                save_customer_conversation = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.get_active_session_with_agent[2], user_input=f'{self.sender}: {text_data}')
                await self.channel_layer.group_send(self.get_active_session_with_agent[0],
                {
                    'type': 'chat_message',
                    'msg': f'{self.sender}: {text_data}'
                }                                      
            )
        elif text_data != "talk to human" and self.talking_with_agent == False:
            print('---------taliking to chatbot---------------')
            chatbot_reply = chatbot_func(text_data, self.training[0], self.training[1], self.training[2], self.training[3])
            chatbot_user_conversation = {}
            chatbot_user_conversation['customer'] = text_data
            chatbot_user_conversation['Bot'] = chatbot_reply
            await self.send(text_data=json.dumps(chatbot_user_conversation))
            save_chat_customer = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.session_foreign_key, user_input=newMessage)
            save_chat_bot = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.session_foreign_key, user_input=f"Bot:- {chatbot_reply}")
        if text_data == "talk to human" and self.talking_with_agent == False:  
            self.talking_with_agent = True
            add_to_queue = await database_sync_to_async(self.add_session_to_queue)(self.session_foreign_key)
            chatbot_user_conversation = {}
            chatbot_user_conversation['customer'] = text_data
            chatbot_user_conversation['Bot'] = "Let me connect you to the agent"
            await self.send(text_data=json.dumps(chatbot_user_conversation))
            await self.channel_layer.group_add(self.session_id, self.channel_name)

    async def chat_message(self, event):
        message_to_be_sent = event['msg'] +':'+ event['type']
        await self.send(text_data=message_to_be_sent)

    def add_session_to_queue(self, session_id):
        get_session = SessionIdStoreModel.objects.get(id=session_id)
        get_session.is_queued = True
        get_session.save()
        return None

    def get_username_in_chatting(self, user_id):
        try:
            user = User.objects.get(id = user_id)
            return (user.role_of_user, user.first_name)
        except Exception as e:
            return (0, 'Not there')


    async def disconnect(self, close_code):
        print('websocket disconnected.....', close_code)

    def create_session_id(self):
        id = base64.b64encode(str(random.randint(100000, 999999)).encode()).decode()
        return id