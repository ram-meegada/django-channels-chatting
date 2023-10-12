from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
from datetime import datetime
import asyncio, json
from api.utils import open_ai_chat
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from api.models import ChatBotModel, GroupModel, SessionIdStoreModel, ChatStorageWithSessionIdModel, OneToOneChatRoomModel, SaveChatOneToOneRoomModel, User
import base64, random
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class AgentChatbotUserChatting(AsyncWebsocketConsumer):
    async def connect(self):
        print('cam to connect websocket----------------')
        # self.sender = self.scope['user'].first_name
        # print(self.sender, '==================')
        # key = self.scope['url_route']['kwargs']['key']
        self.session_id = self.scope['url_route']['kwargs']['session']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.username_in_chatting = await database_sync_to_async(self.get_username_in_chatting)(self.user_id)
        self.get_active_session_with_agent = await database_sync_to_async(self.get_active_session_of_user)(self.scope['url_route']['kwargs']['session'])
        store_chat = await database_sync_to_async(SessionIdStoreModel.objects.get)(session_id = self.session_id)
        self.session_foreign_key = store_chat.id
        print(self.get_active_session_with_agent, '---------------------------')
        if self.get_active_session_with_agent[1] is not None:
            self.talking_with_agent = True
            await self.channel_layer.group_add(self.session_id, self.channel_name)
            await self.accept()
        else:
            self.data_set = await database_sync_to_async(self.get_data_set)(self.session_id)
            self.talking_with_agent = False
            # if self.check_key is None:
            #     await self.close('no api key found')
            with open(f"{self.data_set}", 'r', encoding='utf-8') as file:
                data_set = json.load(file)    
            self.training = train_data(data_set)
            await self.accept()
    def get_active_session_of_user(self, session_id):
        try:
            active_session = SessionIdStoreModel.objects.get(session_id=session_id)
            return (active_session.session_id, active_session.agent, active_session.id)
        except:
            return (None, None, None)

    def get_data_set(self, session_id):
        try:
            # key = ChatBotModel.objects.get(production_api_key=f'prod_{api_key}')
            current_session = SessionIdStoreModel.objects.get(session_id=session_id)
            data_set = current_session.chatbot.data_set
            return (data_set)
        # except ChatBotModel.DoesNotExist:
        #     key = ChatBotModel.objects.get(test_api_key=f'test_{api_key}')
        #     return (key, 'testing')
        except:
            return None
        
    async def receive(self, text_data):
        newMessage = f"{text_data}"
        if self.talking_with_agent == True:
            # try:
            save_customer_conversation = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.session_foreign_key, user_id=self.user_id, user_input=f'{text_data}')
            # print('if self.talking_with_agent == True==============if self.talking_with_agent == True===========')
            await self.channel_layer.group_send(self.session_id,
                    {
                        'type': 'chat_message',
                        'msg': f'{self.username_in_chatting[1]}: {text_data}'
                    }                                      
                )
            # except:
            #     save_customer_conversation = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.get_active_session_with_agent[2], user_input=f'{self.username_in_chatting[1]}: {text_data}')
            #     await self.channel_layer.group_send(self.get_active_session_with_agent[0],
            #     {
            #         'type': 'chat_message',
            #         'msg': f'{self.username_in_chatting[1]}: {text_data}'
            #     }
            # )
        elif text_data != "talk to human" and self.talking_with_agent == False:
            chatbot_reply = chatbot_func(text_data, self.training[0], self.training[1], self.training[2], self.training[3])
            chatbot_user_conversation = {}
            chatbot_user_conversation['customer'] = text_data
            chatbot_user_conversation['Bot'] = chatbot_reply
            # await self.send(text_data=json.dumps(chatbot_user_conversation))
            await self.send(text_data=f"Bot:-{chatbot_reply}")
            save_chat_customer = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.session_foreign_key, user_id=self.user_id, user_input=newMessage)
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
        # await self.send(text_data=message_to_be_sent)
        await self.send(text_data=event['msg'])


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



class UserChattingWithOpenAIAgent(AsyncWebsocketConsumer):
    async def connect(self):
        print('cam to connect websocket----------------')
        # self.sender = self.scope['user'].first_name
        # print(self.sender, '==================')
        # key = self.scope['url_route']['kwargs']['key']
        self.session_id = self.scope['url_route']['kwargs']['session']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.username_in_chatting = await database_sync_to_async(self.get_username_in_chatting)(self.user_id)
        self.get_active_session_with_agent = await database_sync_to_async(self.get_active_session_of_user)(self.scope['url_route']['kwargs']['session'])
        store_chat = await database_sync_to_async(SessionIdStoreModel.objects.get)(session_id = self.session_id)
        self.session_foreign_key = store_chat.id
        print(self.get_active_session_with_agent, '---------------------------')
        if self.get_active_session_with_agent[1] is not None:
            self.talking_with_agent = True
            await self.channel_layer.group_add(self.session_id, self.channel_name)
            await self.accept()
        else:
            # self.data_set = await database_sync_to_async(self.get_data_set)(self.session_id)
            self.talking_with_agent = False
            # if self.check_key is None:
            #     await self.close('no api key found')
            # with open(f"{self.data_set}", 'r', encoding='utf-8') as file:
            #     data_set = json.load(file)    
            # self.training = train_data(data_set)
            await self.accept()
    def get_active_session_of_user(self, session_id):
        try:
            active_session = SessionIdStoreModel.objects.get(session_id=session_id)
            return (active_session.session_id, active_session.agent, active_session.id)
        except:
            return (None, None, None)

    def get_data_set(self, session_id):
        try:
            # key = ChatBotModel.objects.get(production_api_key=f'prod_{api_key}')
            current_session = SessionIdStoreModel.objects.get(session_id=session_id)
            data_set = current_session.chatbot.data_set
            return (data_set)
        # except ChatBotModel.DoesNotExist:
        #     key = ChatBotModel.objects.get(test_api_key=f'test_{api_key}')
        #     return (key, 'testing')
        except:
            return None
        
    async def receive(self, text_data):
        newMessage = f"{text_data}"
        if self.talking_with_agent == True:
            # try:
            save_customer_conversation = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.session_foreign_key, user_id=self.user_id, user_input=f'{text_data}')
            # print('if self.talking_with_agent == True==============if self.talking_with_agent == True===========')
            await self.channel_layer.group_send(self.session_id,
                    {
                        'type': 'chat_message',
                        'msg': f'{self.username_in_chatting[1]}: {text_data}'
                    }                                      
                )
            # except:
            #     save_customer_conversation = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.get_active_session_with_agent[2], user_input=f'{self.username_in_chatting[1]}: {text_data}')
            #     await self.channel_layer.group_send(self.get_active_session_with_agent[0],
            #     {
            #         'type': 'chat_message',
            #         'msg': f'{self.username_in_chatting[1]}: {text_data}'
            #     }
            # )
        elif text_data != "talk to human" and self.talking_with_agent == False:
            chatbot_reply = open_ai_chat(text_data)
            print(chatbot_reply, '--------------------chatbot_reply----------------------') 
            # chatbot_reply = chatbot_func(text_data, self.training[0], self.training[1], self.training[2], self.training[3])
            chatbot_user_conversation = {}
            chatbot_user_conversation['customer'] = text_data
            chatbot_user_conversation['Bot'] = chatbot_reply
            # await self.send(text_data=json.dumps(chatbot_user_conversation))
            await self.send(text_data=f"Bot:-{chatbot_reply}")
            save_chat_customer = await database_sync_to_async(ChatStorageWithSessionIdModel.objects.create)(session_id=self.session_foreign_key, user_id=self.user_id, user_input=newMessage)
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
        # await self.send(text_data=message_to_be_sent)
        await self.send(text_data=event['msg'])


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