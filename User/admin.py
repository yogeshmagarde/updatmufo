from django.contrib import admin
from .models import * #User,Follow, Social_media,claim_coins,room_join_claim_coins,Transaction

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Social_media)
admin.site.register(Transaction)
admin.site.register(room_join_claim_coins)
admin.site.register(claim_coins)
admin.site.register(Coinsclubownerdaliylogin)
admin.site.register(Coins_traderdaliylogin)
admin.site.register(Jockeyclubownerlogin)
admin.site.register(Audiojockeyloigin)


