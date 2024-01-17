
from django.utils.timezone import now
from datetime import datetime
# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from master.Mixins import authenticate_token
from .serializers import *
from rest_framework import status, response
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework import filters
from User.models import *
from Audio_Jockey.models import *
from Coins_club_owner.models import *
from Coins_trader.models import *
from Jockey_club_owner.models import *
from master.models import *
from Chat.models import *
from datetime import *
from django.utils import timezone
class UserSpentTimeList(APIView):
    def seconds_to_hms(self,seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return int(hours), int(minutes), int(seconds)

    def get(self, request, format=None):
        
        month = request.query_params.get('month')
        Daliy = request.query_params.get('Daliy')
        session = request.query_params.get('session')
        
        if month:
            current_month = timezone.now().month
            user_spent_times = UserSpent_Time.objects.filter(created_date__month=current_month)
            
            user_totals = {}
            profiles = [Audio_Jockey, Coins_club_owner, Coins_trader, Jockey_club_owner, User]
            
            for user_spent_time in user_spent_times:
                user_id = user_spent_time.user_uid
                time_duration_seconds = user_spent_time.time_duration.total_seconds()
                hours, minutes, seconds = self.seconds_to_hms(time_duration_seconds)

                for profile_model in profiles:
                    user_profile = profile_model.objects.filter(uid=user_id)
                    if user_profile.exists():
                        recipient = user_profile.first()
                        user_name = recipient.Name
                        if user_id not in user_totals:
                            user_totals[user_id] = {"user_name": user_name, "total_duration": {"hours": 0, "minutes": 0, "seconds": 0}}

                        user_totals[user_id]["total_duration"]["hours"] += hours
                        user_totals[user_id]["total_duration"]["minutes"] += minutes
                        user_totals[user_id]["total_duration"]["seconds"] += seconds
                        user_totals[user_id]["total_duration"]["minutes"] += user_totals[user_id]["total_duration"]["seconds"] // 60
                        user_totals[user_id]["total_duration"]["seconds"] %= 60
                        user_totals[user_id]["total_duration"]["hours"] += user_totals[user_id]["total_duration"]["minutes"] // 60
                        user_totals[user_id]["total_duration"]["minutes"] %= 60
                        
                        break
            user_profiles = [{"user_id": key, "user_name": value["user_name"], "total_duration": value["total_duration"]} for key, value in user_totals.items()]

            return Response({"user_profiles": user_profiles})
        
        elif Daliy:
            Daliy = timezone.now().date()
            user_spent_times = UserSpent_Time.objects.filter(created_date__date=Daliy)
            
            user_totals = {}
            profiles = [Audio_Jockey, Coins_club_owner, Coins_trader, Jockey_club_owner, User]
            
            for user_spent_time in user_spent_times:
                user_id = user_spent_time.user_uid
                time_duration_seconds = user_spent_time.time_duration.total_seconds()
                hours, minutes, seconds = self.seconds_to_hms(time_duration_seconds)

                for profile_model in profiles:
                    user_profile = profile_model.objects.filter(uid=user_id)
                    if user_profile.exists():
                        recipient = user_profile.first()
                        user_name = recipient.Name
                        if user_id not in user_totals:
                            user_totals[user_id] = {"user_name": user_name, "total_duration": {"hours": 0, "minutes": 0, "seconds": 0}}

                        user_totals[user_id]["total_duration"]["hours"] += hours
                        user_totals[user_id]["total_duration"]["minutes"] += minutes
                        user_totals[user_id]["total_duration"]["seconds"] += seconds

                        user_totals[user_id]["total_duration"]["minutes"] += user_totals[user_id]["total_duration"]["seconds"] // 60
                        user_totals[user_id]["total_duration"]["seconds"] %= 60
                        user_totals[user_id]["total_duration"]["hours"] += user_totals[user_id]["total_duration"]["minutes"] // 60
                        user_totals[user_id]["total_duration"]["minutes"] %= 60
                        break

            user_profiles = [{"user_id": key, "user_name": value["user_name"], "total_duration": value["total_duration"]} for key, value in user_totals.items()]

            return Response({"user_profiles": user_profiles})
        
        elif session:
            session_start = timezone.now() - timezone.timedelta(hours=1)
            session_end = timezone.now() 
            user_spent_times = UserSpent_Time.objects.filter(created_date__range=[session_start, session_end])
            
            user_totals = {}
            profiles = [Audio_Jockey, Coins_club_owner, Coins_trader, Jockey_club_owner, User]
            
            for user_spent_time in user_spent_times:
                user_id = user_spent_time.user_uid
                time_duration_seconds = user_spent_time.time_duration.total_seconds()
                hours, minutes, seconds = self.seconds_to_hms(time_duration_seconds)

                for profile_model in profiles:
                    user_profile = profile_model.objects.filter(uid=user_id)
                    if user_profile.exists():
                        recipient = user_profile.first()
                        user_name = recipient.Name
                        if user_id not in user_totals:
                            user_totals[user_id] = {"user_name": user_name, "total_duration": {"hours": 0, "minutes": 0, "seconds": 0}}

                        user_totals[user_id]["total_duration"]["hours"] += hours
                        user_totals[user_id]["total_duration"]["minutes"] += minutes
                        user_totals[user_id]["total_duration"]["seconds"] += seconds

                        user_totals[user_id]["total_duration"]["minutes"] += user_totals[user_id]["total_duration"]["seconds"] // 60
                        user_totals[user_id]["total_duration"]["seconds"] %= 60
                        user_totals[user_id]["total_duration"]["hours"] += user_totals[user_id]["total_duration"]["minutes"] // 60
                        user_totals[user_id]["total_duration"]["minutes"] %= 60

                        break

            user_profiles = [{"user_id": key, "user_name": value["user_name"], "total_duration": value["total_duration"]} for key, value in user_totals.items()]

            return Response({"user_profiles": user_profiles})
        return Response({"msg":"error"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UserSpentTimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
class FollowUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, follow):
        try:
            date=datetime.today().date()
            created_date = datetime.today()
            following_common = Common.objects.get(uid=follow)

            if following_common == request.user:
                    return Response({"error": "following and Follow user cannot be the same user."}, status=status.HTTP_400_BAD_REQUEST)
              
            follow_user, created = Follow1.objects.get_or_create(user=request.user,date = date, following_user=following_common)
            
            print("Follow User:", follow_user)
            if not created:
                follow_user.delete()
                return Response({'success': True, 'message': 'Unfollowed user'})
            else:

                Following_profile = Common.objects.get(token=request.user.token)
                message = f"{Following_profile.Name} started following you!"
                notification = Notificationupdate(user=following_common, message=message)
                notification.save()

                profiles = [Audio_Jockey, Coins_club_owner,Coins_trader, Jockey_club_owner, User]
                for profile_model in profiles:
                       profile_data = profile_model.objects.filter(token=request.user.token).first()
                       if isinstance(profile_data, User):
                            if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today=Follow_claim_coins.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 10 and today < 1:
                                    print("10 user complite")
                                    user_profile = User.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    print(user_profile.coins)
                                    common_profile = Common.objects.get(token=request.user.token)
                                    message = f"You got {10} coins for following 10 users!"
                                    notification = Notificationupdate(user=common_profile, message=message)
                                    notification.save()
                                    Follow_claim_coins.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)
                                
                       elif isinstance(profile_data, Audio_Jockey):
                           if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today = Audio_JockeyFollow_claim.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 10 and today < 1:
                                    print("10 user complite")
                                    user_profile = Audio_Jockey.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    common_profile = Common.objects.get(token=request.user.token)
                                    message = f"You got {10} coins for following 10 users!"
                                    notification = Notificationupdate(user=common_profile, message=message)
                                    notification.save()
                                    Audio_JockeyFollow_claim.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)
                                
                       elif isinstance(profile_data, Jockey_club_owner):
                           if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today = Jockey_club_owner_Follow_claim.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 10 and today < 1:
                                    print("10 user complite")
                                    user_profile = Jockey_club_owner.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    common_profile = Common.objects.get(token=request.user.token)
                                    message = f"You got {10} coins for following 10 users!"
                                    notification = Notificationupdate(user=common_profile, message=message)
                                    notification.save()
                                    Jockey_club_owner_Follow_claim.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)
                                    
                       elif isinstance(profile_data, Coins_club_owner):
                           if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today = Coins_club_owner_Follow_claim.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 10 and today < 1:
                                    print("10 user complite")
                                    user_profile = Coins_club_owner.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    common_profile = Common.objects.get(token=request.user.token)
                                    message = f"You got {10} coins for following 10 users!"
                                    notification = Notificationupdate(user=common_profile, message=message)
                                    notification.save()
                                    Coins_club_owner_Follow_claim.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)
                                
                       elif isinstance(profile_data, Coins_trader):
                           if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today = Coins_trader_Follow_claim.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 10 and today < 1:
                                    print("10 user complite")
                                    user_profile = Coins_trader.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    common_profile = Common.objects.get(token=request.user.token)
                                    message = f"You got {10} coins for following 10 users!"
                                    notification = Notificationupdate(user=common_profile, message=message)
                                    notification.save()
                                    Coins_trader_Follow_claim.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)     
                                
                return Response({'success': True, 'message': 'Followed user'})
        except Common.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'})
'''
class FollowUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, follow):
        try:
            date = datetime.today().date()
            created_date = datetime.today()
            following_common = Common.objects.get(uid=follow)

            # Check if the user is trying to follow themselves
            if following_common == request.user:
                return Response({"error": "Following and Follow user cannot be the same user."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the follow relationship already exists
            follow_user, created = Follow1.objects.get_or_create(user=request.user, date=date, following_user=following_common)

            if not created:
                # Unfollow the user
                follow_user.delete()
                return Response({'success': True, 'message': 'Unfollowed user'})
            else:
                # Notify the user being followed
                message = f"{Common.objects.get(token=request.user.token).Name} started following you!"
                notification = Notificationupdate(user=following_common, message=message)
                notification.save()

                # Define user profiles for iteration
                profiles = [Audio_Jockey, Coins_club_owner, Coins_trader, Jockey_club_owner, User]
                claim_coins = 10
                for profile_model in profiles:
                    profile_data = profile_model.objects.filter(token=request.user.token).first()

                    if isinstance(profile_data, profile_model):
                        today_follow_user = Follow1.objects.filter(user=request.user, date=date).count()
                        today_claim= Follow_claim_coins.objects.filter(user=request.user,created_date__date=created_date.date()).count() 

                        # Check if the conditions are met for awarding coins
                        if today_follow_user == 10 and today_claim< 1:
                            user_profile = profile_model.objects.get(token=request.user.token)
                            user_profile.coins += claim_coins
                            user_profile.save()

                            common_profile = Common.objects.get(token=request.user.token)
                            message = f"You got {claim_coins} coins for following 10 users!"
                            notification = Notificationupdate(user=common_profile, message=message)
                            notification.save()

                            Follow_claim_coins.objects.create(user=request.user, created_date=created_date, claim_coins=True)
                            return Response({'success': "claim success"}, status=status.HTTP_201_CREATED)

                return Response({'success': True, 'message': 'Followed user'})
        except Common.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'})
    
class FollowerList(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        user = request.user  
        followers = Follow1.objects.filter(following_user=user)
        followed_users = Follow1.objects.filter(user=user, following_user__in=followers.values_list('user', flat=True))
        
        queryset = self.annotate_followers(followers, followed_users)
        serializer = getfollowerSerializer(queryset, many=True)
        
        return Response(serializer.data)
    

    def annotate_followers(self, followers, followed_users):
        user_dict = {}
        followed_users_set = set(followed_users.values_list('following_user', flat=True))
        
        for follower in followers:
            following_user = follower.user
            user_dict[following_user.id] = {
                "id": following_user.id,
                "Name": following_user.Name,
                "email": following_user.email,
                "Gender": following_user.Gender,
                "Dob": following_user.Dob,
                "profile_picture": following_user.profile_picture,
                "Introduction_voice": following_user.Introduction_voice,
                "Introduction_text": following_user.Introduction_text,
                "is_followed": following_user.id in followed_users_set
            }
        
        return list(user_dict.values())


class FollowingList(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, *args, **kwargs):
        following = Follow1.objects.filter(user=request.user)
        followed_users = [follow_obj.following_user for follow_obj in following]

        user_data_list = []
        for user in followed_users:
            user_data = {
                "id": user.id,
                "Name": user.Name,
                "email": user.email,
                "Gender": user.Gender,
                "Dob": user.Dob,
                "profile_picture": user.profile_picture,
                "Introduction_voice": user.Introduction_voice,
                "Introduction_text": user.Introduction_text,
                "is_followed": True  
            }
            user_data_list.append(user_data)

        return Response(user_data_list)


class GetUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, Userid):
        try:
            user = Common.objects.get(uid=Userid)
            serializer = GetUserSerializer(user)
            user_data = serializer.data
            user_data['is_followed'] = self.is_followed(user, request.user)
            user_data['follower_count'] = self.get_follower_count(user)
            user_data['following_count'] = self.get_following_count(user)
            return Response(user_data)
        except Common.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def is_followed(self, user, current_user):
        return Follow1.objects.filter(user=current_user, following_user=user).exists()

    def get_follower_count(self, user):
        return Follow1.objects.filter(following_user=user).count()

    def get_following_count(self, user):
        return Follow1.objects.filter(user=user).count()
    

class GetUserdata(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        try:
            user = Common.objects.get(uid=request.user.uid)
            serializer = GetUserSerializer(user)
            user_data = serializer.data
            user_data['is_followed'] = self.is_followed(user, request.user)
            user_data['follower_count'] = self.get_follower_count(user)
            user_data['following_count'] = self.get_following_count(user)
            return Response(user_data)
        except Common.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def is_followed(self, user, current_user):
        return Follow1.objects.filter(user=current_user, following_user=user).exists()

    def get_follower_count(self, user):
        return Follow1.objects.filter(following_user=user).count()

    def get_following_count(self, user):
        return Follow1.objects.filter(user=user).count()
    

class Searchalluser(ListAPIView):
    serializer_class = UserSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['Name', 'email']

    @method_decorator(authenticate_token)
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Common.objects.exclude(id=self.request.user.id)
        print(queryset)
        user = self.request.user
        queryset = queryset.filter(Is_Approved=True)
        queryset = self.annotate_following(queryset, user)

        # if user:
        #     queryset = self.annotate_following(queryset, user)
            
        return queryset

    def annotate_following(self, queryset, user):
        for user_obj in queryset:
            user_obj.is_following = Follow1.objects.filter(
                user=user, following_user=user_obj).exists()
        return queryset

class Alluser(APIView):
    def get(self, request):
        data=Common.objects.all()
        serialiser = masterSerializer(data,many=True)
        return Response(serialiser.data)
    


class GiftTransfer(APIView):
    @method_decorator(authenticate_token)
    def post(self, request, *args, **kwargs):
        serializer = CoinTransferSerializer(data=request.data)
        if serializer.is_valid():
            receiver_uid = serializer.validated_data['receiver_uid']
            amount = serializer.validated_data['amount']

            try:
                receiver = Common.objects.get(uid=receiver_uid)
                sender = Common.objects.get(uid=request.user.uid)

                if sender == receiver:
                    return Response({"error": "Sender and receiver cannot be the same user."}, status=status.HTTP_400_BAD_REQUEST)
                
                profiles = [Audio_Jockey, Coins_club_owner, Coins_trader, Jockey_club_owner, User]

                for profile_model in profiles:
                    receiver_profile = profile_model.objects.filter(uid=receiver.uid)
                    if receiver_profile.exists():
                        receipient = receiver_profile.first()
                        receipient.coins += amount
                        receipient.save()
                        message = f"You received a gift of {amount} coins from {sender.Name}!"
                        notification = Notificationupdate(user=receiver, message=message)
                        notification.save()
                        print(receipient.coins, "receipient.coins")

                for profile_model in profiles:
                    sender_profile = profile_model.objects.filter(token=sender.token)
                    if sender_profile.exists():
                        sender_user = sender_profile.first()
                        if sender_user.coins >= amount:
                            sender_user.coins -= amount
                            sender_user.save()
                            GiftTransactionhistory.objects.create(sender=sender, receiver=receiver, amount=amount, created_date=datetime.today())
                            return Response({"message": f"'{amount} $'{sender.Name}'{sender.usertype}Coins transferred successfully."}, status=status.HTTP_200_OK)
                        
                return Response({"error": "Insufficient coins in the sender's account."}, status=status.HTTP_400_BAD_REQUEST)
            except Common.DoesNotExist:
                return Response({"error": f"User with UID '{receiver_uid}' not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class Top_fans_listing_View(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user = Common.objects.get(uid=request.user.uid)
            month = request.query_params.get('month')

            if month is not None:
                print("monthly condition")
                current_month_start = timezone.now().month
                received_transactions = GiftTransactionhistory.objects.filter(receiver=user, created_date__month=current_month_start)

            else:
                print("lifetime condition")
                received_transactions = GiftTransactionhistory.objects.filter(receiver=user)

            sorted_transactions = received_transactions.order_by('-created_date')

            total_coins_dict = {}

            for transaction in sorted_transactions:
                from_user_name = transaction.sender.Name
                profile = transaction.sender.profile_picture
                uid = transaction.sender.uid
                coins = transaction.amount
                recieve = transaction.receiver.Name
        

                if from_user_name in total_coins_dict:
                    total_coins_dict[from_user_name] += coins
                else:
                    total_coins_dict[from_user_name] = {
                        "Gift_sender": from_user_name,
                        "profile_picture": transaction.sender.profile_picture,
                        "uid": transaction.sender.uid,
                        "coins": coins,
                        "reciever": recieve,
                    }
            data = sorted(
                list(total_coins_dict.values()),
                key=lambda x: x["coins"],
                reverse=True
            )

            return Response({"Top_fan_list": data})

        except Common.DoesNotExist:
            return Response({'error': 'User not found.'})

        except GiftTransactionhistory.DoesNotExist:
            return Response({'error': 'No transactions received by User.'})

        except Exception as e:
            return Response({'error': str(e)})
        

class TopUserListView(APIView):
    def get(self, request, id=None):
        try:
            Daliy = request.query_params.get('Daliy')
            weekly = request.query_params.get('weekly')
            month = request.query_params.get('month')
            commonuser = Common.objects.all()
            # total_coins_dict = {}
            total_coins_dict = {commonuser.Name: 0 for commonuser in commonuser}
            

            for commonuser in commonuser:
                if month is not None:
                    print("monthly condition")
                    current_month_start = timezone.now().month
                    received_transactions = GiftTransactionhistory.objects.filter(receiver=commonuser, created_date__month=current_month_start)
                
                elif Daliy is not None:
                    print("Daliy condition")
                    today = datetime.today()
                    received_transactions = GiftTransactionhistory.objects.filter(created_date__date=today.date())
                
                elif weekly is not None:
                    print("weekly condition")
                    last_week = datetime.today() - timedelta(days=7)
                    received_transactions = GiftTransactionhistory.objects.filter(created_date__gte=last_week)
                    
                else:
                    print("lifetime condition")
                    received_transactions = GiftTransactionhistory.objects.filter(receiver=commonuser)
                sorted_transactions = received_transactions.order_by('-created_date')
                # print(sorted_transactions)
                for transaction in sorted_transactions:
                    from_user_name = transaction.sender.Name
                    coins = transaction.amount
                    profile = transaction.sender.profile_picture
                    uid = transaction.sender.uid


                    if from_user_name in total_coins_dict:
                        total_coins_dict[from_user_name] += coins
                    else:
                        total_coins_dict[from_user_name] = coins
            print("total_coins_dict",total_coins_dict)
            vip_data = sorted(
                [{"Sender_user": user, "coins": total_coins,"profile_picture":profile,"uid":uid} for user, total_coins in total_coins_dict.items()],
                key=lambda x: x["coins"],
                reverse=True
            )
            return Response({"top_list_user": vip_data})

        except GiftTransactionhistory.DoesNotExist:
            return Response({'error': 'No transactions received by any user.'})

        except Exception as e:
            return Response({'error': str(e)})


class ApprovedByAdminAllUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        response_data = {}

        user_types = {
            'AudioJockey': Audio_Jockey,
            'Jockeyclubowner': Jockey_club_owner,
            'Coinstrader': Coins_trader,
            'Coinsclubowner': Coins_club_owner,
        }

        for param, model in user_types.items():
            is_approved = request.query_params.get(param)
            if is_approved is not None:
                is_approved = is_approved.lower() == 'true'
                approved_users = model.objects.filter(Is_Approved=is_approved)
                user_serializer = AllCoinsTraderSerializer(approved_users, many=True)
                print("user_serializer",user_serializer)

                data_list = [{'id': user_data.get('id'),'Name': user_data.get('Name'),'phone': user_data.get('phone'),'uid':user_data.get('uid'),'profile_picture':user_data.get('profile_picture')}for user_data in user_serializer.data]

                model_name = model.__name__
                response_data[model_name] = data_list

        if not any(response_data):
            return Response({'error': 'Users parameter is missing or invalid.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_200_OK)
