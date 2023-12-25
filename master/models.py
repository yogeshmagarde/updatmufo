
# Create your models here.
from django.db import models
from django.utils.timezone import now
from Coins_club_owner.models import *
from Coins_trader.models import *
from Jockey_club_owner.models import *
from Audio_Jockey.models import *
from User.models import *
class Common(models.Model):
    Name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,unique=True)
    Gender = models.CharField(max_length=20, default='')
    Dob = models.DateField(blank=True,  default='')
    profile_picture = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_voice = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_text = models.CharField(max_length=500, default='')
    Invitation_Code = models.IntegerField(null=True, blank=True)
    otp = models.CharField(max_length=8, null=True, blank=True)
    uid = models.CharField(max_length=50, null=True, blank=True)
    usertype = models.CharField(max_length=50, null=True, blank=True)
    token = models.CharField(max_length=300, null=True, blank=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    Otpcreated_at = models.DateTimeField(null=True, blank=True)
    Is_Approved= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    coins = models.PositiveIntegerField(default=0) 
    def __str__(self):
        return str(self.Name)



class Follow1(models.Model):
    user = models.ForeignKey(Common, related_name='following', on_delete=models.CASCADE)
    following_user = models.ForeignKey(Common, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.CharField(max_length=100)
    
   

class Follow_claim_coins(models.Model):
    user = models.ForeignKey(Common, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(max_length=100)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)+"          "+ str(self.created_date)
    


class Audio_JockeyFollow_claim(models.Model):
    user = models.ForeignKey(Common, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(max_length=100)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)+"          "+ str(self.created_date)
    
class Jockey_club_owner_Follow_claim(models.Model):
    user = models.ForeignKey(Common, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(max_length=100)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)+"          "+ str(self.created_date)
    
class Coins_club_owner_Follow_claim(models.Model):
    user = models.ForeignKey(Common, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(max_length=100)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)+"          "+ str(self.created_date)
    
class Coins_trader_Follow_claim(models.Model):
    user = models.ForeignKey(Common, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(max_length=100)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)+"          "+ str(self.created_date)
    
