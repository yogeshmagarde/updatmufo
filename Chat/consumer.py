
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat , Room , Visitor,ChatMessage,Notificationupdate
from User.models import User,room_join_claim_coins
from master.models import Common
from bots import BotHandler
from datetime import datetime
from asgiref.sync import sync_to_async
import json, html, pytz,uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
import redis
from django.conf import settings

redis_client = redis.StrictRedis(
    host=settings.CHANNEL_LAYERS["default"]["CONFIG"]["hosts"][0][0],
    port=settings.CHANNEL_LAYERS["default"]["CONFIG"]["hosts"][0][1],
    db=0,
)

def get_room_users(room_code):
        room_users = redis_client.hgetall(f'joined_room:{room_code}')
        room_users = [str(value, 'utf-8') for value in room_users.values()]
        return room_users
            

class ChatConsumer_sdp(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
        self.group_room_code = f'chat_{self.room_code}'

        self.room_model = await self.get_room_model()
        self.sender_token = self.scope.get("query_string").decode('utf-8')
        if '=' in self.sender_token:
            self.sender_token = self.sender_token.split('=')[1]
        else:
            self.sender_token = None

        self.user = await self.get_user_from_token(self.sender_token)
        if not self.user:
            self.sender = "admin"
            self.sender_profile_picture = ""
        else:
            self.sender = str(self.user)
            print(self.sender)
            self.sender_profile_picture = str(self.user.profile_picture)

        await self.channel_layer.group_add(self.group_room_code, self.channel_name)
        await self.accept()
       

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_room_code, self.channel_name)
        print('Disconnected!')
    

    
   

    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        action = receive_dict['action']
        message = receive_dict['message']
        

        if(action == 'new-offer') or (action =='new-answer'):
            print("sdp")
            receiver_channel_name = receive_dict['message']['receiver_channel_name']

            print('Sending to ', receiver_channel_name)

            receive_dict['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'receive_dict': receive_dict,
                }
            )

            return

        # receive_dict['message']['receiver_channel_name'] = self.channel_name

        await self.channel_layer.group_send(
            self.group_room_code,
            {
                'type': 'send.sdp',
                'receive_dict': receive_dict,
            }
        )

    async def send_sdp(self, event):
        receive_dict = event['receive_dict']
        action = receive_dict.get('action')
        message = receive_dict.get('message')
        await self.send(text_data=json.dumps({
            'action': action,
            'message': message,
            "sender": self.sender,
        }))

    @database_sync_to_async
    def add_coins(self, user, amount):
            user.coins += amount
            user.save()
            v=room_join_claim_coins.objects.create(
            user=user,
            created_at=timezone.now(),
            claim_coins=True
            )
    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            if not token:
                return None
            return User.objects.get(token=token)
        except User.DoesNotExist:
            return None
     
    @database_sync_to_async
    def get_room_model(self):
        return Room.objects.get(room_code=self.room_code)


class ChatConsumer2(AsyncWebsocketConsumer):
    joined_room = {}    
    
    async def connect(self):
        self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
        self.group_room_code = f'chat_{self.room_code}'

        self.sender_token = self.scope.get("query_string").decode('utf-8')
        if '=' in self.sender_token:
            self.sender_token = self.sender_token.split('=')[1]
        else:
            self.sender_token = None

        self.room_model = await self.get_room_model()
        self.bots = await self.active_bots()
        self.bothandler = BotHandler(self.bots, self.group_room_code)

        self.user = await self.get_user_from_token(self.sender_token)
        if not self.user:
            self.sender = "admin"
            self.sender_profile_picture = ""
        else:
            self.sender = str(self.user)
            self.sender_profile_picture = str(self.user.profile_picture)
       
        await self.channel_layer.group_add(self.group_room_code, self.channel_name)

        await self.channel_layer.group_send(
            self.group_room_code,
            {
                "type": "chat_message",
                "message": "Joined the room!",
                "sender": self.sender,
                "sender_profile_picture": self.sender_profile_picture
            }
        )
 
        if self.sender_profile_picture:
            ChatConsumer2.joined_room[self.sender] = self.sender_profile_picture
            redis_client.hset(f'joined_room:{self.room_code}', self.sender, self.sender_profile_picture)

        await self.accept()

        if self.user:
            await self.add_coins(self.user, 10)
    
      
    async def disconnect(self, code):
        if self.sender in self.joined_room:
            del ChatConsumer2.joined_room[self.sender]
            redis_client.hdel(f'joined_room:{self.room_code}', self.sender)
        
        await self.channel_layer.group_send(
            self.group_room_code,
            {
                "type": "chat.message",
                "message": "Leave the room",
                "sender": self.sender,
                "sender_profile_picture": self.sender_profile_picture,
            }
        )
        await self.channel_layer.group_discard(self.group_room_code, self.channel_name)

   
    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        action = receive_dict.get('action')
        message1 = receive_dict.get('message1')
        message = receive_dict.get('message')
        receive_dict["sender"] = self.sender 
        receive_dict["sender_profile_picture"] = str(self.user.profile_picture) if self.user else ""

        if(action == 'new-offer') or (action =='new-answer'):
            print("sdp")
            receiver_channel_name = receive_dict['message']['receiver_channel_name']

            print('Sending to ', receiver_channel_name)

            receive_dict['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'receive_dict': receive_dict,
                }
            )
        else:
            # receive_dict['message']['receiver_channel_name'] = self.channel_name
            print("Sending a message")
            if not message:
                saved = await self.save_message(message1)
                if saved:
                    date_created = str(saved.created)
                else:
                    date_created = str(datetime.now(tz=pytz.UTC))

            await self.channel_layer.group_send(
                self.group_room_code,
                {
                    'type': 'send.sdp',
                    'receive_dict': receive_dict,
                }
            )
            
    async def send_sdp(self, event):
        receive_dict = event['receive_dict']
        message1 = receive_dict.get('message1')
        message = receive_dict.get('message')
        date = receive_dict.get('date')
        sender = receive_dict.get('sender')
        action = receive_dict.get('action')
        sender_profile_picture = receive_dict.get('sender_profile_picture')#str(self.user.profile_picture) if self.user else ""
        await self.send(text_data=json.dumps #(receive_dict))

        ({
            'message': message1,
            "action" : action,
            'sdp_message': message,
            "date": date,
            "sender": sender,
            "sender_profile_picture": sender_profile_picture,
            
            
        }))

    async def chat_message(self, text_data):
        is_blocked = await self.get_blocked()
        if is_blocked:
            return 0
        message = html.escape(text_data.get("message"))
        sender = text_data.get('sender')
        date = text_data.get('date')
        sender_profile_picture = text_data.get('sender_profile_picture')
        joined_room_profile_pictures = list(ChatConsumer2.joined_room.values())
        room_users = redis_client.hgetall(f'joined_room:{self.room_code}')
        room_user = [str(value, 'utf-8') for value in room_users.values()]
        await self.send(text_data=json.dumps({"message": message,"sender": sender,"profile_picture": sender_profile_picture,'date': date,"filtered_joined_room":joined_room_profile_pictures,"room_users": room_user}))

    
    
    @database_sync_to_async
    def add_coins(self, user, amount):
            user.coins += amount
            user.save()
            common_profile = Common.objects.get(token=self.user.token)
            message = f"You got {10} coins to join the chatroom!"
            notification = Notificationupdate(user=common_profile, message=message)
            notification.save()
            room_join_claim_coins.objects.create(
            user=user,
            created_date=datetime.today(),
            claim_coins=True
            )

    @database_sync_to_async
    def save_message(self, text: str, user=None):
        if not user:
            user = self.user
        if user:
            chat = Chat.objects.create(
                from_user=user,
                text=text
            )

            self.room_model.chat_set.add(chat)

            return chat

    @database_sync_to_async
    def get_room_model(self):
        return Room.objects.get(room_code=self.room_code)

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            if not token:
                return None
            return User.objects.get(token=token)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_blocked(self):
        if self.user and self.room_model:
            query = self.room_model.blocked_users.filter(token=self.user.token)
            return any(query)

    @database_sync_to_async
    def active_bots(self):
        bots = [x for x in self.room_model.active_bots.all()]
        return bots

    @sync_to_async
    def bot_handler(self):
        return BotHandler(self.bots, self.group_room_code)

    @database_sync_to_async
    def get_bot_user(self, bot):
        return bot.user    


class ChatConsumer(AsyncWebsocketConsumer):
    joined_room = {}    
    
    async def connect(self):
        self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
        self.group_room_code = f'chat_{self.room_code}'

        self.sender_token = self.scope.get("query_string").decode('utf-8')
        if '=' in self.sender_token:
            self.sender_token = self.sender_token.split('=')[1]
        else:
            self.sender_token = None

        self.room_model = await self.get_room_model()
        self.bots = await self.active_bots()
        self.bothandler = BotHandler(self.bots, self.group_room_code)

        self.user = await self.get_user_from_token(self.sender_token)
        if not self.user:
            self.sender = "admin"
            self.sender_profile_picture = ""
        else:
            self.sender = str(self.user)
            self.sender_profile_picture = str(self.user.profile_picture)
       
        await self.channel_layer.group_add(self.group_room_code, self.channel_name)

        await self.channel_layer.group_send(
            self.group_room_code,
            {
                "type": "chat_message",
                "message": "Joined the room!",
                "sender": self.sender,
                "sender_profile_picture": self.sender_profile_picture
            }
        )
 
        if self.sender_profile_picture:
            ChatConsumer.joined_room[self.sender] = self.sender_profile_picture
            redis_client.hset(f'joined_room:{self.room_code}', self.sender, self.sender_profile_picture)

        await self.accept()

        if self.user:
            await self.add_coins(self.user, 10)
    
      
    async def disconnect(self, code):
        if self.sender in self.joined_room:
            del ChatConsumer.joined_room[self.sender]
            redis_client.hdel(f'joined_room:{self.room_code}', self.sender)
        
        await self.channel_layer.group_send(
            self.group_room_code,
            {
                "type": "chat.message",
                "message": "Leave the room",
                "sender": self.sender,
                "sender_profile_picture": self.sender_profile_picture,
            }
        )
        await self.channel_layer.group_discard(self.group_room_code, self.channel_name)



    async def receive(self, text_data=None, bytes_data=None):
        print("chat_massage")
        json_data = json.loads(text_data)
        message = json_data.get('message')
        saved = await self.save_message(message)
        if saved:
            date_created = str(saved.created)
        else:
            date_created = str(datetime.now(tz=pytz.UTC))

        sender_profile_picture = str(self.user.profile_picture) if self.user else ""

        await self.channel_layer.group_send(
            self.group_room_code,
            {
                "type": "chat.message",
                "message": message,
                "sender": self.sender,
                "date": date_created,
                "sender_profile_picture": sender_profile_picture
                    
            }
        )
    
        bot = await self.bothandler.get_response(message)
        if bot:
            bot_object, response = bot
            user = await self.get_bot_user(bot_object)
            if response:
                saved = await self.save_message(response, user=user)
                
            await self.channel_layer.group_send(
                self.group_room_code,
                {
                    "type": "bot.response",
                    "message": str(response),
                    "sender": str(user),
                    "date": str(saved.created),
                }
            )

    async def bot_response(self, text_data):
        message = text_data.get("message")
        sender = text_data.get("sender")
        date = text_data.get('date')
        await self.send(text_data=json.dumps({"message": message, "sender": sender, "date": date}))


    async def chat_message(self, text_data):
        is_blocked = await self.get_blocked()
        if is_blocked:
            return 0
        message = html.escape(text_data.get("message"))
        sender = text_data.get('sender')
        date = text_data.get('date')
        sender_profile_picture = text_data.get('sender_profile_picture')
        joined_room_profile_pictures = list(ChatConsumer.joined_room.values())
        room_users = redis_client.hgetall(f'joined_room:{self.room_code}')
        room_user = [str(value, 'utf-8') for value in room_users.values()]
        await self.send(text_data=json.dumps({"message": message,"sender": sender,"profile_picture": sender_profile_picture,'date': date,"filtered_joined_room":joined_room_profile_pictures,"room_users": room_user}))

    
    
    @database_sync_to_async
    def add_coins(self, user, amount):
            user.coins += amount
            user.save()

    @database_sync_to_async
    def save_message(self, text: str, user=None):
        if not user:
            user = self.user
        if user:
            chat = Chat.objects.create(
                from_user=user,
                text=text
            )

            self.room_model.chat_set.add(chat)

            return chat

    @database_sync_to_async
    def get_room_model(self):
        return Room.objects.get(room_code=self.room_code)

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            if not token:
                return None
            return User.objects.get(token=token)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_blocked(self):
        if self.user and self.room_model:
            query = self.room_model.blocked_users.filter(token=self.user.token)
            return any(query)

    @database_sync_to_async
    def active_bots(self):
        bots = [x for x in self.room_model.active_bots.all()]
        return bots

    @sync_to_async
    def bot_handler(self):
        return BotHandler(self.bots, self.group_room_code)

    @database_sync_to_async
    def get_bot_user(self, bot):
        return bot.user

class NotifConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('notif_chat', self.channel_name)
    
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        
        ip_addr = data_json.get('ip_address')
        user_agent = data_json.get('user_agent')

        if all([ip_addr, user_agent]):

            await self.save_visitor(ip_addr=ip_addr, user_agent=user_agent)
        
        total_visitor = await self.total_visitor()

        await self.channel_layer.group_send(
            'notif_chat',
            {
                'type':'send.notif',
                'total_visitor':total_visitor
            }
        )
    
    async def send_notif(self, text_data):

        await self.send(text_data=json.dumps(text_data))
    
    @database_sync_to_async
    def total_visitor(self):
        return Visitor.objects.all().count()
    
    @database_sync_to_async
    def save_visitor(self, ip_addr, user_agent):
        if Visitor.objects.filter(ip_addr=ip_addr).first():
            return None
        v = Visitor(ip_addr=ip_addr, user_agent=user_agent)
        v.save()
        return v

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'test_consumer'
        self.room_group_name = 'test_consumer_group'
        await self.channel_layer.group_add(
            self.room_name, self.room_group_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'connected'}))

    async def receive(self, text_data=None, bytes_data=None):
        print('received called')
        await self.send(text_data=json.dumps({'status': 'connectedcascs'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name, self.room_group_name
        )


#####################################################################################################


# class ChatConsumer1(AsyncWebsocketConsumer):

#     async def connect(self):
#         token = self.scope['query_string'].decode().split('=')[1]
#         self.user = await database_sync_to_async(Common.objects.get)(token=token)
#         if not self.user:
#             await self.close()

#         otheruser_id = int(self.scope['url_route']['kwargs']['user_id'])
#         otheruser = await database_sync_to_async(Common.objects.get)(id=otheruser_id)
#         self.otheruser = otheruser
#         sorted_user_ids = sorted([otheruser_id, self.user.id])
#         self.chat_room = f"conversation_{sorted_user_ids[0]}_{sorted_user_ids[1]}"
#         print(self.chat_room)

#         await self.channel_layer.group_add(self.chat_room, self.channel_name)
#         await self.accept()
#         await self.send(text_data=json.dumps({'status': "online"}))

#     async def disconnect(self,code):
#         await self.channel_layer.group_discard(self.chat_room, self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         sender_id = self.user.id
#         saved = await database_sync_to_async(ChatMessage.objects.create)(sender=self.user, receiver=self.otheruser, content=message)
#         if saved:
#             date_created = str(saved.timestamp)
#         else:
#             date_created = str(datetime.now(tz=pytz.UTC))
#         await self.channel_layer.group_send(
#             self.chat_room, {"type": "chat_message",
#                               "message":message,
#                               "date": date_created,
#                               "sender_id":sender_id
#                               }
#                            ) 

#     async def chat_message(self, text_data):
#         message = text_data['message']
#         date = text_data.get('date')
#         sender_id = text_data.get('sender_id')
#         await self.send(text_data=json.dumps({'message': message,' date':date,
#                                              'sender_id': sender_id,
#                                               }))

class OnetoOneChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']

        saved = await self.save_message(sender_id, receiver_id, message)

        if saved:
            date_created = str(saved.timestamp)
        else:
            date_created = str(datetime.now(tz=pytz.UTC))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'date_created':date_created
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event.get('sender_id')
        date = event.get('date_created')
        sender = await database_sync_to_async(Common.objects.get)(id=sender_id)
        sender_username = sender.Name
        print(sender_username)
        await self.send(text_data=json.dumps({
            'message': message,
            'date':date,
            'sender_username': sender_username
        }))
        
    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        sender = Common.objects.get(id=sender_id)
        receiver = Common.objects.get(id=receiver_id)
        ChatMessage.objects.create(sender=sender, receiver=receiver, content=message)




class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope['query_string'].decode().split('=')[1]
        print(token)
        user = await self.get_user_from_token(token)

        role_group_name = f"{user.uid}_group"
        self.user_group_name = role_group_name
        
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'status': f"{user.usertype}_:-{user.Name}"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def receive(self, text_data):
        print(text_data)
        
        data = json.loads(text_data)
        user_id = data.get('user_id')

        await self.channel_layer.group_send(
            self.user_group_name,
            {
                'type': 'send_notification',
                'value': json.dumps({'status': 'We Got You'})
            }
        )

    async def send_notification(self, event):
        print("Sending notification:", event.get('value'))
        value = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({'value': value}))

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            if not token:
                return None
            return Common.objects.get(token=token)
        except Common.DoesNotExist:
            return None
     