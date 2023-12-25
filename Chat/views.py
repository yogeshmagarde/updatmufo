

from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from datetime import datetime, timedelta
from rest_framework.response import Response

from .permissions import RoomPermission
from . import serializers
from .models import Room, Chat,ChatMessage,Notification
from .serializers import ChatMessageSerializer
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from Mufo.Minxins import authenticate_token
import html
from rest_framework.views import APIView
from Chat.consumer import ChatConsumer
from Chat.consumer import get_room_users
from User.models import room_create_claim_coins
from django.utils import timezone
from datetime import timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class RoomViewSets(viewsets.ModelViewSet):
    serializer_class = serializers.RoomSerializer
    queryset = Room.objects.all()
    lookup_field = "room_code"
    @method_decorator(authenticate_token)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room_name = serializer.validated_data.get('room_name')
        serializer.save(creator=request.user) #Use the authenticated user
        self.add_coins(request.user, 10)
        serializer.save(room_name=html.escape(room_name))
        return Response(
            {
                "status": "success",
                "room_code": serializer.data.get('room_code')
            },
            status=status.HTTP_201_CREATED
        )

    def add_coins(self, user, amount):
            created_date = timezone.now()#datetime.today()
            today = room_create_claim_coins.objects.filter(user=user, created_date__date=created_date.date()).count()
            print(today)
            if today<100:
                user.coins += amount
                user.save()
                message = f"You got {amount} coins to create a chatroom!"
                notification = Notification(user=user, message=message)
                notification.save()
            room_create_claim_coins.objects.create(user=user,created_date=created_date,claim_coins=True)
           


    def retrieve(self, request,room_code, *args, **kwargs):
        lookup_field = self.lookup_field or self.lookup_url_kwarg
        lookup_kwargs = {lookup_field: self.kwargs[lookup_field]}
        _ = get_object_or_404(Room, **lookup_kwargs)

        queryset = Chat.objects.filter(room__room_code=self.kwargs[lookup_field],
                                       created__range=(datetime.now() - timedelta(days=5), datetime.now()))
        serializer = serializers.ChatSerializer(queryset, many=True)
        chat_messages=serializer.data
        room_creator_profile_picture = _.creator.profile_picture if _.creator.profile_picture else None
        
        joined_room_profile_pictures = list(ChatConsumer.joined_room.values())
        room_users = get_room_users(room_code)
        print("joined_room_profile_pictures",room_users)
        return Response({"chat_messages":chat_messages,"room_creator_profile_picture":room_creator_profile_picture,"joined_room_profile_pictures":room_users})
    
class ChatMessageList(APIView):
    def get(self, request, format=None):
        chat_messages = ChatMessage.objects.all()
        serializer = ChatMessageSerializer(chat_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ChatViewSets(viewsets.ModelViewSet):

    serializer_class = serializers.ChatSerializer
    queryset = Chat.objects.all()


class JoinRoomView(APIView):
    def get(self, request, room_code):
        is_exist = Room.objects.filter(room_code=room_code).first()
        if not is_exist:
            return Response({"detail": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"room_name": room_code}, status=status.HTTP_200_OK)


class AllRoomView(APIView):
    def get(self,request):
        Rooms= Room.objects.filter(is_public=1)
        serializer = serializers.RoomsGetSerializer(Rooms,many=True)
        return Response(serializer.data)
    

class AllRoomofjockey(APIView):
    @method_decorator(authenticate_token)
    def get(self,request):
        Rooms= Room.objects.filter(creator=request.user.id)
        serializer = serializers.RoomsGetSerializer(Rooms,many=True)
        return Response(serializer.data)
    

    