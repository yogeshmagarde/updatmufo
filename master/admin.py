from django.contrib import admin

# Register your models here.
from .models import*
admin.site.register(Common)
admin.site.register(Follow1)
admin.site.register(Follow_claim_coins)
admin.site.register(Audio_JockeyFollow_claim)
admin.site.register(Jockey_club_owner_Follow_claim)
admin.site.register(Coins_club_owner_Follow_claim)
admin.site.register(Coins_trader_Follow_claim)