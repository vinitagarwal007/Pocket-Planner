from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,unique=True)
    balance = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.name

class category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    is_credit = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.name

class transaction(models.Model):
    created_on = models.DateField(auto_now=True)
    account = models.ForeignKey(account, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(category,on_delete=models.DO_NOTHING)
    transaction_description = models.CharField(max_length=100)
    transaction_amount = models.IntegerField(default=0)
    is_credit = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.transaction_description

