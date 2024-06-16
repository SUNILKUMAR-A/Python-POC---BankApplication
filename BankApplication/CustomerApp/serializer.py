from rest_framework import serializers
from CustomerApp.models import signup,Transaction

class signupSerializer(serializers.ModelSerializer):
    class Meta:
        model=signup
        fields=('UserId',
                "Email",
                "UserName",
                "Mobilenumber",
                "Password",
                "Confirmpassword"
                )
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields=('accountNumber',
                'amount'
                )


