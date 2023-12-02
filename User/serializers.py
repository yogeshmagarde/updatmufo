


from rest_framework import serializers
from .models import User,Follow,Social_media,claim_coins,Paymentgatway, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields =('phone',)

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields =('otp',)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text')

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','coins',)

class UserSearchSerializer(serializers.ModelSerializer):
    is_following = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ('id','Name','email','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','is_following',)


class getfollowing(serializers.ModelSerializer):

    is_followed = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = User 
        fields = ('id','Name', 'email', 'Gender', 'Dob', 'profile_picture', 'Introduction_voice', 'Introduction_text', 'is_followed')

class FollowingSerializer(serializers.ModelSerializer):
    following_user = getfollowing() 

    class Meta:
        model = Follow
        fields = ('following_user',)



class getfollowerSerializer(serializers.ModelSerializer):
    is_followed = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('id','Name', 'email', 'Gender', 'Dob', 'profile_picture', 'Introduction_voice', 'Introduction_text', 'is_followed')

class FollowerSerializer(serializers.ModelSerializer):
    follower_user = getfollowerSerializer() 

    class Meta:
        model = Follow
        fields = ('follower_user',)



class SocialmediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social_media
        fields = ['Google','Facebook','Snapchat']
       
class GoogleLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social_media
        fields =['Google']

class FacebookLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social_media
        fields =['Facebook']


class SnapchatLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social_media
        fields =['Snapchat']



class CoinsclaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = claim_coins
        # fields = ('claim_coins','created_at')
        fields = ('claim_coins','created_date')



class PaymentgatwaySerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Paymentgatway
        fields = '__all__'

class Transactionmodelserializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['payment_id','order_id','signature','amount']
