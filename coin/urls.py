from django.urls import path
from .views import *
from . import views

urlpatterns = [
    
    path("clubowner/", transfar1.as_view(), name="clubowner"),
    path("clubowner/<int:id>", transfar1.as_view()),
    path("cointrader/<int:id>", CoinTransfer2.as_view()),
    path("cointrader/", CoinTransfer2.as_view()),
    path("jokyclubowner/", CoinTransfer3.as_view()),
    path("jokyclubowner/<int:id>", CoinTransfer3.as_view()),
    path("usercoins/", CoinTransfer31.as_view()),
    path("usercoins/<int:id>", CoinTransfer31.as_view()),
    path("audiojoky/<int:id>", CoinTransfer4.as_view()),
    path("audiojoky/", CoinTransfer4.as_view()),
    path("traderth/", cointraderTransactionHistoryView.as_view()),
    path("clubownerth/", clubownerTransactionHistoryView.as_view()),
    path("userth/", UserTransactionHistoryView.as_view()),
    path("Audiojockeyth/", Audio_JockeyTransactionHistoryView.as_view()),
    path("jokyclubownerth/", Jockey_club_ownerTransactionHistoryView.as_view()),


    path("Audio_Jockeytopfanslist/", Audio_JockeyTop_fans_listing_View.as_view()),
    path("Usertopfanlist/", UserTop_fans_listing_View.as_view()),
    path("Cointradertopfanslist/", CointraderTop_fans_listing_View.as_view()),
    path("jokeyclubtopfanslist/", Jockey_club_ownerTop_fans_listing_View.as_view()),
    
    path("globletopfanslist/", Top_fans_listing_globle_View.as_view()),
    path("listofAudioJockey/", listofAudioJockey.as_view()),
          

    
]
