from django.contrib import admin
from .models import User,Follow, Social_media,claim_coins,room_join_claim_coins,Paymentgatway,Transaction
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Social_media)
admin.site.register(claim_coins)
admin.site.register(room_join_claim_coins)
admin.site.register(Paymentgatway)
admin.site.register(Transaction)