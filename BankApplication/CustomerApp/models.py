from django.db import models

# Create your models here.


class signup(models.Model):
    UserId=models.AutoField(primary_key=True)
    Email=models.CharField(max_length=150)
    UserName=models.CharField(max_length=100)
    Mobilenumber=models.CharField(max_length=20)
    Password=models.CharField(max_length=50)
    Confirmpassword=models.CharField(max_length=100)
    
    # DateOfBirth=models.DateField()
class Transaction(models.Model):
        accountNumber=models.CharField(max_length=10)
        amount=models.DecimalField(max_digits=10,decimal_places=2)
    
    