from rest_framework import serializers
from master.models import *
from django.utils import timezone

class masterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = '__all__'


class masterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = ('Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text',)

        



class FollowerSerializer(serializers.ModelSerializer):
    user = masterSerializer()

    class Meta:
        model = Follow1
        fields = ('user', 'created_at')


class FollowingSerializer(serializers.ModelSerializer):
    following_user = masterSerializer()

    class Meta:
        model = Follow1
        fields = ('following_user', 'created_at')


class getfollowerSerializer(serializers.ModelSerializer):
    is_followed = serializers.BooleanField(default=False)

    class Meta:
        model = Common
        fields = ('id','Name', 'email', 'Gender', 'Dob', 'profile_picture', 'Introduction_voice', 'Introduction_text', 'is_followed')


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = ('id','Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','coins',)

class UserSearchSerializer(serializers.ModelSerializer):
    is_following = serializers.BooleanField(read_only=True)
    class Meta:
        model = Common
        fields = ('id','Name','email','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','is_following',)



class CoinTransferSerializer(serializers.Serializer):
    receiver_uid = serializers.CharField()
    amount = serializers.IntegerField(min_value=0)

class GiftTransactionhistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftTransactionhistory
        fields = ['sender', 'receiver', 'amount', 'created_date']

class UserSpentTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpent_Time
        fields = ['time_duration','user_uid','created_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Explicitly set the timezone to 'Asia/Kolkata'
        created_date = instance.created_date.astimezone(timezone.get_fixed_timezone(330))  # 330 is the offset for 'Asia/Kolkata'
        representation['created_date'] = created_date.strftime('%Y-%m-%d %H:%M:%S')

        return representation