from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(User,models.Model):
    LoginName = models.CharField(max_length=100)
    vchr_UserName = models.CharField(max_length=150,unique = True)
    vchr_email = models.CharField(max_length=300)



    def __str__(self):
        return self.vchr_UserName


class AccountType(models.Model):
    AccountTypeId = models.BigAutoField(primary_key=True)
    AccountTypeName = models.CharField(max_length=350,unique = True)
    AccountTypeShortName = models.CharField(max_length=350,unique = True)
    createdBy = models.ForeignKey(UserDetails, models.DO_NOTHING)
    createdOn = models.DateTimeField()

    def __str__(self):
        return self.AccountTypeName


class AccountDetails(models.Model):
    AccountId = models.BigAutoField(primary_key=True)
    AccountNo = models.CharField(max_length=350,unique = True)
    AccountHoldersName = models.CharField(max_length=350)
    Address = models.TextField(blank=True, null=True)
    Country = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    DateOfBirth = models.DateField(blank=True, null=True)
    Age = models.IntegerField(blank=True, null=True)
    Sex = models.CharField(max_length=100)
    ContactNo = models.BigIntegerField()
    ContactEmail = models.CharField(max_length=300)
    AccountTypeId = models.ForeignKey(AccountType, models.DO_NOTHING)
    createdBy = models.ForeignKey(UserDetails, models.DO_NOTHING)
    createdOn = models.DateTimeField()


    def __str__(self):
        return self.AccountHoldersName
