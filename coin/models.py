from django.db import models

# Create your models here.
from Coins_club_owner.models import *
from Coins_trader.models import *
from Jockey_club_owner.models import *
from Audio_Jockey.models import *
from User.models import *

from django.utils.timezone import now

class Admin_to_Coins_club_owner(models.Model):
    Coins_Club_Owner_Id = models.ForeignKey(Coins_club_owner,on_delete=models.CASCADE)
    numcoin = models.PositiveIntegerField(blank=False)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.Coins_Club_Owner_Id)



class Coins_club_owner_to_Coins_trader(models.Model):
    from_owner = models.ForeignKey(Coins_club_owner, on_delete=models.CASCADE)
    to_trader = models.ForeignKey(Coins_trader, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.to_trader)
    

class Coins_trader_to_Jockey_club_owner(models.Model):
    from_trader = models.ForeignKey(Coins_trader, on_delete=models.CASCADE)
    to_Jockey_club_owner = models.ForeignKey(Jockey_club_owner, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.to_Jockey_club_owner)


class Coins_trader_to_User(models.Model):
    from_trader = models.ForeignKey(Coins_trader, on_delete=models.CASCADE)
    to_User = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.to_User)
class User_to_Audio_Jockey(models.Model):
    from_User = models.ForeignKey(User, on_delete=models.PROTECT)
    to_Audio_Jockey = models.ForeignKey(Audio_Jockey, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.to_Audio_Jockey)