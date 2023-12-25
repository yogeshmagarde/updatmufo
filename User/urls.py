from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from .views import *

urlpatterns = [

    path("", views.Users, name="User"),
    path("Register/", Register.as_view(), name="Register"),
    path('login/', Login.as_view(), name="login"),
    path('otp/<uid>/', Otp.as_view() , name='otp'),
    path('getUserData/', GetUserdata.as_view(), name="GetUserdata"),
    path('Updateuser/', UpdateUser.as_view(), name="Updateuser"),
    path('Searchalluser/', Searchalluser.as_view(), name="userview"),
    path('getUser/<int:Userid>/', GetUser.as_view(), name='getUser'),
    path('follow/<int:follow>/', FollowUser.as_view(), name='follow-user'),
    path('followers/', FollowerList.as_view(), name='follower-list'),
    path('following/', FollowingList.as_view(), name='following-list'),
    path('userview/', userview.as_view(), name="userview"),
    path('alluser/', Alluser.as_view(), name="userview"),
    path("Socialmedia/", Socialmedia.as_view(), name="Socialmedia"),
    path("googlelogin/", Googlelogin.as_view(), name="Googlelogin"),
    path("Facebooklogin/", Facebooklogin.as_view(), name="Facebooklogin"),
    path("Snapchatlogin/", Snapchatlogin.as_view(), name="Facebooklogin"),
    #task center
    path("Coinsclaim/", Coinsclaim.as_view(), name="Coinsclaim"),
    path("Coinsclubownerclaim/", Coins_club_ownerdaliyclaim.as_view()),
    path("Coinstraderclaim/", Coinstraderdaliyclaim.as_view()),
    path("Jokeyclaim/", Jockey_club_ownerdaliyclaim.as_view()),
    path("Audiojokeyclaim/", Audio_Jockeydaliyclaim.as_view()),
    path('order_create/',RazorpayOrderAPIView.as_view()),
    path('order_complete/', TransactionAPIView.as_view()),
   
]
