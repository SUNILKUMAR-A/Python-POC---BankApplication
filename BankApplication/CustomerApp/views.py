from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt  # Use with caution in production!
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from CustomerApp.models import signup, Transaction  # User and Transaction models
from CustomerApp.serializer import signupSerializer, TransactionSerializer  # Serializers

from django.core.files.storage import default_storage  # Not used in this code snippet


# Create your views here.


@csrf_exempt
def transactionApi(request):
    """Handles POST requests for transactions (deposit or withdrawal)."""
    if request.method == "POST":
        transaction_data = JSONParser().parse(request)  # Parse JSON data from request body

        # Prepare transaction data for serialization
        transaction_data1 = {
            'accountNumber': transaction_data['accountNumber'],
            'amount': transaction_data['amount']
        }

        transaction_serializer = TransactionSerializer(data=transaction_data1)

        if transaction_serializer.is_valid():
            # Check if account number exists
            if Transaction.objects.filter(accountNumber=transaction_data1['accountNumber']):
                amt = Transaction.objects.get(accountNumber=transaction_data1['accountNumber'])

                # Update amount based on transaction type (deposit or withdrawal)
                if transaction_data['selectedTransaction'] == 'deposit':
                    transaction_data1["amount"] = int(transaction_data1["amount"]) + int(amt.amount)
                    transaction_serializer = TransactionSerializer(amt, data=transaction_data1)
                    if transaction_serializer.is_valid():
                        transaction_serializer.save()
                        return JsonResponse("updated successfully", safe=False)
                elif transaction_data['selectedTransaction'] == 'withdrawal':
                    transaction_data1["amount"] = int(amt.amount) - int(transaction_data1["amount"])
                    if transaction_data1["amount"] < 200:
                        return JsonResponse("Insufficient Balance", safe=False)
                    transaction_serializer = TransactionSerializer(amt, data=transaction_data1)
                    if transaction_serializer.is_valid():
                        transaction_serializer.save()
                        return JsonResponse("Withdrawal Successfull", safe=False)
            else:  # Account number not found
                if transaction_data['selectedTransaction'] == 'deposit':
                    if transaction_serializer.is_valid():
                        transaction_serializer.save()
                        return JsonResponse("Transaction successfully", safe=False)
                elif transaction_data['selectedTransaction'] == 'withdrawal':
                    return JsonResponse("enter Correct Account Number", safe=False)

    return JsonResponse("Failed Transaction", safe=False)


@csrf_exempt
def loginApi(request):
    """Handles POST requests for login."""
    if request.method == "POST":
        login_data = JSONParser().parse(request)  # Parse JSON data from request body
        email = login_data["Email"]
        password = login_data["Password"]

        try:
            user = signup.objects.get(Email=email)  # Attempt to retrieve user object
        except Exception:
            return JsonResponse({"message": "User Not Exist in 1st"}, safe=False)

        if user is None:
            return JsonResponse({"message": "User Not Exist in 2st"}, safe=False)

        if password != user.Password:
            return JsonResponse({"message": "Incorrectpassword"}, safe=False)

        # Login successful
        return JsonResponse({
            'message': 'Login Successfully',
            'data': user.UserId
        }, safe=False)


@csrf_exempt
def signupApi(request):
    """Handles POST requests for user signup."""
    if request.method == "POST":
        user_data = JSONParser().parse(request)
        user_serializer = signupSerializer(data=user_data)

        if user_serializer.is_valid():
            if signup.objects.filter(Email=user_data['Email']).exists():
                return JsonResponse("User Email Already Exist", safe=False)

            user_serializer.save()
            return JsonResponse("Added Successfully!!..", safe=False)

        return JsonResponse("Failed to Add.", safe=False)


@csrf_exempt
def balanceApi(request):
    """Handles POST requests for checking balance."""
    if request.method == "POST":
        accountnumber = JSONParser().parse(request)
        accountobj = Transaction.objects.get(accountNumber=accountnumber['accountNumber'])
        return JsonResponse(accountobj.amount,safe=False)
        
