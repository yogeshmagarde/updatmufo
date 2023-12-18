from django.shortcuts import render

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
from datetime import *
from datetime import *
# class FollowUser(APIView):
#     @method_decorator(authenticate_token)
#     def get(self, request, follow):
#         try:
#             following_common = Common.objects.get(uid=follow)  
#             follow_user, created = Follow1.objects.get_or_create(user=request.user, following_user=following_common)
        
#             print("Follow User:", follow_user)
            
#             if not created:
#                 follow_user.delete()
#                 return Response({'success': True, 'message': 'Unfollowed user'})
#             else:
#                 if created:
#                     today = datetime.now(timezone.utc)
#                     start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
#                     end_of_day = today.replace(hour=23, minute=59, second=59, microsecond=999999)
#                     today_follow_user = Follow1.objects.filter(user=request.user,created_at__range=(start_of_day, end_of_day)).count()
#                     print(today_follow_user)
#                     if today_follow_user == 10:
#                         print("10 user complite")
#                         profiles = [Audio_Jockey, Coins_club_owner,Coins_trader, Jockey_club_owner, User]
#                         for profile_model in profiles:
#                                 profile_data = profile_model.objects.filter(token=request.user.token).first()
        
#                                 if isinstance(profile_data, User):
#                                     user_profile = User.objects.get(token=request.user.token)
#                                     if not user_profile.coins:
#                                         print(f"get {10} coins user account.")
#                                         user_profile.coins += 10
#                                         user_profile.save()
#                                         print(user_profile.coins)
                                        
#                                 elif isinstance(profile_data, Audio_Jockey):
#                                     user_profile = Audio_Jockey.objects.get(token=request.user.token)
#                                     if not user_profile.coins:
#                                         print(f"get {10} coins user account.")
#                                         user_profile.coins += 10
#                                         user_profile.save()
#                                         print(user_profile.coins)

#                                 elif isinstance(profile_data, Coins_club_owner):
#                                     user_profile = Coins_club_owner.objects.get(token=request.user.token)
#                                     if not user_profile.coins:
#                                         print(f"get {10} coins user account.")
#                                         user_profile.coins += 10
#                                         user_profile.save()
#                                         print(user_profile.coins)

#                                 elif isinstance(profile_data, Coins_trader):
#                                     user_profile = Coins_trader.objects.get(token=request.user.token)
#                                     if not user_profile.coins:
#                                         print(f"get {10} coins user account.")
#                                         user_profile.coins += 10
#                                         user_profile.save()
#                                         print(user_profile.coins)

#                                 elif isinstance(profile_data, Jockey_club_owner):
#                                     user_profile = Jockey_club_owner.objects.get(token=request.user.token)
#                                     if not user_profile.coins:
#                                         print(f"get {10} coins user account.")
#                                         user_profile.coins += 10
#                                         user_profile.save()
#                                         print(user_profile.coins)     

#                 return Response({'success': True, 'message': 'Followed user'})
#         except Common.DoesNotExist:
#             return Response({'success': False, 'message': 'User does not exist.'})


class FollowUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, follow):
        try:
            # date = request.data.get("date")
            date=datetime.today().date()
            print("aaj",date)
            created_date = datetime.today()
            following_common = Common.objects.get(uid=follow)  
            follow_user, created = Follow1.objects.get_or_create(user=request.user,date = date, following_user=following_common)
            
            print("Follow User:", follow_user)
            
            if not created:
                follow_user.delete()
                return Response({'success': True, 'message': 'Unfollowed user'})
            else:
                profiles = [Audio_Jockey, Coins_club_owner,Coins_trader, Jockey_club_owner, User]
                for profile_model in profiles:
                       profile_data = profile_model.objects.filter(token=request.user.token).first()
                       if isinstance(profile_data, User):
                            if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today=Follow_claim_coins.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 2 and today < 1:
                                    print("10 user complite")
                                    user_profile = User.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    print(user_profile.coins)
                                    Follow_claim_coins.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)
                                
                       elif isinstance(profile_data, Audio_Jockey):
                           if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today = Audio_JockeyFollow_claim.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 2 and today < 1:
                                    print("10 user complite")
                                    user_profile = Audio_Jockey.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    print(user_profile.coins)
                                    Audio_JockeyFollow_claim.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)
                                
                       elif isinstance(profile_data, Jockey_club_owner):
                           if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today = Jockey_club_owner_Follow_claim.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 2 and today < 1:
                                    print("10 user complite")
                                    user_profile = Jockey_club_owner.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    print(user_profile.coins)
                                    Jockey_club_owner_Follow_claim.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)
                                    
                       elif isinstance(profile_data, Coins_club_owner):
                           if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today = Coins_club_owner_Follow_claim.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 2 and today < 1:
                                    print("10 user complite")
                                    user_profile = Coins_club_owner.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    print(user_profile.coins)
                                    Coins_club_owner_Follow_claim.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)
                                
                       elif isinstance(profile_data, Coins_trader):
                           if created:
                                today_follow_user = Follow1.objects.filter(user=request.user,date = date).count()
                                print(today_follow_user)
                                today = Coins_trader_Follow_claim.objects.filter(user=request.user,created_date__date=created_date.date()).count()
                                print(today,"today claim")
                                if today_follow_user == 2 and today < 1:
                                    print("10 user complite")
                                    user_profile = Coins_trader.objects.get(token=request.user.token)
                                    print(f"get {10} coins user account.")
                                    user_profile.coins += 10 
                                    user_profile.save()
                                    print(user_profile.coins)
                                    Coins_trader_Follow_claim.objects.create(user=request.user,created_date=created_date, claim_coins=True)
                                    return Response({'success':"claim success"}, status=status.HTTP_201_CREATED)     
                                
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
    


# class CoinTransfer(APIView):
#     @method_decorator(authenticate_token)
#     def post(self, request, *args, **kwargs):
#         serializer = CoinTransferSerializer(data=request.data)
#         if serializer.is_valid():
#             receiver_uid = serializer.validated_data['receiver_uid']
#             amount = serializer.validated_data['amount']
#             try:
#                 receiver = Common.objects.get(uid=receiver_uid)
#                 sender = Common.objects.get(uid=request.user.uid)
#                 uid=receiver.uid
#                 token=sender.token
#                 profiles = [Audio_Jockey, Coins_club_owner,Coins_trader, Jockey_club_owner, User]
#                 for profile_model in profiles:
#                        profile = profile_model.objects.filter(uid=uid)
#                        if profile.exists():
#                             if profile_model == User or Audio_Jockey or Coins_club_owner or Coins_trader or Jockey_club_owner:
#                                 recever_user = profile.first()
#                                 recever_user.coins += amount
#                                 recever_user.save()
#                                 print(recever_user.coins, "recever_user.coins")
#                             else:
#                                 print("no username")

#                        profile_data = profile_model.objects.filter(token=token)
#                        if profile_data.exists():
#                             if profile_model == User or Audio_Jockey or Coins_club_owner or Coins_trader or Jockey_club_owner:
#                                 sender_user = profile_data.first()
#                                 if sender_user.coins >= amount:
#                                         sender_user.coins -= amount
#                                         sender_user.save()
#                                         return Response({"message": "Coins transferred successfully."}, status=status.HTTP_200_OK)
#                             else:
#                                 print("no username")
#                 if sender.coins >= amount:
#                     sender.coins -= amount
#                     sender.save()

#                     receiver.coins += amount
#                     receiver.save()

#                     return Response({"message": "Coins transferred successfully."}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"error": "Insufficient coins in the sender's account."}, status=status.HTTP_400_BAD_REQUEST)
#             except Common.DoesNotExist:
#                 return Response({"error": f"User with UID '{receiver_uid}' not found."}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                        print(receipient.coins, "receipient.coins")

                for profile_model in profiles:
                    sender_profile = profile_model.objects.filter(token=sender.token)
                    if sender_profile.exists():
                        sender_user = sender_profile.first()
                        if sender_user.coins >= amount:
                            sender_user.coins -= amount
                            sender_user.save()
                            GiftTransactionhistory.objects.create(sender=sender, receiver=receiver, amount=amount, created_date=datetime.today())
                            return Response({"message": f"'{amount} $' Coins transferred successfully."}, status=status.HTTP_200_OK)
                        
                return Response({"error": "Insufficient coins in the sender's account."}, status=status.HTTP_400_BAD_REQUEST)
            except Common.DoesNotExist:
                return Response({"error": f"User with UID '{receiver_uid}' not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# class Top_fans_listing_View(APIView):
#     @method_decorator(authenticate_token)
#     def get(self, request, id=None):
#         try:
#             user = Common.objects.get(uid=request.user.uid)
#             time_period = request.query_params.get('time_period')

#             if time_period is not None:
#                 print("monthly condition")
#                 current_month = timezone.now().month
#                 received_transactions = GiftTransactionhistory.objects.filter(receiver=user,created_date__month=current_month)
#             else:
#                 print("lifetime condition")
#                 received_transactions = GiftTransactionhistory.objects.filter(receiver=user)
#             sorted_transactions = received_transactions.order_by('-created_date')

#             total_coins_dict = {}

#             for transaction in sorted_transactions:
#                 from_user_name = transaction.sender
#                 coins = transaction.amount

#                 if from_user_name in total_coins_dict:
#                     total_coins_dict[from_user_name] += coins
#                 else:
#                     total_coins_dict[from_user_name] = coins

#             vip_data = sorted(
#                 [{"from_trader": user, "coins": total_coins} for user, total_coins in total_coins_dict.items()],
#                 key=lambda x: x["coins"],
#                 reverse=True
#             )

#             return Response({"vip_data": vip_data})

#         except Audio_Jockey.DoesNotExist:
#             return Response({'error': 'User not found.'})

#         except GiftTransactionhistory.DoesNotExist:
#             return Response({'error': 'No transactions received by User.'})

#         except Exception as e:
#             return Response({'error': str(e)})
        




class Top_fans_listing_View(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user = Common.objects.get(uid=request.user.uid)
            time_period = request.query_params.get('time_period')

            if time_period is not None:
                print("monthly condition")
                current_month = timezone.now().month
                received_transactions = GiftTransactionhistory.objects.filter(
                    receiver=user, created_date__month=current_month
                )
            else:
                print("lifetime condition")
                received_transactions = GiftTransactionhistory.objects.filter(receiver=user)

            sorted_transactions = received_transactions.order_by('-created_date')

            total_coins_dict = {}
            max_coins_sender = None  # Variable to store the sender with the highest total coins

            for transaction in sorted_transactions:
                from_user_name = transaction.sender
                coins = transaction.amount

                if from_user_name in total_coins_dict:
                    total_coins_dict[from_user_name] += coins
                else:
                    total_coins_dict[from_user_name] = coins

                # Update max_coins_sender if the current sender has more coins
                if max_coins_sender is None or total_coins_dict[from_user_name] > total_coins_dict[max_coins_sender]:
                    max_coins_sender = from_user_name

            vip_data = sorted(
                [{"from_trader": user, "coins": total_coins} for user, total_coins in total_coins_dict.items()],
                key=lambda x: x["coins"],
                reverse=True
            )

            return Response({"vip_data": vip_data, "max_coins_sender": max_coins_sender})

        except Common.DoesNotExist:
            return Response({'error': 'User not found.'})

        except GiftTransactionhistory.DoesNotExist:
            return Response({'error': 'No transactions received by User.'})

        except Exception as e:
            return Response({'error': str(e)})