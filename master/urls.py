from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('follow/<uuid:follow>/', FollowUser.as_view(), name='follow-user'),
    path('follow/<uuid:follow>/<str:date>', FollowUser.as_view(), name='follow-user'),
    path('followers/', FollowerList.as_view(), name='follower-list'),
    path('following/', FollowingList.as_view(), name='following-list'),
    path('getUser/<uuid:Userid>/', GetUser.as_view(), name='getUser'),
    path('getUserData/', GetUserdata.as_view(), name="GetUserdata"),
    path('Searchalluser/', Searchalluser.as_view(), name="userview"),
    # path('coinSearchalluser12/', CoinTraderSearchAllUser.as_view(), name="userview"),
    
    path('allcommonuser/', Alluser.as_view(), name="userview"),
    path('gift-transfer/', GiftTransfer.as_view(), name='coin-transfer'),
    path('user-spent-time/', UserSpentTimeList.as_view(), name='user-spent-time-list'),
    path('topfanlist/', Top_fans_listing_View.as_view(), name='topfanlist'),
    path("usertoplist/", TopUserListView.as_view(),name='topuserlist'),
    path("all_coinstranding_userlist/", ApprovedByAdminAllUser.as_view(),name='Alluserlist'),
    path("user_notification/",Notification.as_view(), name='notification'),

    path('Coins_club_ownerSearchalluser/', Coins_club_ownerSearchAllUser.as_view(), name="userview"),
    path('Coins_traderSearchalluser/', Coins_traderSearchAllUser.as_view(), name="userview"),
    path('AudiojockeySearchalluser/', Audio_JockeySearchAllUser.as_view(), name="userview"),
    path('JockeyclubownerSearchalluser/', Jockey_club_ownerSearchAllUser.as_view(), name="userview"),
]
