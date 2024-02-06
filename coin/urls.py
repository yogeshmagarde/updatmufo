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
    # path("traderth/", cointraderTransactionHistoryView.as_view()),
    # path("clubownerth/", clubownerTransactionHistoryView.as_view()),
    # path("userth/", UserTransactionHistoryView.as_view()),
    # path("Audiojockeyth/", Audio_JockeyTransactionHistoryView.as_view()),
    
    path("clubownerpurchaseth/", clubownerpurchaseTransactionHistoryView.as_view()),
    path("clubownerspendth/", clubownespendTransactionHistoryView.as_view()),
    path("traderpurchaseth/", CointraderpurchaseTransactionHistoryView.as_view()),
    path("traderspendth/", CointraderspendTransactionHistoryView.as_view()),
    path("userspendth/", UserspendTransactionHistoryView.as_view()),
    path("userpurchseth/", UserpurchaseTransactionHistoryView.as_view()),
    path("Audiojockeypurchseth/", Audio_JockeypurchaseTransactionHistoryView.as_view()),
    path("Audio_Jockey_and_Jockey_club_owner/", Audio_Jockey_and_Jockey_club_owner_spendTransactionHistoryView.as_view()),
    path("jokyclubownerpurchaseth/", Jockey_club_ownerpurchaseTransactionHistoryView.as_view()),

    path("allspend/",TotalUserspendTransactionHistoryView.as_view()),
    
    path("audiojockeytoplist/",Top_fans_listing_globle_View.as_view()),
    path("listofAudioJockey/", listofAudioJockey.as_view()),
    path("alluserpurchasehistory/", AllUserpurchaseHistoryView.as_view()),
          
]
